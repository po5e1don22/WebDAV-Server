from config_loader import config_loader

def main():
    config = config_loader()

    if not config["storage"]["shared_folder"]:
        print("⚠️ Attention: shared_folder is not specified.")

    print("✅ Configuration is loaded.")
    print(config)

if __name__ == "__main__":
    main()