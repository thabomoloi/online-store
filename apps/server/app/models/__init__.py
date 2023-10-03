from flask_sqlalchemy.model import DefaultMeta
from app.extensions import db

BaseModel: DefaultMeta = db.Model
