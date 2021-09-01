from flask import Flask
from application import db

class Users(db.Model):
    userName = db.Column(db.String(50), primary_key=True)

    def as_dict(self):
        return {"userName":self.userName}
