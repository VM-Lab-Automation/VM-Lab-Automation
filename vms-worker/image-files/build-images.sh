#!/bin/bash

while !(docker stats --no-stream); do
  echo "Waiting for Docker to launch..."
  sleep 3
done

cd /app/vm/lab-base-container && docker build -t lab-base .
