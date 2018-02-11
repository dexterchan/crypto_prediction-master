#!/usr/bin/env bash

PRJ=dextergcptest1

DOCKER_IMAGE_NAME=gcr.io/$PRJ/crypto_predict_py:v1

gcloud docker -- push $DOCKER_IMAGE_NAME