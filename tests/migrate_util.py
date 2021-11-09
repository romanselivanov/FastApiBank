import os
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database

os.environ['TESTING'] = 'True'
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///example_test.db"

create_database(TEST_SQLALCHEMY_DATABASE_URL) # Создаем БД
base_dir = os.path.dirname(os.path.dirname(__file__))
alembic_cfg = Config(os.path.join(base_dir, "alembic.ini")) # Загружаем конфигурацию alembic 
# command.revision(alembic_cfg, message = "migration", autogenerate = True, version_path="migrations/testversions", rev_id = "1111111111")
command.upgrade(alembic_cfg, revision = "1111111111@head") # выполняем миграции