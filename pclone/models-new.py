# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Boards(models.Model):
    bidpreformat = models.AutoField(primary_key=True)
    bid = models.CharField(
        unique=True, 
        max_length=4,
        db_default=models.Value(
            "LPAD(bidpreformat::text, 4, '0')", 
            output_field=models.CharField()))
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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    picidpreformat = models.AutoField(primary_key=True)
    picid = models.CharField(
        unique=True, 
        max_length=4,
        db_default=models.Value(
            "LPAD(picidpreformat::text, 4, '0')", 
            output_field=models.CharField()))
    pic = models.ImageField(null=True, blank=True, upload_to="images/")
    # won't be created until we upload the first image
    # images is a folder inside 'media' defined in setting
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pictures'


class Pins(models.Model):
    pinidpreformat = models.AutoField(primary_key=True)
    pinid = models.CharField(
        unique=True, 
        max_length=4,
        db_default=models.Value(
            "LPAD(pinidpreformat::text, 4, '0')", 
            output_field=models.CharField()))
    picid = models.ForeignKey(Pictures, models.DO_NOTHING, db_column='picid', blank=True, null=True)
    bid = models.ForeignKey(Boards, models.DO_NOTHING, db_column='bid', blank=True, null=True)
    original = models.BooleanField(blank=True, null=True)
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pins'

class Pintags(models.Model):
    tidpreformat = models.AutoField(primary_key=True)
    # tid = models.CharField(
    #     unique=True, 
    #     max_length=4,
    #     db_default=models.Value(
    #         "LPAD(tidpreformat::text, 4, '0')", 
            # output_field=models.CharField()))
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


class Users(models.Model):
    uidpreformat = models.AutoField(primary_key=True)
    uid = models.CharField(
        unique=True, 
        max_length=4,
        db_default=models.Value(
            "LPAD(uidpreformat::text, 4, '0')", 
            output_field=models.CharField()))
    username = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=50)
    # password = models.CharField(max_length=20)
    regtime = models.DateTimeField(blank=True, null=True)
    intro = models.CharField(blank=True, null=True, max_length=500)
    
    class Meta:
        managed = True
        db_table = 'users'

class Streams(models.Model):
    sidpreformat = models.AutoField(primary_key=True)
    sid = models.CharField(
        unique=True, 
        max_length=4,
        db_default=models.Value(
            "LPAD(sidpreformat::text, 4, '0')", 
            output_field=models.CharField()))
    sname = models.CharField(max_length=20, blank=True, null=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    regtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'streams'