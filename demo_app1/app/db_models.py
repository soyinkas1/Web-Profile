from demo_app1.app.extensions import db2

class HeartPredictions(db2.Model):
    __tablename__='heart_predictions'
    id = db2.Column(db2.Integer, primary_key=True)
    email = db2.Column(db2.String(120), unique=False, nullable=False)
    age = db2.Column(db2.Integer, unique=False, nullable=False)
    sex = db2.Column(db2.Integer, unique=False, nullable=False)
    cp = db2.Column(db2.Integer, unique=False, nullable=False)
    trestbps = db2.Column(db2.Integer, unique=False, nullable=False)
    chol = db2.Column(db2.Integer, unique=False, nullable=False)
    fbs = db2.Column(db2.Integer, unique=False, nullable=False)
    restecg = db2.Column(db2.Integer, unique=False, nullable=False)
    thalach = db2.Column(db2.Integer, unique=False, nullable=False)
    exang = db2.Column(db2.Integer, unique=False, nullable=False)
    oldpeak = db2.Column(db2.Float, unique=False, nullable=False)
    slope = db2.Column(db2.Integer, unique=False, nullable=False)
    ca = db2.Column(db2.Integer, unique=False, nullable=False)
    thal = db2.Column(db2.Integer, unique=False, nullable=False)
    target = db2.Column(db2.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"<Heart Diesease Prediction(id={self.id}, name='{self.email}', age='{self.age}')>"