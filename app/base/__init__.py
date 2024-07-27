# app/base/__init__.py
from flask import Blueprint

base = Blueprint('base', __name__)

def none_to_empty(value):
    return '' if value == None else value

def none_to_empty_price(value):
    return f"${value}/ea" if value is not None else ''

# Register the custom filter with the blueprint
base.add_app_template_filter(none_to_empty)
base.add_app_template_filter(none_to_empty_price)

from . import routes