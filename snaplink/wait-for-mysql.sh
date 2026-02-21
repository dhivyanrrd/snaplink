#!/bin/sh
echo "Waiting for MySQL to be ready..."
while ! nc -z db 3306; do
  sleep 1
  echo "Still waiting for MySQL..."
done
echo "MySQL is ready!"