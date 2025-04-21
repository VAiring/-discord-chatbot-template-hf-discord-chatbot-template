import importlib
import logging
import pkgutil
from typing import List, Callable, Optional


def load_commands(package_name: str) -> List[Callable]:
    """指定されたパッケージ内のすべてのコマンドを動的にロード"""
    logging.info(f"Loading commands from package: {package_name}")
    commands: List[Callable] = []
    try:
        package = importlib.import_module(package_name)
        package_path = package.__path__  # パッケージのパスを取得
        for _, module_name, _ in pkgutil.iter_modules(package_path):
            logging.info(f"Attempting to load module: {module_name}")
            command = _load_command(package_name, module_name)
            if command:
                logging.info(f"Successfully loaded command from module: {module_name}")
                commands.append(command)
            else:
                logging.warning(f"No command found in module: {module_name}")
    except Exception as e:
        logging.error(f"Failed to load package '{package_name}': {e}", exc_info=True)
    return commands


def _load_command(package_name: str, module_name: str) -> Optional[Callable]:
    """指定されたモジュールからコマンドをロード"""
    try:
        module = _import_module(package_name, module_name)
        if hasattr(module, "register_command"):
            logging.info(f"Found 'register_command' in module: {module_name}")
            return module.register_command
        else:
            logging.warning(f"'register_command' not found in module: {module_name}")
    except Exception as e:
        logging.error(
            f"Failed to load command from module '{module_name}' in package '{package_name}': {e}",
            exc_info=True,
        )
    return None


def _import_module(package_name: str, module_name: str):
    """モジュールをインポート"""
    logging.info(f"Importing module: {package_name}.{module_name}")
    return importlib.import_module(f"{package_name}.{module_name}")
