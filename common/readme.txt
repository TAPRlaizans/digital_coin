#///////////////////////////////////////////////////////////////////////////////
#
# (c) 2019-2022 Toolsensing, Inc. All rights reserved.
# Unless otherwise permitted, no distribution or use is permitted.
#
#///////////////////////////////////////////////////////////////////////////////

1. if you want to use log_helper, then you should install ConcurrentLogHandler module
by "pip3 install ConcurrentLogHandler==0.9.1"

2. if you want to use command_control, then you should install ConcurrentLogHandler module
by "pip3 install paramiko==2.6.0"

3. if you want to use tool to add log info, then import log_helper module .

如果某个py文件需要包含common文件下某些模块来使用需要包含以下内容
```
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
PARENT_PARENT_DIR = os.path.dirname(PARENT_DIR)
PARENT_PARENT_PARENT_DIR = os.path.dirname(PARENT_PARENT_DIR)
sys.path.append(BASE_DIR)
sys.path.append(PARENT_DIR)
sys.path.append(PARENT_PARENT_DIR)
sys.path.append(PARENT_PARENT_PARENT_DIR)

from common.time_helper import TimeUntil as tm
from common.json_helper import JsonHelper as jh
from common.logger import Logger, LogLevel 
from common.file_helper import FileHelper as fh
from common.math_hepler import MathHelper as mh
from common.excle_helper import ExcleHelper as eh
```