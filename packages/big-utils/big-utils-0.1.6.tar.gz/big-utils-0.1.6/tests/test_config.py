"""
Config module unit tests
"""
import pytest
from pathlib import Path
from dataclasses import dataclass, field
from dacite import MissingValueError
from typing import Optional
from big_utils.config.config import (
    load_from_ini_file,
    load_from_json_file,
    load_from_toml_file,
    load_from_yaml_file,
    load_from_properties_file,
    load_config_from_file,
    str2bool_converter,
    Configurator,
    StandardStrategy
)

TEST_DATA_INI = """
[DEFAULT]
TEST = True

[APP]
ENVIRONMENT = development
DEBUG = False

[DATABASE]
USERNAME = root1
PASSWORD = p@ssw0rd
HOST = 127.0.0.1
PORT = 5432
DB = my_database1
TEST = False

[LOGS]
ERRORS: logs/errors.log
INFO = data/info.log

[FILES]
STATIC_FOLDER: static
TEMPLATES_FOLDER = templates
"""

TEST_DATA_JSON = """
{
  "DEFAULT": {
    "TEST": true
  },
  "APP": {
    "ENVIRONMENT": "development",
    "DEBUG": false
  },
  "DATABASE": {
    "USERNAME": "root2",
    "PASSWORD": "p@ssw0rd",
    "HOST": "127.0.0.2",
    "PORT": 5433,
    "DB": "my_database2",
    "TEST": false
  },
  "LOGS": {
    "ERRORS": "logs/errors.log",
    "INFO": "data/info.log"
  },
  "FILES": {
    "STATIC_FOLDER": "static",
    "TEMPLATES_FOLDER": "templates"
  }
}
"""

OVERRIDE_TEST_DATA_JSON = """
{
  "DEFAULT": {
    "TEST": true
  },
  "APP": {
    "ENVIRONMENT": "development",
    "DEBUG": false
  },
  "DATABASE": {
    "USERNAME": "root666",
    "PASSWORD": "very well kept secret"
  }
}
"""

TEST_DATA_YAML = """
DEFAULT:
    TEST: True

APP:
    ENVIRONMENT: "development"
    DEBUG: false

DATABASE:
    USERNAME: "root3"
    PASSWORD: "p@ssw0rd"
    HOST: "127.0.0.3"
    PORT: 5434
    DB: "my_database3"
    TEST: false

LOGS:
    ERRORS: "logs/errors.log"
    INFO: "data/info.log"

FILES:
    STATIC_FOLDER: "static"
    TEMPLATES_FOLDER: "templates"
"""

TEST_DATA_TOML = """
[DEFAULT]
TEST = true

[APP]
ENVIRONMENT = "development"
DEBUG = false

[DATABASE]
USERNAME = "root4"
PASSWORD = "p@ssw0rd"
HOST = "127.0.0.4"
PORT = 5435
DB = "my_database4"
TEST = false

[LOGS]
ERRORS = "logs/errors.log"
INFO = "data/info.log"

[FILES]
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
"""

TEST_DATA_PROPERTIES_WITH_SECTIONS = """
[Test]
test.a = blah
my.name = Patrick
balance = 123

[Another]
my.name = Louis
my.name: Brad
"""

TEST_DATA_PROPERTIES_NO_SECTIONS = """
test.a = blah
my.name = Patrick
balance = 123
my.name = Louis
my.name: Brad
"""

TEST_DATA_JSON_MISSING_KEYS = """
{
  "DEFAULT": {
    "TEST": true
  },
  "APP": {
    "ENVIRONMENT": "development",
    "DEBUG": false
  },
  "DATABASE": {
    "PASSWORD": "p@ssw0rd",
    "HOST": "127.0.0.2",
    "PORT": 5433,
    "DB": "my_database2",
    "TEST": false
  },
  "LOGS": {
    "ERRORS": "logs/errors.log",
    "INFO": "data/info.log"
  },
  "FILES": {
    "STATIC_FOLDER": "static",
    "TEMPLATES_FOLDER": "templates"
  }
}
"""

