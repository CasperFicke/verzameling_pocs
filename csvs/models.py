### csvs/models.py ###

# Django
from django.db import models

# Create your models here.

# Csv model
class Csv(models.Model):
  file_name = models.FileField(upload_to='csvs')
  uploaded  = models.DateTimeField(auto_now_add=True, help_text='Date the csv-file was uploaded')
  activated = models.BooleanField(default=False)

  # functie om csv-file in de admin web-pagina te kunnen presenteren
  def __str__(self):
    #return self.file_name
    return f"File id: {self.id}"
