#!/bin/bash

supervisord && /usr/local/bin/build-images.sh && waitress-serve --port=$1 worker.app:app