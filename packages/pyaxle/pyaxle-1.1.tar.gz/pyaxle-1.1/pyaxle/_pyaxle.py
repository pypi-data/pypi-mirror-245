import ctypes
from os import getcwd, path, getuid, mkdir, system
from shutil import rmtree
from threading import Thread

_PARENT_DIR = getcwd()
_VERBOSE = False

def _VERBOSE_PRINT(text, end="\n"):
    if _VERBOSE:
        print(text, end=end)

def enable_verbose():
    """
    Enable verbose mode.

    We can change the `_VERBOSE` variable in `_pyaxle.py`
    (pyaxle module folder) to `True` to enable verbose mode.

    Note: You can call this function again to disable
    verbose mode.
    """

    global _VERBOSE

    _VERBOSE = not _VERBOSE

    if _VERBOSE:
        print("Verbose mode enabled.")
    else:
        print("Verbose mode disabled.")

def create_axle(_AXLE_DATA, _AXLE_DIR="axles"):
    """
    Create axle.

    This needs administrative access to make the
    axles in the axle directory read only.

    `_AXLE_DATA` needs to be iterable, e.g., a list
    or tuple.
    `_AXLE_DIR` will contain all the axles. The
    default is `axles`.

    The data needs to contain python code, or a
    python file that contains python code.

    Note: If `_AXLE_DIR` already exists, it will
    overwrite it.
    """

    if type(_AXLE_DATA) != list:
        _VERBOSE_PRINT(f"\33[0;49;91mError: '{_AXLE_DATA}' is not a list.\33[0;49;39m")

    _VERBOSE_PRINT(f"========= Creating axle  =========")
    _VERBOSE_PRINT("Checking for administrative access...", end="\r")
    try:
        # For Unix systems
        _is_admin = (getuid() == 0)
    except AttributeError:
        # For (almost all) Windows systems
        _is_admin = (ctypes.windll.shell32.IsUserAnAdmin() != 0)
    if _is_admin: _VERBOSE_PRINT("Checking for administrative access... \33[0;49;92myes\33[0;49;39m")
    else:
        _VERBOSE_PRINT("Checking for administrative access... \33[0;49;91mno\33[0;49;39m")
        print("\33[0;49;91mError: No administrative access!\33[0;49;39m")
        exit(1)

    _VERBOSE_PRINT(f"Axel directory: {_AXLE_DIR}")
    if not path.isdir(_AXLE_DIR):
        mkdir(_AXLE_DIR)
        _VERBOSE_PRINT("Made the axel directory.")
    else:
        print(f"\33[1;49;97mThe axle directory already exists! Would you like to overwrite it?\nNote: This action may not be irreversible, make sure the directory does not contain any critical system files!\33[0;49;39m")
        _option = input("[y/n] ")
        if _option.lower() in ["y", ""]:
            rmtree(_AXLE_DIR)
            mkdir(_AXLE_DIR)
        else:
            return 0

    _output_string = "Axle data: \33[0;49;92m"
    for _obj in _AXLE_DATA:
        if _obj != max(_AXLE_DATA):
            _output_string += f"{_obj}, "
        else:
            _output_string += f"{_obj}\33[0;49;39m"
    _VERBOSE_PRINT(_output_string)
    
    for _index, _data in enumerate(_AXLE_DATA):
        _VERBOSE_PRINT(f"Creating axle #{(_index + 1)}...", end="\r")
        mkdir(f"{_AXLE_DIR}/axle{(_index + 1)}")
        if type(_data) == str:
            with open(f"{_AXLE_DIR}/axle{(_index + 1)}/axle_data.py", "w") as _file:
                if not path.isfile(_data):
                    _file.write(_data)
                else:
                    _write = open(_data).read()
                    _file.write(_write)
        else:
            print(f"\33[0;49;91mUnable to create axle #{(_index + 1)}! Axle data (index of {_index}) needs to be a string.\33[0;49;39m")
        _VERBOSE_PRINT(f"Creating axle #{(_index + 1)}... done")

def _RUN(_PYTHON_FILE):
    system(f"python3 {_PYTHON_FILE}")

def run_axle(_AXLE_NUM, _AXLE_DIR="axles", _RUN_IN_THREAD=True):
    """
    Run an axle.

    `_AXLE_NUM` needs to be an available axle
    number.
    `_AXLE_DIR` needs to be an available axle
    directory. It's `axles` by default.

    If you make `_RUN_IN_THREAD` to `True`
    (which it is by default), it will run it
    in a thread.
    """

    _VERBOSE_PRINT(f"====== Running axle #{_AXLE_NUM} ======")

    if not path.isdir(_AXLE_DIR):
        print(f"\33[0;49;91mError: Axel directory ({_AXLE_DIR}) does not exist.\33[0;49;39m")
    if not path.isfile(f"{_AXLE_DIR}/axle{_AXLE_NUM}"):
        print(f"\33[0;49;91mError: Axel number ({_AXLE_NUM}) does not exist.\33[0;49;39m")

    if _RUN_IN_THREAD:
        _VERBOSE_PRINT("Running in thread...")
        _thread = Thread(target=_RUN, args=(f"{_AXLE_DIR}/axle{_AXLE_NUM}/axle_data.py",))
        _thread.start()
        _thread.join()
        _VERBOSE_PRINT("Thread finished.")
    else:
        _VERBOSE_PRINT("Just running...")
        _RUN(f"{_AXLE_DIR}/axle{_AXLE_NUM}/axle_data.py")
        _VERBOSE_PRINT("Finished.")

def delete_axle(_AXLE_NUM=1, _AXLE_DIR="axles", _DELETE_ALL=False):
    """
    Deletes an axle.

    This needs administrative permissions.
    (Remember, the axle files are read
    only)

    `_AXLE_NUM` needs to be an available axle
    number, but it doesn't matter if you set
    `_DELETE_ALL` to `True` (which it is by
    default). It's `1` by default.
    `_AXLE_DIR` needs to be an available axle
    directory. It's `axles` by default.
    """

    _VERBOSE_PRINT("====== Deleting axles ======")
    _VERBOSE_PRINT("Checking for administrative access...", end="\r")
    try:
        # For Unix systems
        _is_admin = (getuid() == 0)
    except AttributeError:
        # For (almost all) Windows systems
        _is_admin = (ctypes.windll.shell32.IsUserAnAdmin() != 0)
    if _is_admin:
        _VERBOSE_PRINT("Checking for administrative access... \33[0;49;92myes\33[0;49;39m")
    else:
        _VERBOSE_PRINT("Checking for administrative access... \33[0;49;91mno\33[0;49;39m")
        print("\33[0;49;91mError: No administrative access!\33[0;49;39m")
        exit(1)

    if not path.isdir(_AXLE_DIR):
        print(f"\33[0;49;91mError: Axle directory '{_AXLE_DIR}' doesn't exist.\33[0;49;39m")
        exit(1)
    if not path.isfile(f"{_AXLE_DIR}/axle{_AXLE_NUM}") and not _DELETE_ALL:
        print(f"\33[0;49;91mError: Axel number ({_AXLE_NUM}) does not exist.\33[0;49;39m")

    print(f"\33[1;49;97mAre you sure you want to do this?\nNote: This action may not be irreversible!\33[0;49;39m")
    _option = input("[y/n] ")
    if not _option.lower() in ["y", ""]:
        return 0

    if _DELETE_ALL:
        rmtree(_AXLE_DIR)
    else:
        rmtree(f"{_AXLE_DIR}/axle{_AXLE_NUM}")