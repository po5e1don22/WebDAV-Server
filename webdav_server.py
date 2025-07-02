from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from cheroot import wsgi

def start_webdav_server(config: dict):
    folder = config.get("storage", {}).get("shared_folder")
    host = config.get("server", {}).get("host", "127.0.0.1")
    port = config.get("server", {}).get("port", 8080)

    if not folder:
        raise ValueError("No storage folder set in config.")

    print(f"Starting WebDAV server at http://{host}:{port}")
    print(f"Serving folder: {folder}")

    config_dict = {
        "provider_mapping": {"/": FilesystemProvider(folder)},
        "simple_dc": {"user_mapping": {"*": True}},
        "verbose": 1,
        "logging": {"enable_loggers": {}},
    }

    app = WsgiDAVApp(config_dict)
    server = wsgi.Server((host, port), app)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped by user")
    finally:
        server.stop()
