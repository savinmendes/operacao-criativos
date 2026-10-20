# -*- coding: utf-8 -*-
"""Imprime o JSON 'files' do create_asset_upload_batch para os ids dados (in.mp4 + de.mp3 de cada)."""
import sys, json
from pathlib import Path
AQ = Path(__file__).resolve().parent.parent
fs = []
for tid in sys.argv[1:]:
    D = AQ / "work" / tid
    fs.append({"filename": f"{tid}_in.mp4", "content_type": "video/mp4", "size_bytes": (D / "in.mp4").stat().st_size})
    fs.append({"filename": f"{tid}_de.mp3", "content_type": "audio/mpeg", "size_bytes": (D / "de.mp3").stat().st_size})
print(json.dumps(fs))
