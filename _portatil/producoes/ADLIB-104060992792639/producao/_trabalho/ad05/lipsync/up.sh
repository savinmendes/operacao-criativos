while IFS='|' read -r f u; do
  [ -z "$f" ] && continue
  case $f in *.mp4) ct=video/mp4;; *) ct=audio/mpeg;; esac
  code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: $ct" -H "x-amz-server-side-encryption: AES256" --data-binary "@$f" "$u")
  echo "$f $code"
done < "$1"
