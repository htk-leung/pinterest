# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Boards(models.Model):
    bid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    bname = models.CharField(max_length=20, blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)
    frdonly = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'boards'


class Comments(models.Model):
    pk = models.CompositePrimaryKey('uid', 'pinid', 'regtime')
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    pinid = models.ForeignKey('Pins', models.DO_NOTHING, db_column='pinid')
    comment = models.CharField(max_length=250, blank=True, null=True)
    regtime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'comments'
        unique_together = (('uid', 'pinid', 'regtime'),)


class Follows(models.Model):
    pk = models.CompositePrimaryKey('uid', 'bid')
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    bid = models.ForeignKey(Boards, models.DO_NOTHING, db_column='bid')
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'follows'
        unique_together = (('uid', 'bid'),)


class Friends(models.Model):
    pk = models.CompositePrimaryKey('uid1', 'uid2')
    uid1 = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid1')
    uid2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid2', related_name='friends_uid2_set')
    frdonly = models.BooleanField(blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'friends'
        unique_together = (('uid1', 'uid2'),)


class Invitations(models.Model):
    pk = models.CompositePrimaryKey('uidfr', 'uidto', 'regtime')
    uidfr = models.ForeignKey('Users', models.DO_NOTHING, db_column='uidfr')
    uidto = models.ForeignKey('Users', models.DO_NOTHING, db_column='uidto', related_name='invitations_uidto_set')
    status = models.IntegerField(blank=True, null=True)
    regtime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'invitations'
        unique_together = (('uidfr', 'uidto', 'regtime'),)


class Likes(models.Model):
    pk = models.CompositePrimaryKey('uid', 'pinid')
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    pinid = models.ForeignKey('Pins', models.DO_NOTHING, db_column='pinid')
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'likes'
        unique_together = (('uid', 'pinid'),)


class Pictures(models.Model):
    picid = models.AutoField(primary_key=True)
    pic = models.ImageField(null=True, blank=True, upload_to="images/")
    # won't be created until we upload the first image
    # images is a folder inside 'media' defined in setting
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pictures'


class Pins(models.Model):
    pinid = models.AutoField(primary_key=True)
    picid = models.ForeignKey(Pictures, models.DO_NOTHING, db_column='picid', blank=True, null=True)
    bid = models.ForeignKey(Boards, models.DO_NOTHING, db_column='bid', blank=True, null=True)
    original = models.BooleanField(blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pins'

class Pintags(models.Model):
    tid = models.AutoField(primary_key=True)
    pinid = models.ForeignKey(Pins, models.DO_NOTHING, db_column='pinid', to_field='pinid')
    tag = models.CharField(max_length=50)
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pintags'
        # unique_together = (('pinid', 'tag'),)


class Streamboards(models.Model):
    pk = models.CompositePrimaryKey('sid', 'bid')
    sid = models.ForeignKey('Streams', models.DO_NOTHING, db_column='sid', to_field='sid')
    bid = models.ForeignKey(Boards, models.DO_NOTHING, db_column='bid')
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'streamboards'
        unique_together = (('sid', 'bid'),)


# class Users(models.Model):
#     uid = models.AutoField(primary_key=True)
#     username = models.CharField(unique=True, max_length=20)
#     email = models.CharField(unique=True, max_length=50)
#     # password = models.CharField(max_length=20)
#     regtime = models.DateTimeField(blank=True, null=True)
#     intro = models.CharField(blank=True, null=True, max_length=500)
    
#     class Meta:
#         managed = True
#         db_table = 'users'

class Users(AbstractUser):
    # Don't redefine username, email, password - inherited from AbstractUser!
    uid = models.AutoField(primary_key=True)
    intro = models.CharField(blank=True, null=True, max_length=500)
    regtime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'

class Streams(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=20, blank=True, null=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'streams'