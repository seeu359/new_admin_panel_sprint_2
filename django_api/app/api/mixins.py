import uuid
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleType(Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True
