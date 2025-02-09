import os

__version__ = "1.5.0"

resources_path = os.path.join(os.path.dirname(__file__), "resources")
languages_path = os.path.join(os.path.dirname(__file__), "languages")

# Cache Directory: Store images
if p := os.getenv("XDG_CACHE_HOME"):
    cache_dir = os.path.join(p, "rare/cache")
elif os.name == "nt":
    cache_dir = os.path.expandvars("%APPDATA%/rare/cache")
else:
    cache_dir = os.path.expanduser("~/.cache/rare/")
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Data Directory: Images
if p := os.getenv("XDG_DATA_HOME"):
    data_dir = os.path.join(p, "rare")
if os.name == "nt":
    data_dir = os.path.expandvars("%APPDATA%/rare/")
else:
    data_dir = os.path.expanduser("~/.local/share/rare/")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

image_dir = os.path.join(data_dir, "images")
