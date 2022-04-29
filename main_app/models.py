from django.db import models
from django.contrib.auth.models import User


class HistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.PositiveBigIntegerField()
    patient_name = models.CharField(max_length=50)
    pregancies = models.IntegerField()
    glucose = models.IntegerField()
    bp = models.IntegerField()
    skin = models.IntegerField()
    insulin = models.IntegerField()
    bmi = models.FloatField()
    dpf = models.FloatField()
    age = models.IntegerField()
    result = models.CharField(max_length=10)
    datetime = models.CharField(max_length=50)

    def __str__(self):
        return str(self.patient_id) + ": " + str(self.result)
    
    class Meta:
        db_table = 'HistoryModel'
