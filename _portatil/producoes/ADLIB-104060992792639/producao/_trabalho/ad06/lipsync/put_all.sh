# uso: sh put_all.sh up.tsv  (linhas: arquivo content-type asset_id url, separadas por espaço)
while read f ct id url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: $ct" -H "x-amz-server-side-encryption: AES256" --data-binary "@$f" "$url")
  echo "$f $code"
done < "$1"
