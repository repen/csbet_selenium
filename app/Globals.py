import os
HeaderPath = os.getenv("APP_HOME", "/home/repente/prog/python/kwork/selenium/betcsgo/DockerApp/app")
WORK_DIR   = HeaderPath
LOGIN = "testapp1233"
PASSWORD = "+$f4I+qTxp"

REDIS_PORT = 6379
REDIS_HOST = "redisa"
# docker run -d -v betcss:/usr/src/app/data --name selenium --network=mynet selenium_docker