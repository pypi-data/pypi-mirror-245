# 创建应用实例
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rmbserver.servers import run_server


# 启动Flask Web服务
if __name__ == '__main__':
    try:
        run_server(sys.argv[1], int(sys.argv[2]))
    except:
        run_server()
