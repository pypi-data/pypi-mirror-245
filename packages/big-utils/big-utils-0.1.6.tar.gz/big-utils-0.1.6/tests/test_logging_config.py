"""
Logging configuration unit tests.
"""
import json
import logging
import logging.config
import pytest
from big_utils.config import configure_logging

TEST_LOGGING_CONFIG_1 = {
    "logging": {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "single-line": {
                "class": "logging.Formatter",
                "format": "%(asctime)s [%(levelname)s - %(name)s]: %(message)s"
            },
            "single-line-detailed": {
                "class": "logging.Formatter",
                "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s - %(name)s]: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "single-line",
                "stream": "ext://sys.stdout"
            },
            "console-detailed": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "single-line-detailed",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "test1": {
                "level": "DEBUG"
            },
            "test2": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False
            },
            "test3": {
                "level": "WARN"
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO"
        }
    }
}

TEST_LOGGING_CONFIG_2 = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "single-line": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(levelname)s - %(name)s]: %(message)s"
        },
        "single-line-detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s - %(name)s]: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "single-line",
            "stream": "ext://sys.stdout"
        },
        "console-detailed": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "single-line-detailed",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "test1": {
            "level": "DEBUG"
        },
        "test2": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        },
        "test3": {
            "level": "WARN"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

TEST_LOGGING_CONFIG_YAML_WITH_ROOT = """
logging:
  version: 1
  disable_existing_loggers: true

  formatters:
    single-line:
      class: "logging.Formatter"
      format: "%(asctime)s [%(levelname)s - %(name)s]: %(message)s"

    single-line-detailed:
      class: "logging.Formatter"
      format: "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s - %(name)s]: %(message)s"

  handlers:
    console:
      level: "DEBUG"
      class: "logging.StreamHandler"
      formatter: "single-line"
      "stream": "ext://sys.stdout"

    console-detailed:
      level: "DEBUG"
      class: "logging.StreamHandler"
      formatter: "single-line-detailed"
      stream: "ext://sys.stdout"

  loggers:
    test1:
      level: "DEBUG"

    test2:
      handlers: [ "console" ]
      level: "DEBUG"
      propagate: False

    test3:
      level: "WARN"

    sqlalchemy.engine.base.Engine:
      level: "WARN"

  root:
    handlers: [ "console" ]
    level: "INFO"
"""

TEST_LOGGING_CONFIG_YAML_NO_ROOT = """
version: 1
disable_existing_loggers: true

formatters:
  single-line:
    class: "logging.Formatter"
    format: "%(asctime)s [%(levelname)s - %(name)s]: %(message)s"

  single-line-detailed:
    class: "logging.Formatter"
    format: "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s - %(name)s]: %(message)s"

handlers:
  console:
    level: "DEBUG"
    class: "logging.StreamHandler"
    formatter: "single-line"
    "stream": "ext://sys.stdout"

  console-detailed:
    level: "DEBUG"
    class: "logging.StreamHandler"
    formatter: "single-line-detailed"
    stream: "ext://sys.stdout"

loggers:
  test1:
    level: "DEBUG"

  test2:
    handlers: [ "console" ]
    level: "DEBUG"
    propagate: False

  test3:
    level: "WARN"

  sqlalchemy.engine.base.Engine:
    level: "WARN"

root:
  handlers: [ "console" ]
  level: "INFO"
"""


@pytest.fixture
def logging_config_file_1(tmp_path):
    cfg_file = tmp_path.joinpath('logging.json')
    cfg_file.write_text(json.dumps(TEST_LOGGING_CONFIG_1))
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def logging_config_file_2(tmp_path):
    cfg_file = tmp_path.joinpath('logging.json')
    cfg_file.write_text(json.dumps(TEST_LOGGING_CONFIG_2))
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def logging_config_yaml_file_with_root(tmp_path):
    cfg_file = tmp_path.joinpath('logging.yaml')
    cfg_file.write_text(TEST_LOGGING_CONFIG_YAML_WITH_ROOT)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def logging_config_yaml_file_no_root(tmp_path):
    cfg_file = tmp_path.joinpath('logging.yaml')
    cfg_file.write_text(TEST_LOGGING_CONFIG_YAML_NO_ROOT)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


def __common_logging_cfg_test():
    """Shared test implementation"""
    logger = logging.getLogger('test1')

    assert logger.level == logging.DEBUG
    assert logger.propagate is True

    logger = logging.getLogger('test2')
    assert logger.level == logging.DEBUG
    assert len(logger.handlers)
    assert logger.propagate is False

    logger = logging.getLogger('test3')
    assert logger.level == logging.WARN

    # root logger
    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO
    assert len(root_logger.handlers) == 1


def test_config_logging_json_file_with_root(logging_config_file_1):
    configure_logging(logging_config_file_1)
    __common_logging_cfg_test()


def test_config_logging_json_file_without_root(logging_config_file_2):
    configure_logging(logging_config_file_2)
    __common_logging_cfg_test()


def test_config_logging_yaml_file_with_root(logging_config_yaml_file_with_root):
    configure_logging(logging_config_yaml_file_with_root)
    __common_logging_cfg_test()


def test_config_logging_yaml_file_without_root(logging_config_yaml_file_no_root):
    configure_logging(logging_config_yaml_file_no_root)
    __common_logging_cfg_test()
