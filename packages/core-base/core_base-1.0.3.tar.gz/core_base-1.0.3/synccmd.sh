#!/bin/bash
# 30 0 * * * /xxx/a.sh
curl http://10.104.1.191:8080/api/system/user/syncOrgAndUser/

exec "$@"