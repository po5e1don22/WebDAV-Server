import os
import shutil
import yaml

CONFIG_DIR = "config"
DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, "default_config.yaml")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

def config_loader():
    #creating config.yaml from a template if it does not exist
    if not os.path.exists(CONFIG_PATH):
        if not os.path.exists(DEFAULT_CONFIG_PATH):
            raise FileNotFoundError("No default_main.yaml found!")
        shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
        print("[config loader] config.yaml is created from a template.")

    #loading main.yaml
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
            print("[config loader] config.yaml uploaded successfully." )
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error in YAML: {e}")
    return config