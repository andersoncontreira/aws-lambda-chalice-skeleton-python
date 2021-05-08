TARGET=$1
if [ -z "$TARGET" ]; then
  TARGET=./public/swagger/openapi.json
fi

if ! test -f $TARGET; then
  echo "Target $TARGET not exists"
  exit 1
else
  chalice generate-models > $TARGET
fi