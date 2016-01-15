from application import db
from application.models.mixin import TimeStampMixin
from application.models.mixin import SerializableModelMixin


class InstantWork(db.Model, TimeStampMixin, SerializableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    is_completed = db.Column(db.Boolean, default=False)
    completed_time = db.Column(db.DateTime, default=db.func.current_timestamp())