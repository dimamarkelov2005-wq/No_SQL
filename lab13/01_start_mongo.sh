#!/usr/bin/env bash
set -euo pipefail

read -s -p "Введите пароль администратора MongoDB (hradmin): " MONGO_ROOT_PASS
echo ""

docker run -d --name mongo-hr-lab13 \
  -p 127.0.0.1:27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=hradmin \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_ROOT_PASS" \
  mongo:7

unset MONGO_ROOT_PASS
echo "Контейнер mongo-hr-lab13 запущен."
