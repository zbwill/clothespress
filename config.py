# coding:utf-8
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    LOG_LEVEL = 0
    LOG_FILE_PATH = os.path.join(BASE_DIR, 'log', 'Snail.log')
    LOG_MAX_SIZE = 10 * 1024 * 1024
    LOG_BACKUP_COUNT = 5
    FILE_LOG_LEVEL = 10
    STREAM_LOG_LEVEL = 20

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
