import os

# 导入plugin中的配置项
from rmbserver.plugins.config import *

# 导入 default 中的配置项
from rmbserver.config.default import *

# custom 会覆盖 plugin 和 default 中的配置项
if os.path.exists(os.path.join(os.path.dirname(__file__), 'custom.py')):
    from rmbserver.config.custom import *


