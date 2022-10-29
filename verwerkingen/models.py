# verwerkingen/models.py

import uuid

# Django
from django.db import models
from django.urls import reverse

# Gemeente model
class Gemeente(models.Model):
  naam = models.CharField('gemeente-naam', max_length=100)
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'gemeenten'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Verordening model
class Verordening(models.Model):
  naam         = models.CharField('verordening-naam', max_length=100)
  beschrijving = models.CharField('beschrijving', max_length=200, blank=True)
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'verordeningen'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Verantwoordelijke model
class Verantwoordelijke(models.Model):
  naam = models.CharField('verantwoordelijke', max_length=100)
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'verantwoordelijken'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Team model
class Team(models.Model):
  naam = models.CharField('teamnaam', max_length=100)
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'teams'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Grondslag model
class Grondslag(models.Model):
  naam         = models.CharField('grondslag naam', max_length=100)
  beschrijving = models.CharField('beschrijving', max_length=200, blank=True)
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'grondslagen'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Persoonsgegevens model
class Persoonsgegeven(models.Model):
  type         = models.CharField('type persoonsgegeven', max_length=100)
  beschrijving = models.CharField('beschrijving', max_length=200, blank=True)
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering = ['type']
    verbose_name_plural = 'persoonsgegevens'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.type

# Verwerker model
class Verwerker(models.Model):
  naam           = models.CharField('verwerker naam', max_length=100)
  beschrijving   = models.CharField('beschrijving', max_length=200, blank=True)
  # secundair
  uuid           = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at       = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at         = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created        = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'verwerkers'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Verwerkersovereenkomst model
class Verwerkersovereenkomst(models.Model):
  naam         = models.CharField('verwerkersovereenkomst naam', max_length=100)
  beschrijving = models.CharField('beschrijving', max_length=200, blank=True)
  pdf          = models.FileField(upload_to='documenten/verwerkingsovereenkomsten/', blank=True)
  vwo_start    = models.DateField('ingangsdatum verwerkersovereenkomst', blank=True)
  vwo_end      = models.DateField('einddatum verwerkersovereenkomst', blank=True)
  extern       = models.BooleanField('Extern', default=False)
  # relaties
  verwerker    = models.ForeignKey('verwerker', on_delete=models.CASCADE, related_name='verwerkersovereenkomsten')
  verwerkingen = models.ManyToManyField('verwerking', related_name='verwerkersovereenkomsten')
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'verwerkersovereenkomsten'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Betrokkene model
class Betrokkene(models.Model):
  naam              = models.CharField('betrokkene naam', max_length=100)
  beschrijving      = models.CharField('beschrijving', max_length=200, blank=True)
  # relaties
  persoonsgegevens  = models.ManyToManyField('persoonsgegeven', blank=True, related_name='betrokkenen')
  # secundair
  uuid              = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at          = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at            = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created           = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'betrokkenen'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Ontvanger model
class Ontvanger(models.Model):
  naam         = models.CharField('ontvanger', max_length=100)
  beschrijving = models.CharField('beschrijving', max_length=200, blank=True)
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'ontvangers'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Hoofdproces model
class Hoofdproces(models.Model):
  naam = models.CharField('hoofdproces', max_length=100)
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'hoofdprocessen'
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Verwerking model
class Verwerking(models.Model):
  naam              = models.CharField('verwerkingsactiviteit', max_length=200)
  doel              = models.TextField('doel van verwerking', max_length=250)
  reden_grondslag   = models.TextField('reden van grondslag', max_length=250, blank=True)
  bewaartermijn     = models.CharField('bewaartermijn', max_length=200)
  buitenEUgedeeld   = models.BooleanField('buiten de EU gedeeld', default=False)
  dpia_uitgevoerd   = models.BooleanField('DPIA uitgevoerd', default=False)
  # relaties
  gemeente          = models.ManyToManyField('gemeente', blank=True, related_name='verwerkingen')
  verordening       = models.ManyToManyField('verordening', blank=True, related_name='verwerkingen')
  verantwoordelijke = models.ForeignKey('verantwoordelijke', null=True, blank=True, on_delete=models.SET_NULL, related_name='verwerkingen')
  hoofdproces       = models.ForeignKey('hoofdproces', null=True, blank=True, on_delete=models.SET_NULL, related_name='verwerkingen')
  team              = models.ManyToManyField('team', blank=True)
  grondslag         = models.ForeignKey('grondslag', null=True, blank=True, on_delete=models.SET_NULL, related_name='verwerkingen')
  verwerkers        = models.ManyToManyField('verwerker', blank=True, related_name='verwerkingen')
  betrokkenen       = models.ManyToManyField('betrokkene', blank=True, related_name='verwerkingen')
  ontvangers        = models.ManyToManyField('ontvanger', blank=True, related_name='verwerkingen')
  # secundair
  uuid              = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at          = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at            = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created           = models.DateTimeField(auto_now_add=True, help_text='Date of registration')
  class Meta:
    ordering            = ['naam']
    verbose_name_plural = 'verwerkingen'
  # create absolute url
  def get_absolute_url(self):
    return reverse('show-verwerking', args=[self.uuid])
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam
