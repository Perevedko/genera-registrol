#!/bin/sh
docker stop genera
docker rm genera
docker build -t genera-img .
docker run -p 8080:8080 --name genera -t genera-img