TEST_DATA_JSON_WRONG_VALUES = """
{
  "DEFAULT": {
    "TEST": true
  },
  "APP": {
    "ENVIRONMENT": "development",
    "DEBUG": false
  },
  "DATABASE": {
    "USERNAME": "root2",
    "PASSWORD": "p@ssw0rd",
    "HOST": "127.0.0.2",
    "PORT": "some port",
    "DB": "my_database2",
    "TEST": false
  },
  "LOGS": {
    "ERRORS": "logs/errors.log",
    "INFO": "data/info.log"
  },
  "FILES": {
    "STATIC_FOLDER": "static",
    "TEMPLATES_FOLDER": "templates"
  }
}
"""

ENV_DATABASE_USERNAME = 'env_root'
ENV_DATABASE_HOST = '192.168.0.4'
ENV_DATABASE_PORT = 6666
ENV_APP_DEBUG = True


@dataclass
class LogConfig:
    ERRORS: str
    INFO: str


@dataclass
class AppConfig:
    ENVIRONMENT: str
    DEBUG: bool


@dataclass
class DatabaseConfig:
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB: Optional[str]


@dataclass
class CompositeConfig:
    LOGS: LogConfig
    APP: AppConfig
    DATABASE: DatabaseConfig
    EXTRA: Optional[str]

    # noinspection PyPep8Naming
    @property
    def DB_URL(self):
        return f'{self.DATABASE.HOST}:{self.DATABASE.PORT}'


@pytest.fixture
def ini_file(tmp_path):
    cfg_file = tmp_path.joinpath('config.ini')
    cfg_file.write_text(TEST_DATA_INI)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def json_file(tmp_path):
    cfg_file = tmp_path.joinpath('config.json')
    cfg_file.write_text(TEST_DATA_JSON)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def override_json_file(tmp_path):
    cfg_file = tmp_path.joinpath('config_override.json')
    cfg_file.write_text(OVERRIDE_TEST_DATA_JSON)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def json_file_missing_keys(tmp_path):
    cfg_file = tmp_path.joinpath('config.json')
    cfg_file.write_text(TEST_DATA_JSON_MISSING_KEYS)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def json_file_bad_values(tmp_path):
    cfg_file = tmp_path.joinpath('config.json')
    cfg_file.write_text(TEST_DATA_JSON_WRONG_VALUES)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def yaml_file(tmp_path):
    cfg_file = tmp_path.joinpath('config.yaml')
    cfg_file.write_text(TEST_DATA_YAML)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def toml_file(tmp_path):
    cfg_file = tmp_path.joinpath('config.toml')
    cfg_file.write_text(TEST_DATA_TOML)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def properties_file_with_sections(tmp_path):
    cfg_file = tmp_path.joinpath('config.properties')
    cfg_file.write_text(TEST_DATA_PROPERTIES_WITH_SECTIONS)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def properties_file_no_sections(tmp_path):
    cfg_file = tmp_path.joinpath('config.properties')
    cfg_file.write_text(TEST_DATA_PROPERTIES_NO_SECTIONS)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def fake_env(monkeypatch):
    monkeypatch.setenv('DATABASE__USERNAME', ENV_DATABASE_USERNAME)
    monkeypatch.setenv('DATABASE__HOST', ENV_DATABASE_HOST)
    monkeypatch.setenv('DATABASE__PORT', str(ENV_DATABASE_PORT))
    monkeypatch.setenv('APP__DEBUG', str(ENV_APP_DEBUG))
    yield
    monkeypatch.undo()


@pytest.mark.parametrize('val, expected_result', [
    (True, True), (False, False),
    ('True', True), ('\t\t\t \n   True \n\t  ', True), ('tRuE', True),
    (1, True), ('1', True), ('y', True), ('Y   ', True), ('T', True), ('\t\t\n 1 ', True),
    ('False', False), ('\t\t\t \n   False \n\t  ', False), ('fAlSe', False),
    (0, False), ('0', False), ('n', False), ('N   ', False), ('N', False), ('\t\t\n 0 ', False),
])
def test_str2bool_converter(val, expected_result):
    result = str2bool_converter(val)
    assert result == expected_result


@pytest.mark.parametrize('val', ['yep', 'Nope', 2, 5, -8, '67', 'ok'])
def test_str2bool_converter_bad_val(val):
    with pytest.raises(ValueError):
        str2bool_converter(val)


def test_load_from_ini_file(ini_file):
    d = load_from_ini_file(ini_file)
    assert d['APP']['ENVIRONMENT'] == 'development'
    assert d['APP']['TEST'] == 'True'
    assert d['DATABASE']['PASSWORD'] == 'p@ssw0rd'
    assert d['DATABASE']['PORT'] == '5432'
    assert d['LOGS']['ERRORS'] == 'logs/errors.log'
    assert d['LOGS']['INFO'] == 'data/info.log'
    assert d['FILES']['STATIC_FOLDER'] == 'static'
    assert d['FILES']['TEMPLATES_FOLDER'] == 'templates'


