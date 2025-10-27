import os
import sys
import django
from pathlib import Path

# This is the folder that contains the Django module 'news_application'
DJANGO_PARENT = Path(__file__).resolve().parent.parent.parent / 'news_application'

# Add it to sys.path so Python can find 'news_application'
sys.path.insert(0, str(DJANGO_PARENT))

# Set the correct settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_application.settings'

# Setup Django
django.setup()
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'News'
copyright = '2025, Siphephile'
author = 'Siphephile'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
