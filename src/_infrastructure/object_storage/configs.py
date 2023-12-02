import os
import pathlib

CLOUD_STORAGE_CONFIG_FILE = os.path.join(
    pathlib.Path(__file__).parent.parent.parent.parent, "storage/cloud_storage_config.json")
CLOUD_STORAGE_BUCKET = "pawtnerup-assets"
