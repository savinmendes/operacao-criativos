# uso: sh put.sh up.tsv  (linhas: arquivo asset_id url) -> PUT de cada arquivo em in/
while read f id url; do
  ct=video/mp4
  case $f in *.mp3) ct=audio/mpeg;; esac
  c=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: $ct" -H "x-amz-server-side-encryption: AES256" --data-binary @in/$f "$url")
  echo "$f $c"
done < "$1"
