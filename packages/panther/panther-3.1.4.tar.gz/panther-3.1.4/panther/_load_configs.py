import ast
import os
import platform
import sys
from datetime import timedelta
from importlib import import_module
from pathlib import Path

from pydantic._internal._model_construction import ModelMetaclass

from panther._utils import import_class
from panther.configs import JWTConfig, config
from panther.exceptions import PantherException
from panther.middlewares import BaseMiddleware
from panther.routings import finalize_urls, flatten_urls
from panther.throttling import Throttling

__all__ = (
    'load_configs_file',
    'load_secret_key',
    'load_monitoring',
    'load_log_queries',
    'load_background_tasks',
    'load_throttling',
    'load_default_cache_exp',
    'load_middlewares',
    'load_user_model',
    'load_authentication_class',
    'load_jwt_config',
    'collect_all_models',
    'load_urls',
    'load_panel_urls',
)


def load_configs_file(_configs, /) -> dict:
    """Read the config file and put it as dict in self.configs"""
    if _configs:
        _module = sys.modules[_configs]
    else:
        try:
            _module = import_module('core.configs')
        except ModuleNotFoundError:
            raise _exception_handler(field='core/configs.py', error='Not Found')
    return _module.__dict__


def load_secret_key(configs: dict, /) -> bytes | None:
    if secret_key := configs.get('SECRET_KEY'):
        return secret_key.encode()
    return secret_key


def load_monitoring(configs: dict, /) -> bool:
    return configs.get('MONITORING', config['monitoring'])


def load_log_queries(configs: dict, /) -> bool:
    return configs.get('LOG_QUERIES', config['log_queries'])


def load_background_tasks(configs: dict, /) -> bool:
    return configs.get('BACKGROUND_TASKS', config['background_tasks'])


def load_throttling(configs: dict, /) -> Throttling | None:
    return configs.get('THROTTLING', config['throttling'])


def load_default_cache_exp(configs: dict, /) -> timedelta | None:
    return configs.get('DEFAULT_CACHE_EXP', config['default_cache_exp'])


def load_middlewares(configs: dict, /) -> list:
    """Collect The Middlewares & Set db_engine If One Of Middlewares Was For DB"""
    middlewares = []

    for path, data in configs.get('MIDDLEWARES', []):
        if path.find('panther.middlewares.db.DatabaseMiddleware') != -1:
            config['db_engine'] = data['url'].split(':')[0]
        try:
            Middleware = import_class(path)  # noqa: N806
        except AttributeError:
            raise _exception_handler(field='MIDDLEWARES', error=f'{path} is not a valid middleware path')

        if not issubclass(Middleware, BaseMiddleware):
            raise _exception_handler(field='MIDDLEWARES', error='is not a sub class of BaseMiddleware')

        middlewares.append(Middleware(**data))  # noqa: Py Argument List
    return middlewares


def load_user_model(configs: dict, /) -> ModelMetaclass:
    return import_class(configs.get('USER_MODEL', 'panther.db.models.BaseUser'))


def load_authentication_class(configs: dict, /) -> ModelMetaclass | None:
    return configs.get('AUTHENTICATION') and import_class(configs['AUTHENTICATION'])


def load_jwt_config(configs: dict, /) -> JWTConfig | None:
    """Only Collect JWT Config If Authentication Is JWTAuthentication"""
    if getattr(config['authentication'], '__name__', None) == 'JWTAuthentication':
        user_config = configs.get('JWTConfig', {})
        if 'key' not in user_config:
            user_config['key'] = config['secret_key'].decode()

        return JWTConfig(**user_config)
    return None


def collect_all_models() -> list[dict]:
    """Collecting all models for panel APIs"""
    from panther.db.models import Model

    collected_models = []

    for root, _, files in os.walk(config['base_dir']):
        # Traverse through each directory
        for f in files:
            # Traverse through each file of directory
            if f == 'models.py':
                slash = '\\' if platform.system() == 'Windows' else '/'

                # If the file was "models.py" read it
                file_path = f'{root}{slash}models.py'
                with Path(file_path).open() as file:
                    # Parse the file with ast
                    node = ast.parse(file.read())
                    for n in node.body:
                        # Find classes in each element of files' body
                        if type(n) is ast.ClassDef and n.bases:
                            class_path = (
                                file_path.removesuffix(f'{slash}models.py')
                                .removeprefix(f'{config["base_dir"]}{slash}')
                                .replace(slash, '.')
                            )
                            # We don't need to import the package classes
                            if class_path.find('site-packages') == -1:
                                # Import the class to check his parents and siblings
                                klass = import_class(f'{class_path}.models.{n.name}')

                                collected_models.extend(
                                    [
                                        {
                                            'name': n.name,
                                            'path': file_path,
                                            'class': klass,
                                            'app': class_path.split('.'),
                                        }
                                        for parent in klass.__mro__
                                        if parent is Model
                                    ]
                                )
    return collected_models


def load_urls(configs: dict, /, urls: dict | None) -> tuple[dict, dict]:
    """
    Return tuple of all urls (as a flat dict) and (as a nested dict)
    """
    if isinstance(urls, dict):
        collected_urls = flatten_urls(urls)
        return collected_urls, finalize_urls(collected_urls)

    if (url_routing := configs.get('URLs')) is None:
        raise _exception_handler(field='URLs', error='is required.')

    if isinstance(url_routing, dict):
        error = (
            "can't be 'dict', you may want to pass it's value directly to Panther(). " 'Example: Panther(..., urls=...)'
        )
        raise _exception_handler(field='URLs', error=error)

    if not isinstance(url_routing, str):
        error = 'should be dotted string.'
        raise _exception_handler(field='URLs', error=error)

    try:
        imported_urls = import_class(url_routing)
    except ModuleNotFoundError as e:
        raise _exception_handler(field='URLs', error=e)

    if not isinstance(imported_urls, dict):
        raise _exception_handler(field='URLs', error='should point to a dict.')

    collected_urls = flatten_urls(imported_urls)
    return collected_urls, finalize_urls(collected_urls)


def load_panel_urls() -> dict:
    from panther.panel.urls import urls

    return finalize_urls(flatten_urls(urls))


def _exception_handler(field: str, error: str | Exception) -> PantherException:
    return PantherException(f"Invalid '{field}': {error}")
