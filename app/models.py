from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import secrets

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(64), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))

    api_key = db.Column(db.String(64), unique=True, nullable=True, default=lambda: secrets.token_hex(32))

    def generate_api_key(self):
        raw_key = secrets.token_hex(32)
        self.api_key = f"amn={raw_key}"
        db.session.commit()

    def generate_verification_token(self):
        self.verification_token = str(uuid.uuid4())
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
