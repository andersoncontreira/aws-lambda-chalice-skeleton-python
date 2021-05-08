if [ -z "$1" ]; then
  echo 'Queue name must be informed'
  exit 1
else
  aws sqs get-queue-url --queue-name $1
  if [ $? -eq 0 ]; then
      echo "Queue already created"
  else
      aws sqs create-queue --queue-name $1
      if [ $? -eq 0 ]; then
        echo "Queue created"
      else
        echo "Queue not created"
      fi
  fi
fi
