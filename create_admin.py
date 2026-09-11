"""Create an EstateHub administrator from the command line only."""
import argparse
from getpass import getpass

from app import create_app, db
from app.models import User


def main():
    parser = argparse.ArgumentParser(description="Create an EstateHub admin account.")
    parser.add_argument("username")
    parser.add_argument("email")
    parser.add_argument("--full-name", default="")
    parser.add_argument("--phone", default="")
    args = parser.parse_args()

    password = getpass("Password (at least 8 characters): ")
    if len(password) < 8:
        parser.error("Password must be at least 8 characters long.")
    if "@" not in args.email:
        parser.error("Enter a valid email address.")

    app = create_app()
    with app.app_context():
        if User.query.filter((User.username == args.username) | (User.email == args.email.lower())).first():
            parser.error("That username or email is already registered.")
        admin = User(username=args.username, email=args.email.lower(), full_name=args.full_name or None, phone=args.phone or None, role="admin")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
    print(f"Admin '{args.username}' created successfully.")


if __name__ == "__main__":
    main()
