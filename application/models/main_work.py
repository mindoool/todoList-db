from application import db
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class MainWork(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    items = db.Column(db.String(1000))
    due = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    completed_time = db.Column(db.DateTime, default=db.func.current_timestamp())