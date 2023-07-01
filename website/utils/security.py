
from itsdangerous import URLSafeTimedSerializer

from website import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])