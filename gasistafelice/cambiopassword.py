# IPython log file

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
User.objects.get(username='domthu')
u = User.objects.get(username='domthu')
u.set_password('a')
u.save()
authenticate(username='domthu', password='a')
get_ipython().magic(u'logstart')
