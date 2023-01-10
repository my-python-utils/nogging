#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read `nogging.yaml` from of __main__ or its parent(...) folder,
if none found, do nothing.
if one found, use it to config loggers.

for example:
```yaml
# nogging.yaml
debug: &debug
  level: DEBUG
  handlers:
    - type: StreamHandler
      level: DEBUG
      format: "%(asctime)s | %(thread)d | %(name)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s"
info: &info
  level: INFO
  handlers:
    - type: StreamHandler
      level: INFO
      format: "%(asctime)s | %(thread)d | %(name)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s"
warning: &warning
  level: WARNING
  handlers:
    - type: StreamHandler
      level: WARNING
      format: "%(asctime)s | %(thread)d | %(name)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s"
error: &error
  level: ERROR
  handlers:
    - type: StreamHandler
      level: ERROR
      format: "%(asctime)s | %(thread)d | %(name)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s"

nogging:
  __main__:
    <<: *debug
  myconfig.gui.main:
    <<: *debug
  myconfig.threads:
    <<: *error
```
"""
import functools
import logging
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import yaml

APP = 'nogging'


def log(*args) -> None:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    thread = threading.get_ident()
    return functools.partial(print, now, thread, __name__, sep=' | ')(*args)


def conf(path: str, c=f'{APP}.yaml', key: str = 'nogging') -> Optional[dict]:
    p = Path(path).absolute()
    while p.parent != p:
        if (p / c).exists():
            log('INFO', f'using config file "{(p / c).as_posix()}"')
            break
        p = p.parent
    else:
        log('WARNING', f'"{c}" not found!')
    try:
        return yaml.safe_load((p / c).open())[key]
    except FileNotFoundError:
        ...
    except KeyError:
        log('ERROR', f'format error! Key "{key}" not found.')


class Nogging(object):
    def setup(self, path: str = '.') -> None:
        for k, v in (conf(path) or {}).items():
            self._setup_logger(name=k, config=v)

    def _setup_logger(self, name: str, config: dict) -> None:
        logger = logging.getLogger(name)
        # setup level
        level = self._get_level(config)
        if level is not None:
            logger.setLevel(level)

        # setup handler
        handlers = self._get_handlers(config)
        if handlers is not None:
            for _ in logger.handlers:
                logger.removeHandler(_)

            for handler_config in handlers or []:
                handler = self._get_handler(handler_config)
                if handler is None:
                    continue

                formatter = self._get_handler_formatter(handler_config)
                if formatter is not None:
                    handler.setFormatter(formatter)

                level = self._get_level(handler_config)
                if level is not None:
                    handler.setLevel(level)

                logger.addHandler(handler)

    @staticmethod
    def _get_level(handler_config: dict) -> Optional[int]:
        if 'level' in handler_config:
            level: Union[int, str] = handler_config['level']

            if isinstance(level, str):
                level: int = getattr(logging, level)

            return level

    @staticmethod
    def _get_handlers(handler_config: dict) -> Optional[list]:
        if 'handlers' in handler_config:
            handlers: Union[list, None] = handler_config['handlers']

            return handlers

    @staticmethod
    def _get_handler(handler_config: dict) -> Optional[logging.StreamHandler]:
        handler = None
        handler_type = handler_config['type']
        if handler_type == 'FileHandler':
            handler = logging.FileHandler(
                filename=handler_config['filename'],
                encoding='utf-8',
            )
        elif handler_type == 'StreamHandler':
            handler = logging.StreamHandler(sys.stdout)
        else:
            log('WARNING', f'invalid handler type "{handler_type}"!')
        return handler

    @staticmethod
    def _get_handler_formatter(handler_config: dict) -> Optional[logging.Formatter]:
        if 'format' in handler_config:
            return logging.Formatter(handler_config['format'])


if __name__ == '__main__':
    Nogging().setup()
