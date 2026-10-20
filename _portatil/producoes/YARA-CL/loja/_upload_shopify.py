# -*- coding: utf-8 -*-
"""Envia o vídeo e o poster para os staged uploads do Shopify."""
import requests

video_params = {
    "GoogleAccessId": "video-production@video-production-225115.iam.gserviceaccount.com",
    "key": "c/o/v/d8e0f8130bd942528017a8333edd7fb6.mp4",
    "policy": "eyJjb25kaXRpb25zIjpbWyJlcSIsIiRidWNrZXQiLCJzaG9waWZ5LXZpZGVvLXByb2R1Y3Rpb24tY29yZS1vcmlnaW5hbHMiXSxbImVxIiwiJGtleSIsImMvby92L2Q4ZTBmODEzMGJkOTQyNTI4MDE3YTgzMzNlZGQ3ZmI2Lm1wNCJdLFsiY29udGVudC1sZW5ndGgtcmFuZ2UiLDM4NjE1MzMsMzg2MTUzM11dLCJleHBpcmF0aW9uIjoiMjAyNi0xMC0wOVQyMjo1NToxM1oifQ==",
    "signature": "mMi7dVTJyXGsO0rr6wh8JcuxQCwntBL8OkO/MGkIyoI71mEvzYRbubTOOO25J8dO1kVMX8wRM+ErQJYXf3CNoFHV//Qf4Jh3qiNTl+Kk/ns1MZUKP1kpaQMst8IwR3eMhqRyw3kxmLhFUz7xF+b5HVlQVSib04FGQ13extIHkGfwt3sV3OPdt80rDdkPberxOY2qEAxIhSvSHVeqG885EvwuJlnoJzvtNvLu1+fyy1vB8eO9aTIokGFmZINvGkX5nQTAjVpW0PhYZO7bZiC5Z+p7Sc0f2sQ+2QjozeoaDbirF90HEBlz9ZhOCZtA/aEury0OuCtcHZDo3eIhiXmlAA==",
}
img_params = {
    "Content-Type": "image/jpeg",
    "success_action_status": "201",
    "acl": "private",
    "key": "tmp/69972820224/files/a3c8f521-dbf0-463d-a25f-95bb4167346b/loja-chile-avatar-poster.jpg",
    "x-goog-date": "20261009T215447Z",
    "x-goog-credential": "merchant-assets@shopify-tiers.iam.gserviceaccount.com/20261009/auto/storage/goog4_request",
    "x-goog-algorithm": "GOOG4-RSA-SHA256",
    "x-goog-signature": "932171d1ce567b719092bac75d773aefea5acccdf4a22481f0d8b7052a150e3c692ad118921218f3d330f95c6b9f5f41de599b32180456f7fa50bb1ec71bcf6032c1eebc961302c10e4cfce5a5f3e571ce45472ca76d2d0510810766e447e69f3cc3660728fa10abf16fae5fed330f0df9e0d1f59edc9c87e579e021407fd3340ab02792772886c819cf949e56bff0ffae46eacab65d97c584d7098077506139b42d913ebdcd3bb7c4b7ffc7d102be8314861782f5f5c11b545f05307527d9bd4aeec4d9d8615bce0bccdc031930db894c2fedfc6c1aaf1448b3e4d98e9494549197f6107a175b5d83401904523a94a0c36bdddec560660655939d5d0c2138f1",
    "policy": "eyJjb25kaXRpb25zIjpbeyJDb250ZW50LVR5cGUiOiJpbWFnZVwvanBlZyJ9LHsic3VjY2Vzc19hY3Rpb25fc3RhdHVzIjoiMjAxIn0seyJhY2wiOiJwcml2YXRlIn0sWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsMSwyMDk3MTUyMF0seyJidWNrZXQiOiJzaG9waWZ5LXN0YWdlZC11cGxvYWRzIn0seyJrZXkiOiJ0bXBcLzY5OTcyODIwMjI0XC9maWxlc1wvYTNjOGY1MjEtZGJmMC00NjNkLWEyNWYtOTViYjQxNjczNDZiXC9sb2phLWNoaWxlLWF2YXRhci1wb3N0ZXIuanBnIn0seyJ4LWdvb2ctZGF0ZSI6IjIwMjYxMDA5VDIxNTQ0N1oifSx7IngtZ29vZy1jcmVkZW50aWFsIjoibWVyY2hhbnQtYXNzZXRzQHNob3BpZnktdGllcnMuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb21cLzIwMjYxMDA5XC9hdXRvXC9zdG9yYWdlXC9nb29nNF9yZXF1ZXN0In0seyJ4LWdvb2ctYWxnb3JpdGhtIjoiR09PRzQtUlNBLVNIQTI1NiJ9XSwiZXhwaXJhdGlvbiI6IjIwMjYtMTAtMTBUMjE6NTQ6NDdaIn0=",
}
with open("loja-chile_avatar_legendado.mp4", "rb") as f:
    r = requests.post("https://shopify-video-production-core-originals.storage.googleapis.com",
                      data=video_params, files={"file": ("loja-chile-avatar.mp4", f, "video/mp4")}, timeout=600)
print("video", r.status_code, r.text[:200])
with open("poster.jpg", "rb") as f:
    r = requests.post("https://shopify-staged-uploads.storage.googleapis.com/",
                      data=img_params, files={"file": ("loja-chile-avatar-poster.jpg", f, "image/jpeg")}, timeout=600)
print("poster", r.status_code, r.text[:200])
