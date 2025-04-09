# extensions.py
from flask_mongoengine import MongoEngine
from google_recaptcha_flask import ReCaptcha

db = MongoEngine()
recaptcha = ReCaptcha()