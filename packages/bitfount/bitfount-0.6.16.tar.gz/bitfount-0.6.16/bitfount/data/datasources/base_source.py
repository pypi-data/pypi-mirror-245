"""Module containing BaseSource class.

BaseSource is the abstract data source class from which all concrete data sources
must inherit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
import inspect
import logging
import os
from pathlib import Path
import random
import shutil
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    TypeVar,
    Union,
    cast,
)

from filetype import guess_extension
from mypy_extensions import Arg, DefaultNamedArg, KwArg, VarArg
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype as is_datetime

from bitfount.config import BITFOUNT_CACHE_DIR
from bitfount.data.datasources.utils import _modify_column, _modify_file_paths
from bitfount.data.datasplitters import DatasetSplitter, SplitterDefinedInData
from bitfount.data.exceptions import DataNotLoadedError
from bitfount.data.types import (
    DataPathModifiers,
    _Column,
    _GetColumnCallable,
    _GetDtypesCallable,
    _SingleOrMulti,
)
from bitfount.data.utils import _generate_dtypes_hash, _hash_str
from bitfount.hooks import HookType, get_hooks
from bitfount.types import _Dtypes
from bitfount.utils import delegates, seed_all

logger = logging.getLogger(__name__)

# Suffix used for caching images in the file system.
FILE_SYSTEM_ITERABLE_IMAGE_CACHE_SUFFIX: str = "-cache"

# The following constants are used for fast loading of data. Fast loading is used to
# speed up the process of schema generation where only a small subset of the data is
# loaded.
FAST_LOAD_NUMBER_OF_FILES_PERCENTAGE: float = 0.01
FAST_LOAD_MINIMUM_NUMBER_OF_FILES_WITHOUT_NEW_FIELDS: int = 3
FAST_LOAD_MAXIMUM_NUMBER_OF_FILES_WITHOUT_NEW_FIELDS: int = 10
FAST_LOAD_MAXIMUM_NUMBER_OF_FILES_TO_LOAD: int = 50

# This is used for annotating the data in the datasource with
# the inferred label
BITFOUNT_INFERRED_LABEL_COLUMN: str = "BITFOUNT_INFERRED_LABEL"

T = TypeVar("T", bound="BaseSource")
BaseSourceInitSignature = Callable[
    [
        Arg(T, "self"),  # noqa: F821
        VarArg(Any),
        DefaultNamedArg(Optional[DatasetSplitter], "data_splitter"),  # noqa: F821
        DefaultNamedArg(Optional[int], "seed"),  # noqa: F821
        DefaultNamedArg(
            Optional[Dict[str, DataPathModifiers]], "modifiers"  # noqa: F821
        ),
        DefaultNamedArg(Union[str, Sequence[str], None], "ignore_cols"),  # noqa: F821
        KwArg(Any),
    ],
    None,
]


class BaseSource(ABC):
    """Abstract Base Source from which all other data sources must inherit.

    Args:
        data_splitter: Approach used for splitting the data into training, test,
            validation. Defaults to None.
        seed: Random number seed. Used for setting random seed for all libraries.
            Defaults to None.
        modifiers: Dictionary used for modifying paths/ extensions in the dataframe.
            Defaults to None.
        ignore_cols: Column/list of columns to be ignored from the data.
            Defaults to None.

    Attributes:
        data: A Dataframe-type object which contains the data.
        data_splitter: Approach used for splitting the data into training, test,
            validation.
        seed: Random number seed. Used for setting random seed for all libraries.
    """

    def __init__(
        self,
        data_splitter: Optional[DatasetSplitter] = None,
        seed: Optional[int] = None,
        modifiers: Optional[Dict[str, DataPathModifiers]] = None,
        ignore_cols: Optional[Union[str, Sequence[str]]] = None,
        **kwargs: Any,
    ) -> None:
        self._base_source_init = True
        self.data_splitter = data_splitter
        self.seed = seed
        self._modifiers = modifiers
        self._data_is_split: bool = False
        self._data_is_loaded: bool = False
        self._is_task_running: bool = False
        seed_all(self.seed)

        self._train_idxs: Optional[np.ndarray] = None
        self._validation_idxs: Optional[np.ndarray] = None
        self._test_idxs: Optional[np.ndarray] = None

        self._data: pd.DataFrame
        self._table_hashes: Set[str] = set()

        self._ignore_cols: List[str] = []
        if isinstance(ignore_cols, str):
            self._ignore_cols = [ignore_cols]
        elif ignore_cols is not None:
            self._ignore_cols = list(ignore_cols)

        for unexpected_kwarg in kwargs:
            logger.warning(f"Ignoring unexpected keyword argument {unexpected_kwarg}")

        super().__init__()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if not (inspect.isabstract(cls) or ABC in cls.__bases__):
            cls.get_dtypes = cls._get_dtypes()  # type: ignore[method-assign] # reason: wrap subclass get_dtypes # noqa: B950
            cls.get_column = cls._get_column()  # type: ignore[method-assign] # reason: wrap subclass get_column # noqa: B950

    @classmethod
    def _get_dtypes(cls) -> _GetDtypesCallable:
        """Decorate subclass' get_dtypes implementation.

        Decorate subclass' implementation of get_dtypes to handle ignored
        columns and handle `_table_hashes`.
        """
        subclass_get_dtypes = cls.get_dtypes

        def get_dtypes(self: BaseSource, *args: Any, **kwargs: Any) -> _Dtypes:
            dtypes: _Dtypes = subclass_get_dtypes(self, *args, **kwargs)
            if self._ignore_cols:
                for col in self._ignore_cols:
                    if col in dtypes:
                        del dtypes[col]
            self._table_hashes.add(_generate_dtypes_hash(dtypes))
            return dtypes

        return get_dtypes

    @classmethod
    def _get_column(
        cls,
    ) -> _GetColumnCallable:
        """Decorate subclass' get_column implementation.

        Decorate subclass' implementation of get_column to handle ignored
        columns and modifiers.
        """
        subclass_get_column = cls.get_column

        def get_column(
            self: BaseSource, col_name: str, *args: Any, **kwargs: Any
        ) -> _Column:
            column = subclass_get_column(self, col_name, *args, **kwargs)
            if self._modifiers:
                if modifier_dict := self._modifiers.get(col_name):
                    column = _modify_column(column, modifier_dict)
            return column

        return get_column

    @property
    def is_task_running(self) -> bool:
        """Returns True if a task is running."""
        return self._is_task_running

    @is_task_running.setter
    def is_task_running(self, value: bool) -> None:
        """Sets `_is_task_running` to `value`."""
        self._is_task_running = value

    @property
    def is_initialised(self) -> bool:
        """Checks if `BaseSource` was initialised."""
        if hasattr(self, "_base_source_init"):
            return True
        else:
            return False

    @property
    def data(self) -> pd.DataFrame:
        """A property containing the underlying dataframe if the data has been loaded.

        Raises:
            DataNotLoadedError: If the data has not been loaded yet.
        """
        if self._data_is_loaded:
            return self._data
        else:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `load_data` first."
            )

    @data.setter
    def data(self, _data: Optional[pd.DataFrame]) -> None:
        """Data setter."""
        if _data is not None:
            if isinstance(_data, pd.DataFrame):
                if self._ignore_cols:
                    # If columns already ignored in data, ignore errors.
                    _data = _data.drop(columns=self._ignore_cols, errors="ignore")
                self._data = _data

                if self._modifiers:
                    _modify_file_paths(self._data, self._modifiers)

                self._data_is_loaded = True
            else:
                raise TypeError(
                    "Invalid data attribute. "
                    "Expected pandas dataframe for attribute 'data' "
                    f"but received :{type(_data)}"
                )

    @property
    def hash(self) -> str:
        """The hash associated with this BaseSource.

        This is the hash of the static information regarding the underlying DataFrame,
        primarily column names and content types but NOT anything content-related
        itself. It should be consistent across invocations, even if additional data
        is added, as long as the DataFrame is still compatible in its format.

        Returns:
            The hexdigest of the DataFrame hash.
        """
        if not self._table_hashes:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `get_dtypes` first."
            )
        else:
            return _hash_str(str(sorted(self._table_hashes)))

    @staticmethod
    def _get_data_dtypes(data: pd.DataFrame) -> _Dtypes:
        """Returns the nullable column types of the dataframe.

        This is called by the `get_dtypes` method. This method also overrides datetime
        column dtypes to be strings. This is not done for date columns which are of
        type object.
        """
        data = data.convert_dtypes()
        dtypes: _Dtypes = data.dtypes.to_dict()
        for name in list(dtypes):
            if is_datetime(data[name]):
                dtypes[name] = pd.StringDtype()

        return dtypes

    def load_data(self, **kwargs: Any) -> None:
        """Load the data for the datasource.

        Raises:
            TypeError: If data format is not supported.
        """
        if not self._data_is_loaded and (data := self.get_data(**kwargs)) is not None:
            self.data = data

    @abstractmethod
    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(self, col_name: str, **kwargs: Any) -> _Column:
        """Implement this method to get single column from dataset.

        Used in the `ColumnAverage` algorithm as well as to iterate over image columns
        for the purposes of schema generation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Implement this method to load and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Implement this method to get the number of rows in the dataset."""
        raise NotImplementedError

    @property
    def multi_table(self) -> bool:
        """This returns False if the DataSource does not subclass `MultiTableSource`.

        However, this property must be re-implemented in `MultiTableSource`, therefore
        it is not necessarily True if the DataSource inherits from `MultiTableSource`.
        """
        return False

    @property
    def iterable(self) -> bool:
        """This returns False if the DataSource does not subclass `IterableSource`.

        However, this property must be re-implemented in `IterableSource`, therefore it
        is not necessarily True if the DataSource inherits from `IterableSource`.
        """
        return False


@delegates()
class MultiTableSource(BaseSource, ABC):
    """Abstract base source that supports multiple tables.

    This class is used to define a data source that supports multiple tables. The
    datasources do not necessarily have multiple tables though.
    """

    @property
    @abstractmethod
    def multi_table(self) -> bool:
        """Implement this method to define whether the data source is multi-table.

        The datasource must inherit from `MultiTableSource` if this is True. However,
        the inverse is not necessarily True.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def table_names(self) -> List[str]:
        """Implement this to return a list of table names.

        If there is only one table, it should return a list with one element.
        """
        raise NotImplementedError

    @abstractmethod
    def _validate_table_name(self, table_name: str) -> None:
        """Validate the table name exists in the multi-table datasource.

        This method should raise a ValueError if the table_name is not valid.
        """
        raise NotImplementedError

    @abstractmethod
    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(
        self, col_name: str, table_name: Optional[str] = None, **kwargs: Any
    ) -> _Column:
        """Implement this method to get single column from dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_data(
        self, table_name: Optional[str] = None, **kwargs: Any
    ) -> Optional[pd.DataFrame]:
        """Implement this method to loads and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, table_name: Optional[str] = None, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError


