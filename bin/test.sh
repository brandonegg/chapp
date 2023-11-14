if ! [ -x "$(command -v pytest)" ]; then
  pip install -U pytest
fi

pytest