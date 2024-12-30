from demo_app1.app.extensions import db

class HeartPredictions(db.Model):
    __tablename__='heart_predictions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    sex = db.Column(db.Integer, unique=False, nullable=False)
    cp = db.Column(db.Integer, unique=False, nullable=False)
    trestbps = db.Column(db.Integer, unique=False, nullable=False)
    chol = db.Column(db.Integer, unique=False, nullable=False)
    fbs = db.Column(db.Integer, unique=False, nullable=False)
    restecg = db.Column(db.Integer, unique=False, nullable=False)
    thalach = db.Column(db.Integer, unique=False, nullable=False)
    exang = db.Column(db.Integer, unique=False, nullable=False)
    oldpeak = db.Column(db.Float, unique=False, nullable=False)
    slope = db.Column(db.Integer, unique=False, nullable=False)
    ca = db.Column(db.Integer, unique=False, nullable=False)
    thal = db.Column(db.Integer, unique=False, nullable=False)
    target = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"<Heart Diesease Prediction(id={self.id}, name='{self.email}', age='{self.age}')>"