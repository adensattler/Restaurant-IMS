# app/base/__init__.py
from flask import Blueprint

base = Blueprint('base', __name__)

def none_to_empty(value):
    return '' if value == None else value

# Register the custom filter with the blueprint
base.add_app_template_filter(none_to_empty)

from . import routes