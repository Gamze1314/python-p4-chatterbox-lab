from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
#import datetime
from sqlalchemy import func

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    #body
    body = db.Column(db.String, nullable=False)
    #username
    username = db.Column(db.String, nullable=False)
    #created at
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    #updated at
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


