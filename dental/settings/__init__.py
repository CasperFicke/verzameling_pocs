# dental/settings/__init__.py
import os
#from .dev import *

if os.environ['DENTAL_PROJ'] == 'dev':
  from .dev import *
else:
  from .prod import *