@delegates()
class IterableSource(BaseSource, ABC):
    """Abstract base source that supports iterating over the data.

    This is used for streaming data in batches as opposed to loading the entire dataset
    into memory.

    Args:
        partition_size: The size of each partition when iterating over the data.
    """

    def __init__(
        self,
        partition_size: int = 100,
        **kwargs: Any,
    ) -> None:
        self.partition_size = partition_size
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def iterable(self) -> bool:
        """Implement this method to define whether the data source is iterable.

        The datasource must inherit from `IterableSource` if this is True. However,
        the inverse is not necessarily True.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """This method must return None if the data source is iterable."""
        raise NotImplementedError

    @abstractmethod
    def yield_data(self, **kwargs: Any) -> Iterator[pd.DataFrame]:
        """Implement this method to yield dataframes."""
        raise NotImplementedError


@delegates()
class FileSystemIterableSource(IterableSource, ABC):
    """Abstract base source that supports iterating over file-based data.

    This is used for Iterable data sources that whose data is stored as files on disk.

    Args:
        path: Path to the directory which contains the data files. Subdirectories
            will be searched recursively.
        output_path: The path where to save intermediary output files. Defaults to
            'preprocessed/'.
        iterable: Whether the data source is iterable. This is used to determine
            whether the data source can be used in a streaming context during a task.
            Defaults to False.
        fast_load: Whether the data will be loaded in fast mode. This is used to
            determine whether the data will be iterated over during set up for schema
            generation and splitting (where necessary). Only relevant if `iterable` is
            True, otherwise it is ignored. Defaults to False.
        file_extension: File extension(s) of the data files. If None, all files
            will be searched. Can either be a single file extension or a list of
            file extensions. Case insensitive. Defaults to None.
        strict: Whether File loading should be strictly done on files with the
            explicit file extension provided. If set to True will only load
            those files in the dataset. Otherwise, it will scan the given path
            for files of the same type as the provided file extension. Only
            relevant if `file_extension` is provided. Defaults to False.
    """

    def __init__(
        self,
        path: Union[os.PathLike, str],
        output_path: Optional[Union[os.PathLike, str]] = None,
        iterable: bool = False,
        fast_load: bool = False,
        file_extension: Optional[_SingleOrMulti[str]] = None,
        strict: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._unsanitized_path = path
        self.out_path: Path
        if output_path is None:
            self.out_path = BITFOUNT_CACHE_DIR
        else:
            self.out_path = Path(output_path)
        logger.debug(f"File output path set to {self.out_path}")
        self.out_path.mkdir(exist_ok=True, parents=True)  # create if not exists

        self._iterable = iterable
        self.fast_load = fast_load
        self.file_extension: Optional[List[str]] = None
        if file_extension:
            file_extension_: List[str] = (
                [file_extension]
                if isinstance(file_extension, str)
                else list(file_extension)
            )
            self.file_extension = [
                f".{fe}" if not fe.startswith(".") else fe for fe in file_extension_
            ]

        self.strict = strict if self.file_extension is not None else False
        # This is used to select a subset of file names by the data splitter rather than
        # every file that has been loaded or that is in the directory. In particular,
        # this is used to subset the files for batched execution of a task.
        self.selected_file_names_override: List[str] = []

        # A list of files that have previously been skipped either because of errors or
        # because they don't contain any image data and `images_only` is True. This
        # allows us to skip these files again more quickly if they are still present in
        # the directory.
        self.skipped_files: Set[str] = set()

    @staticmethod
    def _scan_files_for_extension(
        files: List[Path], file_extension: List[str]
    ) -> List[str]:
        """Scans files for the provided file extension.

        Looks for files with same defined or guessed extension as the provided
        file extension.

        Args:
            files: A list of files to scan.

        Returns:
            A list of files with a matching extension.
        """

        # Otherwise, restrict files based on specified file extension.
        ignored_file_types = set()
        number_of_ignored_files = 0
        matched_files: List[Path] = []

        for file in files:
            # Order: file extension, guessed extension
            file_type = file.suffix or f".{guess_extension(file)}"

            # If guessing the extension failed the result is ".None"
            if file_type == ".None":
                logger.warning(
                    f"Could not determine file type of '{file.resolve()}'. Ignoring..."
                )
            elif file_type.lower() not in [x.lower() for x in file_extension]:
                ignored_file_types.add(file_type)
                number_of_ignored_files += 1
            else:
                matched_files.append(file)

        logger.info(
            f"Found {len(matched_files)} files that match file types "
            f"{file_extension}."
        )
        if ignored_file_types:
            logger.info(
                f"Ignoring {number_of_ignored_files} files with file types "
                f"{ignored_file_types}."
            )
        # Fix for shuffling so that data is mapped correctly
        matched_files.sort(key=lambda x: hash(x))
        return [str(x.resolve()) for x in matched_files]

    @property
    def path(self) -> Path:
        """Resolved absolute path to data.

        Provides a consistent version of the path provided by the user
        which should work throughout regardless of operating system
        and of directory structure.
        """
        return Path(self._unsanitized_path).absolute().resolve()

    @property
    def selected_file_names(self) -> List[str]:
        """Returns a list of selected file names."""
        if self.selected_file_names_override:
            return self.selected_file_names_override

        try:
            if len(self.data) == 0:
                filenames = []
            else:
                filenames = list(self.data["_original_filename"])
        except DataNotLoadedError:
            filenames = self.file_names

        return filenames

    def clear_file_names_cache(self) -> None:
        """Clears the list of selected file names.

        This allows the datasource to pick up any new files that have been added to the
        directory since the last time it was cached.
        """
        # This is the specified way to clear the cache on a cached_property
        # https://docs.python.org/3/library/functools.html#functools.cached_property
        try:
            del self.file_names
        except AttributeError:
            # If the file_names property hasn't been accessed yet, it will raise an
            # AttributeError. We can safely ignore this.
            pass

    @cached_property
    def file_names(self) -> List[str]:
        """Returns a list of file names in the directory."""
        if not os.path.exists(self.path):
            logger.warning(
                "The specified path for the datasource was not found. "
                "No files can be loaded."
            )
            return []
        original_files = [x for x in self.path.rglob("*") if x.is_file()]
        files = [x for x in original_files if str(x) not in self.skipped_files]
        # We aren't assuming that all the files in `self.skipped_files`
        # are still present in the directory, so we have to calculate
        # the number of skipped files based on the difference between
        # the original files and the files that have been skipped.
        num_skipped_files = len(original_files) - len(files)
        if num_skipped_files > 0:
            logger.info(f"Skipping {num_skipped_files} files.")

        if self.strict or not self.file_extension:
            if self.file_extension:
                lower_case_file_extensions = [x.lower() for x in self.file_extension]
                files = [
                    x for x in files if x.suffix.lower() in lower_case_file_extensions
                ]
                logger.info(
                    f"Found {len(files)} files with the explicit extensions "
                    f"{self.file_extension}."
                )
            else:
                logger.info(f"Found {len(files)} files.")
            return [str(x.resolve()) for x in files]

        # Only called if self.file_extension is specified and self.strict is False
        return self._scan_files_for_extension(files, self.file_extension)

    @property
    def stale(self) -> bool:
        """Whether the data source is stale.

        This is defined by whether the data is loaded and the number of files matches
        the number of rows in the dataframe.
        """
        if self._data_is_loaded and len(self.data) == len(self.file_names):
            return False

        return True

    @property
    def iterable(self) -> bool:
        """Defines whether the data source is iterable.

        This is defined by the user when instantiating the class.
        """
        return self._iterable

    def _load_data_iteratively(self, **kwargs: Any) -> None:
        """Load data iteratively using `yield_data`.

        This is only applicable for FileSystemIterableSource.
        """
        dfs = []
        for df in self.yield_data(**kwargs):
            dfs.append(df)
        self.data = pd.concat(dfs, axis=0, ignore_index=True)

    @abstractmethod
    def _get_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> pd.DataFrame:
        """Implement to return data corresponding to the provided file names.

        This method is called under the hood by `get_data` and `yield_data`. This
        method must return a dataframe with the columns `_original_filename` and
        `_last_modified" containing the original file name of each row, and the
        timestamp when the file was last modified in ISO 8601 format, respectively.

        Args:
            file_names: List of file names to load. If None, all files should be
                loaded.

        Returns:
            A dataframe containing the data.
        """
        raise NotImplementedError

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in the dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.
            **kwargs: Additional keyword arguments to pass to the `load_data` method
                if the data is stale.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        dic: Dict[str, Iterable[Any]] = {}

        if self.stale:
            self.load_data(**kwargs)

        for col in col_names:
            try:
                dic[col] = self.data[col].unique()
            except TypeError:
                logger.warning(f"Found unhashable value type, skipping column {col}.")
        return dic

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from the dataset.

        Args:
            col_name: The name of the column which should be loaded.
            **kwargs: Additional keyword arguments to pass to the `load_data` method
                if the data is stale.

        Returns:
            The column request as a series.
        """
        if self.stale:
            self.load_data(**kwargs)

        return self.data[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the column names and types of the dataframe.

        If `fast_load` is set to True and the data is stale, only the first file will
        be loaded to get the column names and types. Otherwise, all files will be
        loaded. We only perform this optimisation if the data is stale because if it's
        not, it's faster to just return the dtypes of the already loaded data.

        Args:
            **kwargs: Additional keyword arguments to pass to the `load_data` method
                if the data is stale.

        Returns:
            A mapping from column names to column types.
        """
        if self.stale:
            if self.fast_load:
                data = self._get_data(file_names=[self.file_names[0]], **kwargs)
                return self._get_data_dtypes(data)
            else:
                self.load_data(**kwargs)

        return self._get_data_dtypes(self.data)

    def yield_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> Iterator[pd.DataFrame]:
        """Yields data in batches from files that match the given file names.

        Args:
            file_names: An optional list of file names to use for yielding data.
                Otherwise, all files that have already been found will be used.
                `file_names` is always provided when this method is called from the
                Dataset as part of a task.

        Raises:
            ValueError: If no file names provided and no files have been found.
        """
        if not file_names and not self.file_names:
            logger.warning("No files found to yield data from.")
            # if there are no files, log a warning, and yield from an empty list
            yield self._get_data([])
        file_names = file_names or self.file_names

        for hook in get_hooks(HookType.POD):
            # Signal files partition
            hook.on_files_partition(
                self, total_num_files=len(file_names), batch_size=self.partition_size
            )

        for file_names_partition in self.partition(file_names, self.partition_size):
            file_names_partition = cast(List[str], file_names_partition)
            yield self._get_data(file_names_partition)
            # Delete the files after they have been processed and used
            self._cleanup(file_names_partition)

    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Returns data if the datasource is not iterable, otherwise None.

        We don't reload the data if it has already been loaded. We are assuming that
        files are only added, not removed, meaning we can rely on simply matching the
        number of files detected with the length of the dataframe to ascertain whether
        the data has already been loaded.
        """
        if not self.stale:
            return self.data

        return self._get_data(**kwargs)

    def _recreate_file_structure(self, file_path: str, exist_ok: bool) -> Path:
        """Recreates the file structure in the output directory.

        This is used to ensure that the output directory has the same structure as the
        input directory. This is useful for when the input data is partitioned into
        subdirectories.

        Args:
            file_path: The file name to recreate the structure for.
            exist_ok: Whether to raise an error if the directory already exists.

        Returns:
            The path to the recreated file structure.

        Raises:
            FileExistsError: If the subdir already exists in the output directory and
                `exist_ok` is False.
        """
        path = Path(file_path)
        file_id = path.stem + FILE_SYSTEM_ITERABLE_IMAGE_CACHE_SUFFIX
        parent_path = path.parent.absolute()
        # Relative path gets the path of the original file relative to the specified
        # input path. This relative path is then used to recreate the file structure
        # in the output directory with the original filename being used as a
        # subdirectory instead containing any relevant extracted files.
        relative_path = parent_path.relative_to(self.path)
        save_prefix = self.out_path / relative_path / file_id
        save_prefix.mkdir(parents=True, exist_ok=exist_ok)
        return save_prefix

    def _cleanup(self, file_names: List[str]) -> None:
        """Remove intermediate files creating during yielding of partitions.

        Intended to be called by `yield_data` every partition.
        """
        for file_name in file_names:
            save_dir = self._recreate_file_structure(file_name, exist_ok=True)
            shutil.rmtree(save_dir)

    @staticmethod
    def partition(iterable: Sequence, partition_size: int = 1) -> Iterable:
        """Takes an iterable and yields partitions of size `partition_size`.

        The final partition may be less than size `partition_size` due to the variable
        length of the iterable.
        """
        len_ = len(iterable)
        for partition_start_idx in range(0, len_, partition_size):
            yield iterable[
                partition_start_idx : min(partition_start_idx + partition_size, len_)
            ]

    def _fast_load_data(self, **kwargs: Any) -> None:
        """Load the data in fast mode.

        Loads a small random subset of the data to speed up the process of schema
        generation. The number of files loaded is determined by the number of files
        in the directory and the variability of the data. The more unique fields that
        get discovered with each file, the more files will be loaded.
        """
        # We don't want to load too many or too few files, so we aim for a small
        # percentage of the total number of files, but with a minimum and maximum
        # number of files which overrides the percentage if the number of files falls
        # outside of the range.
        minimum_number_of_files_without_new_fields = np.clip(
            FAST_LOAD_NUMBER_OF_FILES_PERCENTAGE * len(self.file_names),
            FAST_LOAD_MINIMUM_NUMBER_OF_FILES_WITHOUT_NEW_FIELDS,
            FAST_LOAD_MAXIMUM_NUMBER_OF_FILES_WITHOUT_NEW_FIELDS,
        )
        minimum_number_of_files_without_new_fields = int(
            min(minimum_number_of_files_without_new_fields, len(self.file_names))
        )
        logger.debug(
            "Minimum number of files without new fields is "
            f"{minimum_number_of_files_without_new_fields}"
        )
        sampled_file_names = random.sample(
            self.file_names,
            # Ensure we don't attempt to sample more files than there are in the
            # directory.
            min(len(self.file_names), FAST_LOAD_MAXIMUM_NUMBER_OF_FILES_TO_LOAD),
        )
        number_of_files_without_new_fields = 0
        num_files_processed = 0
        unique_fields: Set[str] = set()
        dfs = []
        for file in sampled_file_names:
            df = self._get_data(file_names=[file], **kwargs)
            if len(set(df.columns).difference(unique_fields)) == 0:
                number_of_files_without_new_fields += 1
            else:
                number_of_files_without_new_fields = 0

            unique_fields.update(df.columns)
            dfs.append(df)
            num_files_processed += 1
            if (
                number_of_files_without_new_fields
                >= minimum_number_of_files_without_new_fields
            ):
                break

        logger.info(f"Loaded {num_files_processed} files using fast load.")
        if (
            number_of_files_without_new_fields
            < minimum_number_of_files_without_new_fields
        ) and len(sampled_file_names) < len(self.file_names):
            logger.warning(
                "Schema generation may be inaccurate. "
                f"Loaded {num_files_processed} files "
                f"but didn't reach {minimum_number_of_files_without_new_fields} "
                "consecutive files without finding new fields."
            )

        self.data = pd.concat(dfs, axis=0, ignore_index=True)

    def load_data(self, **kwargs: Any) -> None:
        """Load the data for the datasource.

        Args:
            **kwargs: Keyword arguments to be passed to underlying functions.

        Raises:
            TypeError: If data format is not supported.
        """
        if not self.stale:
            return

        # If a task is running, we don't care about fast load, we just load the data
        # normally.
        if self.fast_load and not self.is_task_running:
            if self._data_is_loaded:
                # If the data is already loaded, we don't need to load it again.
                return
            self._fast_load_data(**kwargs)
            return

        if self.iterable:
            self._load_data_iteratively(**kwargs)
        elif (data := self.get_data(**kwargs)) is not None:
            self.data = data

    def __len__(self) -> int:
        return len(self.selected_file_names)


@delegates()
class FileSystemIterableSourceInferrable(FileSystemIterableSource, ABC):
    """Abstract base source that supports iterating over file-based data.

    This is used for Iterable data sources that whose data is stored as files on disk.

    Args:
        path: Path to the directory which contains the data files. Subdirectories
            will be searched recursively.
        infer_class_labels_from_filepaths: Whether class labels should be
            added to the data based on the filepath of the files.
            Defaults to the first directory within self.path,
            but can go a level deeper if the datasplitter is provided
            with `infer_data_split_labels` set to true
    """

    _first_directory_in_path: Final[str] = "_first_directory"
    _second_directory_in_path: Final[str] = "_second_directory"
    _unused_directory_in_path: Final[str] = "_unused_path_segment"

    def __init__(
        self,
        path: Union[os.PathLike, str],
        infer_class_labels_from_filepaths: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(path=path, **kwargs)
        self.infer_class_labels_from_filepaths = infer_class_labels_from_filepaths

    def _get_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> pd.DataFrame:
        """Returns data corresponding to the provided file names.

        Args:
            file_names: List of file names to load. If None, all files should be
                loaded.

        Returns:
            A dataframe containing the data.
        """
        processed_data_list: List[Dict[str, Any]] = []
        if file_names:
            full_data = False
        else:
            file_names = self.file_names
            # Check if data is stale
            full_data = not self.stale

        total_num_files = len(file_names)

        for hook in get_hooks(HookType.POD):
            # Signal file processing start
            hook.on_file_process_start(
                self, file_num=0, total_num_files=total_num_files
            )

        for i, filename in enumerate(file_names):
            logger.info(f"Processing file {filename}...")
            processed_data = self._process_file(filename, full_data, **kwargs)

            # Signal file finished processing
            for hook in get_hooks(HookType.POD):
                hook.on_file_process_end(
                    self, file_num=i + 1, total_num_files=total_num_files
                )
            if processed_data:
                # File has not been skipped and is not empty,
                # so we can add some metadata
                # columns and append it to the list of data points.
                for row in processed_data:
                    processed_data_with_metadata = self._add_metadata_to_data(
                        row, filename
                    )
                    processed_data_list.append(processed_data_with_metadata)

        if len(processed_data_list) == 0:
            logger.warning("No files could be loaded.")
        # We don't want to log when we're just loading a single file because this is
        # not a meaningul log message as sometimes we iterate through all the files
        # one by one calling this method.
        elif len(processed_data_list) > 1:
            logger.info(f"{len(processed_data_list)} files loaded successfully.")

        # Create the dataframe
        df = pd.DataFrame.from_records(processed_data_list)

        # Perform any subclass defined processing of the dataframe
        df = self._process_dataset(df, **kwargs)
        infer_data_split_column_name = (
            self.data_splitter.column_name
            if isinstance(self.data_splitter, SplitterDefinedInData)
            and self.data_splitter.infer_data_split_labels
            else False
        )

        unique_first_directory_values: List[str] = []
        unique_second_directory_values: List[str] = []

        if self.infer_class_labels_from_filepaths or infer_data_split_column_name:
            # We need to extract unique value from the first and second directory
            # so we can differentiate between the split and the label directories.
            if self._first_directory_in_path in df.columns:
                unique_first_directory_values = (
                    df[self._first_directory_in_path].unique().tolist()
                )
            if self._second_directory_in_path in df.columns:
                unique_second_directory_values = (
                    df[self._second_directory_in_path].unique().tolist()
                )
            inferred_label_column_name = (
                BITFOUNT_INFERRED_LABEL_COLUMN
                if self.infer_class_labels_from_filepaths
                else self._unused_directory_in_path
            )
            if infer_data_split_column_name:
                # infer_data_split_column_name will *only* be
                # True for SplitterDefinedInData
                self.data_splitter = cast(SplitterDefinedInData, self.data_splitter)
                # We need to extract the split labels from the
                # data splitter for SplitterDefinedInData
                datasplitter_labels = [
                    self.data_splitter.training_set_label.lower(),
                    self.data_splitter.validation_set_label.lower(),
                    self.data_splitter.test_set_label.lower(),
                ]
                # We need to identify which column is the data split labels
                # We'll then mark the other directory as the inferred labels
                if unique_first_directory_values and set(
                    [i.lower() for i in unique_first_directory_values]
                ).issubset(datasplitter_labels):
                    logger.info(
                        f"`{self._first_directory_in_path}` column contains "
                        f"data split labels. "
                        "Inferring class labels from second directory"
                    )
                    df = df.rename(
                        columns={
                            self._first_directory_in_path: infer_data_split_column_name,  # noqa: B950
                            self._second_directory_in_path: inferred_label_column_name,
                        },
                    )
                elif unique_second_directory_values and set(
                    [i.lower() for i in unique_second_directory_values]
                ).issubset(datasplitter_labels):
                    df = df.rename(
                        columns={
                            self._first_directory_in_path: inferred_label_column_name,
                            self._second_directory_in_path: infer_data_split_column_name,  # noqa: B950
                        },
                    )
            else:
                # We only need the class labels
                df = df.rename(
                    columns={
                        self._first_directory_in_path: inferred_label_column_name,
                    },
                )

        # Drop any intermediate columns that aren't needed
        df = df.drop(
            columns=[
                self._first_directory_in_path,
                self._second_directory_in_path,
                self._unused_directory_in_path,
            ],
            errors="ignore",
        )
        if self._data_is_loaded and full_data:
            # If the data is already loaded, and we want all the data, we append the new
            # data to the existing dataframe.
            return pd.concat([self.data, df], axis=0, ignore_index=True)
        return df

    @abstractmethod
    def _process_file(
        self,
        filename: str,
        full_data: bool,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """Implement to process a single file.

        Files may contain more than one datapoint, so this function can return a list
        of dictionaries.

        Args:
            filename: The name of the file to process.
            full_data: True if we're loading all data and want to append to existing
                data.

        """
        raise NotImplementedError

    @abstractmethod
    def _process_dataset(self, dataframe: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        """This method can be overridden to perform any processing of the dataset."""
        raise NotImplementedError

    def _add_metadata_to_data(
        self, data: Dict[str, Any], filename: str
    ) -> Dict[str, Any]:
        """Adds metadata to the data.

        Args:
            data: The data to add metadata to.
            filename: The filename of the file to be processed.

        Returns:
            The data with metadata added.
        """
        data["_original_filename"] = filename
        modify_time = os.path.getmtime(filename)
        data["_last_modified"] = datetime.fromtimestamp(modify_time).isoformat()
        # Track the first two directory levels so that we can easily
        # process the possible labels later on as needed
        relative_filepath = Path(filename).relative_to(self.path).parts
        if len(relative_filepath) > 1:
            data[self._first_directory_in_path] = relative_filepath[0]
        if len(relative_filepath) > 2:
            data[self._second_directory_in_path] = relative_filepath[1]

        return data
