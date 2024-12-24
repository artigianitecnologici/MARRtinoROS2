 #!/bin/bash
#set -x  # Abilita il debug

docker build --no-cache -t marrtinorobot2:humble -f Dockerfile.system .
