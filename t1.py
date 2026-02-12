import hashlib

def is_authenticated(user):
    if not user:
        return False
    token = user.get("token")
    if not token:
        return False
    return token.startswith("AUTH")

def log_access(user):
    print(f"Access attempt by {user.get('name')}")

def process_request(user):
    log_access(user)
    if is_authenticated(user):
        return "Access Granted"
    return "Access Denied"

def audit_trail(user):
    print("Audit:", user)

def main():
    user = {"name": "Vijay", "token": "AUTH123"}
    result = process_request(user)
    audit_trail(user)
    print(result)

if __name__ == "__main__":
    main()
