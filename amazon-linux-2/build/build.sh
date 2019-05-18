#!/bin/sh

docker build --pull --squash -t lambci/yumda:build-2 .
