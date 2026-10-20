import sys, requests
arq, key, sig, pol = sys.argv[1:5]
f = {"Content-Type":"image/png","key":key,"x-goog-date":"20261014T174551Z","x-goog-credential":"vercel-app-prod@flora-prod-455015.iam.gserviceaccount.com/20261014/auto/storage/goog4_request","x-goog-algorithm":"GOOG4-RSA-SHA256","policy":pol,"x-goog-signature":sig}
r = requests.post("https://storage.googleapis.com/flora-assets-prod/", data=f, files={"file": (arq.split("/")[-1], open(arq,"rb"), "image/png")}); print(r.status_code, r.text[:200])
