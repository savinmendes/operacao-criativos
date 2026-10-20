#!/bin/sh
# uso: put.sh arquivo content-type url
curl -s -o /dev/null -w "%{http_code}\n" -X PUT -H "Content-Type: $2" -H "x-amz-server-side-encryption: AES256" --data-binary "@$1" "$3"
