if test -f "requirements-layers.txt"; then
  input="requirements-layers.txt"
  while IFS= read -r arn
  do
    echo "current arn: $arn"
    url=$(aws lambda get-layer-version-by-arn --arn $arn --query Content.Location --output text)
    replacer="-"
    zip_file_name="${arn//\:/$replacer}"

    # create the tmp dir
    if test ! -d "./tmp"; then
      echo 'create the tmp dir'
      mkdir ./tmp/
    fi

    # do the download
    echo 'do the download'
    curl $url -o ./tmp/$zip_file_name

    # extract zip content
    echo 'extract zip content'
    unzip ./tmp/$zip_file_name -d ./vendor

  done < "$input"
fi