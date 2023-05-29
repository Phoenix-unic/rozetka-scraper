import sys, os, django


sys.path.append(os.path.abspath('rozetka'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rozetka.settings'
django.setup()