def test_load_from_json_file(json_file):
    d = load_from_json_file(json_file)
    assert d['DEFAULT']['TEST'] is True
    assert d['APP']['ENVIRONMENT'] == 'development'
    assert d['APP']['DEBUG'] is False
    assert d['DATABASE']['PASSWORD'] == 'p@ssw0rd'
    assert d['DATABASE']['PORT'] == 5433
    assert d['LOGS']['ERRORS'] == 'logs/errors.log'
    assert d['LOGS']['INFO'] == 'data/info.log'
    assert d['FILES']['STATIC_FOLDER'] == 'static'
    assert d['FILES']['TEMPLATES_FOLDER'] == 'templates'


def test_load_from_yaml_file(yaml_file):
    d = load_from_yaml_file(yaml_file)
    assert d['DEFAULT']['TEST'] is True
    assert d['APP']['ENVIRONMENT'] == 'development'
    assert d['APP']['DEBUG'] is False
    assert d['DATABASE']['PASSWORD'] == 'p@ssw0rd'
    assert d['DATABASE']['PORT'] == 5434
    assert d['LOGS']['ERRORS'] == 'logs/errors.log'
    assert d['LOGS']['INFO'] == 'data/info.log'
    assert d['FILES']['STATIC_FOLDER'] == 'static'
    assert d['FILES']['TEMPLATES_FOLDER'] == 'templates'


def test_load_from_toml_file(toml_file):
    d = load_from_toml_file(toml_file)
    assert d['DEFAULT']['TEST'] is True
    assert d['APP']['ENVIRONMENT'] == 'development'
    assert d['APP']['DEBUG'] is False
    assert d['DATABASE']['PASSWORD'] == 'p@ssw0rd'
    assert d['DATABASE']['PORT'] == 5435
    assert d['LOGS']['ERRORS'] == 'logs/errors.log'
    assert d['LOGS']['INFO'] == 'data/info.log'
    assert d['FILES']['STATIC_FOLDER'] == 'static'
    assert d['FILES']['TEMPLATES_FOLDER'] == 'templates'


def test_load_from_properties_file_from_ini(ini_file):
    d = load_from_properties_file(ini_file)
    assert d['APP']['ENVIRONMENT'] == 'development'
    assert d['APP']['TEST'] == 'True'
    assert d['DATABASE']['PASSWORD'] == 'p@ssw0rd'
    assert d['DATABASE']['PORT'] == '5432'
    assert d['LOGS']['ERRORS'] == 'logs/errors.log'
    assert d['LOGS']['INFO'] == 'data/info.log'
    assert d['FILES']['STATIC_FOLDER'] == 'static'
    assert d['FILES']['TEMPLATES_FOLDER'] == 'templates'


def test_load_from_properties_file_with_sections(properties_file_with_sections):
    d = load_from_properties_file(properties_file_with_sections)
    assert d['Test']['test.a'] == 'blah'
    assert d['Test']['balance'] == '123'
    assert d['Another']['my.name'] == 'Brad'


def test_load_from_properties_file_no_sections(properties_file_no_sections):
    d = load_from_properties_file(properties_file_no_sections)
    assert d['test.a'] == 'blah'
    assert d['balance'] == '123'
    assert d['my.name'] == 'Brad'


@pytest.mark.parametrize('file_name, default_ext', [
    ('test', ''),
    ('test', None),
    ('test', '   '),
    ('test', ' \t\t\t   \n\t\n\t\t\n\n\n '),
    ('test', '        '),
])
def test_load_config_from_file_missing_ext(file_name, default_ext):
    with pytest.raises(ValueError):
        load_config_from_file(Path(file_name), default_ext)


@pytest.mark.parametrize('file_name, default_ext', [
    ('test.PAT', ''),
    ('test.KLT', None),
    ('test.klm', '   '),
    ('test.broth', ' \t\t\t   \n\t\n\t\t\n\n\n '),
    ('test.MoJo', '        '),
])
def test_load_config_from_file_unknown_ext(file_name, default_ext):
    with pytest.raises(KeyError):
        load_config_from_file(file_name, default_ext)


