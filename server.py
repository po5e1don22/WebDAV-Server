from config_loader import config_loader
from webdav_server import start_webdav_server

def main():
    config = config_loader()
    start_webdav_server(config)

    if not config["storage"]["shared_folder"]:
        print("⚠️ Attention: shared_folder is not specified.")

    print("✅ Configuration is loaded.")
    print(config)

if __name__ == "__main__":
    main()