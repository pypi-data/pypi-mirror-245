import os
from rmbserver.config.default import *

if os.path.exists(os.path.join(os.path.dirname(__file__), 'custom.py')):
    from rmbserver.config.custom import *
