### csvs/views.py ###

# Django
from django.contrib.auth.models import User
from django.shortcuts import render

# Local
from .models import Csv
from .forms import CsvModelForm

from sales.models import Sale

import csv

# Upload file view
def upload_fileView(request):
  title = 'upload file'
  form = CsvModelForm(request.POST or None, request.FILES or None)
  if form.is_valid():
    form.save()
    form = CsvModelForm()
    obj = Csv.objects.get(activated=False)
    with open(obj.file_name.path, 'r') as f:
      reader = csv.reader(f)
      for i, row in enumerate(reader):
        if i == 0:
          pass
        else:
          product = row[1].upper()
          user = User.objects.get(username=row[3])
          Sale.objects.create(
            product = product,
            quantity = int(row[2]),
            salesman = user,
          )
          # print(row)
          # print(type(row))
      obj.activated=True
      obj.save()
  context = {
    'title': title,
    'form': form
  }
  return render(request, 'csvs/upload.html', context)