# ConfigParser doesn't need a valid file
@pytest.mark.parametrize('file_name', [
    'test.json',
    'test.yaml',
    'test.yml',
    'test.toml',
])
def test_load_config_from_file_invalid_file(file_name):
    with pytest.raises(IOError):
        load_config_from_file(file_name)


def test_configurator_1(ini_file, json_file, yaml_file, toml_file):
    file_list = [ini_file, json_file, yaml_file, toml_file]
    c = Configurator(file_list)
    config_dict = c.load_configuration()
    assert config_dict['DATABASE']['USERNAME'] == 'root4'
    assert config_dict['DATABASE']['HOST'] == '127.0.0.4'
    assert config_dict['DATABASE']['PORT'] == 5435
    assert config_dict['DATABASE']['DB'] == 'my_database4'


def test_configurator_2(ini_file, json_file, yaml_file, toml_file):
    file_list = [ini_file, json_file, toml_file, yaml_file]
    c = Configurator(file_list)
    config_dict = c.load_configuration()
    assert config_dict['DATABASE']['USERNAME'] == 'root3'
    assert config_dict['DATABASE']['HOST'] == '127.0.0.3'
    assert config_dict['DATABASE']['PORT'] == 5434
    assert config_dict['DATABASE']['DB'] == 'my_database3'


def test_configurator_3(ini_file, json_file, yaml_file, toml_file):
    file_list = [json_file, yaml_file, toml_file, ini_file]
    c = Configurator(file_list)
    config_dict = c.load_configuration()
    assert config_dict['DATABASE']['USERNAME'] == 'root1'
    assert config_dict['DATABASE']['HOST'] == '127.0.0.1'
    assert config_dict['DATABASE']['PORT'] == '5432'
    assert config_dict['DATABASE']['DB'] == 'my_database1'


def test_configurator_ignore_missing(ini_file, json_file, yaml_file, toml_file):
    file_list = [ini_file, 'missing1.yaml', json_file, yaml_file, toml_file, 'missing2.json']
    c = Configurator(file_list)
    config_dict = c.load_configuration()
    assert config_dict['DATABASE']['USERNAME'] == 'root4'
    assert config_dict['DATABASE']['HOST'] == '127.0.0.4'
    assert config_dict['DATABASE']['PORT'] == 5435
    assert config_dict['DATABASE']['DB'] == 'my_database4'


def test_configurator_require_missing(ini_file, json_file, yaml_file, toml_file):
    file_list = [ini_file, 'missing1.yaml', json_file, yaml_file, toml_file, 'missing2.json']
    c = Configurator(file_list, ignore_missing=False)
    with pytest.raises(IOError):
        c.load_configuration()


def test_configurator_configure_files_only(ini_file, json_file, yaml_file, toml_file):
    file_list = [ini_file, json_file, yaml_file, toml_file]
    c = Configurator(file_list)
    cfg = c.configure(CompositeConfig)
    assert cfg.DATABASE.USERNAME == 'root4'
    assert cfg.DATABASE.HOST == '127.0.0.4'
    assert cfg.DATABASE.PORT == 5435
    assert cfg.APP.DEBUG is False


def test_configurator_configure_env(ini_file, json_file, yaml_file, toml_file, fake_env):
    file_list = [ini_file, json_file, yaml_file, toml_file]
    c = Configurator(file_list)
    cfg = c.configure(CompositeConfig)
    assert cfg.DATABASE.USERNAME == ENV_DATABASE_USERNAME
    assert cfg.DATABASE.HOST == ENV_DATABASE_HOST
    assert cfg.DATABASE.PORT == ENV_DATABASE_PORT
    assert cfg.APP.DEBUG is ENV_APP_DEBUG


def test_configurator_configure_missing_keys(json_file_missing_keys):
    file_list = [json_file_missing_keys]
    c = Configurator(file_list)
    with pytest.raises(MissingValueError):
        c.configure(CompositeConfig)


def test_configurator_configure_missing_keys_env(json_file_missing_keys, fake_env):
    file_list = [json_file_missing_keys]
    c = Configurator(file_list)
    cfg = c.configure(CompositeConfig)
    assert cfg.DATABASE.USERNAME == ENV_DATABASE_USERNAME
    assert cfg.DATABASE.HOST == ENV_DATABASE_HOST
    assert cfg.DATABASE.PORT == ENV_DATABASE_PORT
    assert cfg.APP.DEBUG is ENV_APP_DEBUG


