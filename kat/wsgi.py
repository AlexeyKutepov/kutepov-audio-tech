"""
WSGI config for KAT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

# add the hellodjango project path into the sys.path
sys.path.append('/home/akutepov/web/kat/')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/akutepov/web/kat3.7_env/lib/python3.7/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kat.settings')

application = get_wsgi_application()
