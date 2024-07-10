# app/base/__init__.py
from flask import Blueprint

base = Blueprint('base', __name__)

from . import routes