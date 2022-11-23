import uuid
from django.db import models
from .Person import Person
from simple_history.models import HistoricalRecords


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True, null=False, default="")
    updatedBy = models.ForeignKey("Person", on_delete=models.DO_NOTHING, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    updatedDate = models.DateTimeField(auto_now=True, blank=True)
    history = HistoricalRecords(user_model=Person)

    @property
    def _history_user(self):
        return self.updatedBy

    @_history_user.setter
    def _history_user(self, value):
        self.updatedBy = value
