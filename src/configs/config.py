import os
import logging

import sqlalchemy as db

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

mode = os.environ.get('HB_ENV')
if mode == 'development':
    load_dotenv('src/configs/envs/dev-env/.env')
elif mode == 'docker':
    load_dotenv('src/configs/envs/docker-env/.env')
else:
    load_dotenv('src/configs/envs/prod-env/.env')


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Settings:
    HB_ENV: str = os.environ.get('HB_ENV')
    # Database
    DATABASE_NODE: str = os.environ.get('DATABASE_NODE')
    DATABASE_PORT: int = int(os.environ.get('DATABASE_PORT'))
    DATABASE_USERNAME: str = os.environ.get('DATABASE_USERNAME')
    DATABASE_PASSWORD: str = os.environ.get('DATABASE_PASSWORD')
    DATABASE_DATABASE: str = os.environ.get('DATABASE_DATABASE')
    # API
    APP_NAME: str = os.environ.get('APP_NAME')
    API_NODE: str = os.environ.get('API_NODE')
    API_PORT: int = int(os.environ.get('API_PORT'))
    API_SECRET_KEY: str = os.environ.get('API_SECRET_KEY')
    API_HASH_ALGORITHM: str = os.environ.get('API_HASH_ALGORITHM')
    ADMIN_USERNAME: str = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD: str = os.environ.get('ADMIN_PASSWORD')
    API_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('API_ACCESS_TOKEN_EXPIRE_MINUTES'))

    def get_db(self):
        engine = db.create_engine(self.DATABASE_URL)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        sess = session()
        try:
            yield sess
        finally:
            sess.close()


settings = Settings()
logger.info('Settings configured')
