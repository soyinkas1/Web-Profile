import datetime
from app import db

class ContactTable(db.Model):
    __tablename__='contact_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(1000), unique=False, nullable=True)
    message = db.Column(db.String(), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.email}', name='{self.name}')>"