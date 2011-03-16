"""This is the base model for Gasista Felice. i

It includes common data on which all (or almost all) other applications rely on.
"""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from gasistafelice.base.const import CONTACT_CHOICES

class Person(models.Model):
    """A person is an anagraphic record of a human.
    It can be a user or not.
    """

    uuid = models.CharField(max_length=128, unique=True, blank=True, null=True, help_text=_('Write your social security number here'))
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    displayName = models.CharField(max_length=128)
    contacts = models.ManyToManyField('Contact')
    user = models.OneToOneField(User, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)
   
class Contact(models.Model):

    contact_type = models.CharField(max_length=32, choices=CONTACT_CHOICES)
    contact_value = models.CharField(max_length=32)

class Role(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()


