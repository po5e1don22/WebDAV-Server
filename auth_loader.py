import os
import yaml

USERS_FILE = "config/users.yaml"
DEVICE_ID_FILE = "config/.device_uuid"

#returns a list of users or creates a new users.yaml if it does not exist
def auth_loader():
    if not os.path.exists(USERS_FILE):
        print("[auth] users.yaml not found, creating default admin user.")

        default_user = {
            "users": [
                {
                    "username": "admin",
                    "password": "admin",
                }
            ]
        }

        with open(USERS_FILE, "w") as f:
            yaml.dump(default_user, f)

        print(f"[auth] Default user created: username=admin, password=admin")

    with open (USERS_FILE, "r") as f:
        return yaml.safe_load(f)
    
#Check if provided credentials match any user.
def check_credentials(username, password):
    data = auth_loader()

    for user in data.get("users", []):
        if user["username"] == username and user["password"] == password:
            return user
    return None