# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
#
#
# class Clients(models.Model):
#     # id = models.AutoField(unique=True)
#     name = models.TextField()
#
#     class Meta:
#         managed = False
#         db_table = 'clients'
#
#
# class Durations(models.Model):
#     # id = models.AutoField(unique=True)
#     client_id = models.IntegerField()
#     equipment_id = models.IntegerField()
#     start = models.TextField()
#     stop = models.TextField()
#     mode_id = models.IntegerField()
#     minutes = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'durations'
#
#
# class Equipment(models.Model):
#     # id = models.AutoField()
#     client_id = models.IntegerField()
#     name = models.TextField()
#
#     class Meta:
#         managed = False
#         db_table = 'equipment'
#
#
# class Modes(models.Model):
#     # id = models.AutoField(unique=True)
#     name = models.TextField(unique=True, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'modes'
