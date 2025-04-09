from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_recaptcha import ReCaptcha

mail = Mail()
db = MongoEngine()
recaptcha = ReCaptcha()