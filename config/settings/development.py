# development.py
from .base import Base


class Development(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['*']