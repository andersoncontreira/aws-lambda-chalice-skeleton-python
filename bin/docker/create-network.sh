if test -f .projectrc; then
  source .projectrc
elif test -f ./bin/.projectrc; then
  source ./bin/.projectrc
fi

if [ -z "$NETWORK_NAME" ]; then
  echo 'Network name not defined'
else
  docker network create $NETWORK_NAME
  exit 1
fi
