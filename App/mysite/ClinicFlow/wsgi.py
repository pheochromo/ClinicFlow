"""
WSGI config for ClinicFlow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


import sys
sys.path.append('home/ec2-user/envClinicFlow/ClinicFlow')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClinicFlow.settings")

application = get_wsgi_application()
