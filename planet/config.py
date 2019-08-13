import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "postgresql://localhost:5432/planet"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
