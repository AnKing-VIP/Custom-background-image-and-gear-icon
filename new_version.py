import re
import sys
import time
import simplejson
from pathlib import Path

version_string = sys.argv[1]
assert re.match(r"^(\d+).(\d+)$", version_string)
addon_root = Path(sys.argv[2])
assert addon_root.is_dir()


manifest_path = addon_root / "manifest.json"
# Write version in manifest.json
with manifest_path.open("r") as f:
    manifest = simplejson.load(f)


manifest["version"] = version_string
manifest["mod"] = int(time.time())

with manifest_path.open("w") as f:
    simplejson.dump(manifest, f, indent=2)
