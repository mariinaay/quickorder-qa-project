#!/bin/sh
set -e
if [ ! -f /data/quickorder.db ]; then
  python seed.py
else
  echo "Database already exists; keeping current data."
fi
exec python run.py
