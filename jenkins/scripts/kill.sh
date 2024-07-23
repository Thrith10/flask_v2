#!/usr/bin/env sh

set -x
docker kill my-flask-app
docker rm my-flask-app