def test_configurator_configure_wrong_values(json_file_bad_values):
    file_list = [json_file_bad_values]
    c = Configurator(file_list)
    with pytest.raises(ValueError):
        c.configure(CompositeConfig)


def test_configurator_configure_wrong_values_env(json_file_bad_values, fake_env):
    file_list = [json_file_bad_values]
    c = Configurator(file_list)
    cfg = c.configure(CompositeConfig)
    assert cfg.DATABASE.USERNAME == ENV_DATABASE_USERNAME
    assert cfg.DATABASE.HOST == ENV_DATABASE_HOST
    assert cfg.DATABASE.PORT == ENV_DATABASE_PORT
    assert cfg.APP.DEBUG is ENV_APP_DEBUG


def test_configurator_nested_override(json_file, override_json_file):
    file_list = [json_file, override_json_file]
    c = Configurator(file_list)
    cfg = c.configure(CompositeConfig)
    assert cfg.DATABASE.USERNAME == 'root666'
    assert cfg.DATABASE.PASSWORD == 'very well kept secret'
    assert cfg.DATABASE.HOST == '127.0.0.2'
    assert cfg.DATABASE.PORT == 5433
    assert cfg.DATABASE.DB == 'my_database2'
    assert cfg.APP.DEBUG is False


def test_standard_strategy_1():
    s = StandardStrategy(__file__, 'test-app', '.ini', 'development')
    expected_root = Path(__file__).parent
    assert s.project_root_dir == expected_root
    assert s.ext == '.ini'
    assert expected_root / 'config.ini' in s.config_file_list
    assert expected_root / 'config-dev.ini' in s.config_file_list
    assert Path.home() / '.test-app' / 'config.ini' in s.config_file_list
    assert Path.home() / '.test-app' / 'config-dev.ini' in s.config_file_list
    assert Path('/etc/test-app') / 'config.ini' in s.config_file_list
    assert Path('/etc/test-app') / 'config-dev.ini' in s.config_file_list


def test_standard_strategy_2():
    s = StandardStrategy(__file__, 'test-app', 'InI', 'dev')
    expected_root = Path(__file__).parent
    assert s.project_root_dir == expected_root
    assert s.ext == '.ini'
    assert expected_root / 'config.ini' in s.config_file_list
    assert expected_root / 'config-dev.ini' in s.config_file_list
    assert Path.home() / '.test-app' / 'config.ini' in s.config_file_list
    assert Path.home() / '.test-app' / 'config-dev.ini' in s.config_file_list
    assert Path('/etc/test-app') / 'config.ini' in s.config_file_list
    assert Path('/etc/test-app') / 'config-dev.ini' in s.config_file_list


def test_standard_strategy_3():
    s = StandardStrategy(__file__, 'test-app')
    expected_root = Path(__file__).parent
    assert s.project_root_dir == expected_root
    assert s.ext == '.yaml'
    assert expected_root / 'config.yaml' in s.config_file_list
    assert expected_root / 'config-dev.yaml' in s.config_file_list
    assert Path.home() / '.test-app' / 'config.yaml' in s.config_file_list
    assert Path.home() / '.test-app' / 'config-dev.yaml' in s.config_file_list
    assert Path('/etc/test-app') / 'config.yaml' in s.config_file_list
    assert Path('/etc/test-app') / 'config-dev.yaml' in s.config_file_list


@dataclass
class Address:
    street: str = field(metadata={'env': 'STREET_ADDRESS'})
    province: str = field(metadata={'env': 'STATE'})
    city: str
    country: str = field(default='Canada')


@dataclass(frozen=True)
class Person:
    first_name: str = field(metadata={'env': 'GIVEN_NAME'})
    last_name: str = field(metadata={'env': 'FAMILY_NAME'})
    name: str = field(init=False)
    address: Address

    def __post_init__(self):
        object.__setattr__(self, 'name', f'{self.first_name} {self.last_name}')


@dataclass
class ConfigWithMetadata:
    DB_URL: str = field(metadata={'env': 'DATABASE_URL'})
    PERSON: Person


METADATA_TEST_DATA_COMPLETE = """
DB_URL: test_url
PERSON:
    first_name: Peter
    last_name: Pan
    address:
        street: 123 Over The Rainbow Rd.
        city: Toronto
        province: 'ON'
"""

