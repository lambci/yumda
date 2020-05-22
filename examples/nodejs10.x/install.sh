#!/bin/bash

rm -rf dependencies
mkdir -p dependencies

docker run --rm -v "$PWD"/dependencies:/lambda/opt lambci/yumda:2 yum install -y git GraphicsMagick jp2a

# To test:

# sam local invoke --no-event

# OR

# sls invoke local --docker -f hello-world

# To prepare to deploy:

# cd dependencies
# zip -yr ../dependencies.zip .
# cd ..
