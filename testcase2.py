import hashlib
import time
import random

class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.role = role
        self.login_attempts = 0
        self.locked = False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def increment_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 3:
            self.locked = True

    def reset_attempts(self):
        self.login_attempts = 0


class AuthSystem:
    def __init__(self):
        self.users = {}
        self.sessions = {}

    def register_user(self, username, password, role="user"):
        if username in self.users:
            raise Exception("User already exists")
        user = User(username, password, role)
        self.users[username] = user

    def authenticate(self, username, password):
        if username not in self.users:
            return False

        user = self.users[username]

        if user.locked:
            print("Account locked")
            return False

        if user.verify_password(password):
            user.reset_attempts()
            session_token = self.generate_session_token(username)
            self.sessions[session_token] = username
            return session_token
        else:
            user.increment_attempts()
            return False

    def generate_session_token(self, username):
        seed = f"{username}{time.time()}{random.randint(1,9999)}"
        return hashlib.sha256(seed.encode()).hexdigest()

    def validate_session(self, token):
        if token in self.sessions:
            return True
        return False

    def logout(self, token):
        if token in self.sessions:
            del self.sessions[token]

    def access_resource(self, token):
        if not self.validate_session(token):
            return "Access Denied"

        username = self.sessions[token]
        user = self.users[username]

        if user.role == "admin":
            return "Admin Access Granted"

        elif user.role == "user":
            return "User Access Granted"

        else:
            return "Guest Access"

    def system_status(self):
        total_users = len(self.users)
        active_sessions = len(self.sessions)
        locked_accounts = sum(1 for u in self.users.values() if u.locked)

        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "locked_accounts": locked_accounts
        }


def simulate_system():
    auth = AuthSystem()

    auth.register_user("vijay", "secure123", "admin")
    auth.register_user("guest", "guest123", "user")

    token = auth.authenticate("vijay", "secure123")

    if token:
        print(auth.access_resource(token))
    else:
        print("Authentication Failed")

    print(auth.system_status())


if __name__ == "__main__":
    simulate_system()
