#!/bin/sh

set -e

BASE_PATH="$(dirname "$(readlink -f "$0")")"

# If pyproject.toml exists, use dev environment
if [ -f "$BASE_PATH/pyproject.toml" ]; then
  echo 'Обнаружен pyproject.toml, используется dev-окружение.'
  if ! [ -x "$(command -v poetry)" ]; then
    echo 'Внимание: poetry не установлен.' >&2
    exit 1
  fi

  export PYTHONPATH=$BASE_PATH/src
  cd "$BASE_PATH"/src/compmath
  poetry run python main.py "$@"
  exit 0
fi

# Use venv environment when installed
export PYTHONPATH=$BASE_PATH

. "$BASE_PATH/venv/bin/activate"

cd "$BASE_PATH"/compmath
python "main.py" "$@"