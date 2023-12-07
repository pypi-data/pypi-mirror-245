import os
import pathlib
import sys
import importlib.util


def try_import_mara_config():
    """Tries to find and import a `mara_config.py` file."""
    if 'mara_config' in sys.modules:
        print("A module with name 'mara_config' is already imported.", file=sys.stderr)
        return

    mara_config_path = pathlib.Path(os.environ.get('MARA_CONFIG', ''))

    if mara_config_path.is_dir():
        mara_config_path = mara_config_path / 'mara_config.py'

    if not mara_config_path.exists():
        # the mara_config file does not exist in the config path
        return

    try:
        spec = importlib.util.spec_from_file_location('mara_config', location=mara_config_path.absolute())
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Could not import mara_config.py file '{mara_config_path.absolute()}'") from e
