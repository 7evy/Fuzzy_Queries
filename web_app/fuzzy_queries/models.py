# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from numpy.lib.function_base import sinc


class Immo(models.Model):

    type = models.CharField(max_length=25, blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    pieces = models.SmallIntegerField(blank=True, null=True)
    chambres = models.SmallIntegerField(blank=True, null=True)
    loyer = models.SmallIntegerField(blank=True, null=True)
    meuble = models.BooleanField(blank=True, null=True)
    jardin = models.BooleanField(blank=True, null=True)
    terrasse = models.BooleanField(blank=True, null=True)
    dist_centre = models.SmallIntegerField(blank=True, null=True)
    dist_transport = models.SmallIntegerField(blank=True, null=True)
    dist_commerce = models.SmallIntegerField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'immo'
