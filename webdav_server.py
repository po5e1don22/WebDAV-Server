from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from cheroot import wsgi
from wsgidav.dc.base_dc import BaseDomainController

from auth_loader import auth_loader, check_credentials

class CustomDomainController(BaseDomainController):

    def get_realm(self):
        return "WebDAV"
    
    def get_domain_realm(self, path_info, environ):
        return self.get_realm()
    
    def require_authentication(self, realmname, environ):
        return True


    def basic_auth_user(self, realmname,  username, password, environ,):
        print(f"[auth] Login attempt: {username}:{password}")
        user = check_credentials(username, password)
        if not user:
            print("[auth] ❌ Invalid credentials")
            return None
        print(f"[auth] ✅ Authenticated user: {username}")
        return username

    def supports_http_digest_auth(self):    
        return False
        
    def is_authenticated(self, realmname, environ):
        return environ.get("http_authenticator.username")

    def authorize(self, realmname, environ, username):
        return True  # all authenticated users are authorized

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
        "http_authenticator": {
            "domain_controller": CustomDomainController,
            "accept_basic": True,
            "accept_digest": False,
            "default_to_digest": False,
        },
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
