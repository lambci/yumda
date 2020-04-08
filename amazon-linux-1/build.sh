#!/bin/sh

docker build --pull --squash --no-cache -t lambci/yumda:1 .
