import sys, json
from pathlib import Path
AQ = Path(__file__).resolve().parent.parent
a = json.load(open(AQ / "_tmp" / "assets.json"))
out = []
for t in sys.argv[1:]:
    out.append({"title": f"VSLDE {t}", "mode": "speed", "video": {"type": "asset_id", "asset_id": a[f"{t}_in.mp4"]},
                "audio": {"type": "asset_id", "asset_id": a[f"{t}_de.mp3"]}, "enable_dynamic_duration": False,
                "keep_the_same_format": True, "fps_mode": "cfr", "enable_watermark": False})
print(json.dumps(out))
