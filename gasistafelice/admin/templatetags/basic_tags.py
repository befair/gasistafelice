from django import template
from django.conf import settings
from django.template import resolve_variable, loader
from django.template import TemplateSyntaxError
from django.template.loader import get_template, select_template

from django.db import models
import datetime, os.path

register = template.Library()

@register.simple_tag
def des_media_url():
	return settings.MEDIA_URL

@register.simple_tag
def des_debug():
	return settings.DEBUG

@register.simple_tag
def des_version():
	return settings.VERSION