METADATA_TEST_DATA_PARTIAL = """
PERSON:
    first_name: Peter
    address:
        street: 123 Over The Rainbow Rd.
        city: Toronto
        province: 'ON'
        country: "Snow Mexico"

"""


@pytest.fixture
def metadata_testing_env_partial(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'another_test_url')
    monkeypatch.setenv('PERSON__FAMILY_NAME', 'Panda')
    yield
    monkeypatch.undo()


@pytest.fixture
def metadata_testing_env_complete(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'another_test_url')
    monkeypatch.setenv('PERSON__GIVEN_NAME', 'Pedro')
    monkeypatch.setenv('PERSON__FAMILY_NAME', 'Pan')
    monkeypatch.setenv('PERSON__address__STREET_ADDRESS', '345 Sequoia Blvd.')
    monkeypatch.setenv('PERSON__address__city', 'Los Angeles')
    monkeypatch.setenv('PERSON__address__STATE', 'CA')
    monkeypatch.setenv('PERSON__address__country', 'US of A')
    yield
    monkeypatch.undo()


@pytest.fixture
def config_with_metadata_complete(tmp_path):
    cfg_file = tmp_path.joinpath('config.yaml')
    cfg_file.write_text(METADATA_TEST_DATA_COMPLETE)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


@pytest.fixture
def config_with_metadata_partial(tmp_path):
    cfg_file = tmp_path.joinpath('config.yaml')
    cfg_file.write_text(METADATA_TEST_DATA_PARTIAL)
    yield cfg_file
    cfg_file.unlink(missing_ok=True)


def test_configurator_metadata_file(config_with_metadata_complete):
    file_list = [config_with_metadata_complete]
    c = Configurator(file_list)
    cfg = c.configure(ConfigWithMetadata)
    assert cfg.DB_URL == 'test_url'
    assert cfg.PERSON.first_name == 'Peter'
    assert cfg.PERSON.last_name == 'Pan'
    assert cfg.PERSON.name == 'Peter Pan'
    assert cfg.PERSON.address.street == '123 Over The Rainbow Rd.'
    assert cfg.PERSON.address.city == 'Toronto'
    assert cfg.PERSON.address.province == 'ON'
    assert cfg.PERSON.address.country == 'Canada'


def test_configurator_metadata_file_and_env(config_with_metadata_partial, metadata_testing_env_partial):
    file_list = [config_with_metadata_partial]
    c = Configurator(file_list)
    cfg = c.configure(ConfigWithMetadata)
    assert cfg.DB_URL == 'another_test_url'
    assert cfg.PERSON.first_name == 'Peter'
    assert cfg.PERSON.last_name == 'Panda'
    assert cfg.PERSON.name == 'Peter Panda'
    assert cfg.PERSON.address.street == '123 Over The Rainbow Rd.'
    assert cfg.PERSON.address.city == 'Toronto'
    assert cfg.PERSON.address.province == 'ON'
    assert cfg.PERSON.address.country == 'Snow Mexico'


def test_configurator_metadata_env(metadata_testing_env_complete):
    file_list = []
    c = Configurator(file_list)
    cfg = c.configure(ConfigWithMetadata)
    assert cfg.DB_URL == 'another_test_url'
    assert cfg.PERSON.first_name == 'Pedro'
    assert cfg.PERSON.last_name == 'Pan'
    assert cfg.PERSON.name == 'Pedro Pan'
    assert cfg.PERSON.address.street == '345 Sequoia Blvd.'
    assert cfg.PERSON.address.city == 'Los Angeles'
    assert cfg.PERSON.address.province == 'CA'
    assert cfg.PERSON.address.country == 'US of A'


def test_configurator_metadata_override(config_with_metadata_complete, metadata_testing_env_complete):
    file_list = [config_with_metadata_complete]
    c = Configurator(file_list)
    cfg = c.configure(ConfigWithMetadata)
    assert cfg.DB_URL == 'another_test_url'
    assert cfg.PERSON.first_name == 'Pedro'
    assert cfg.PERSON.last_name == 'Pan'
    assert cfg.PERSON.name == 'Pedro Pan'
    assert cfg.PERSON.address.street == '345 Sequoia Blvd.'
    assert cfg.PERSON.address.city == 'Los Angeles'
    assert cfg.PERSON.address.province == 'CA'
    assert cfg.PERSON.address.country == 'US of A'
