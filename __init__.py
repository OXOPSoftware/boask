# boask/__init__.py
from .core import route, use, run_server
from .templates.html import html_templates
from .templates.tsx import tsx_templates

__version__ = "1.0.2"
__all__ = ["route", "use", "run_server", "html_templates", "tsx_templates"]