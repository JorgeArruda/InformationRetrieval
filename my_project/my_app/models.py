from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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


class Documents(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    tokens = models.TextField(blank=True, null=True)  # This field type is a guess.
    qtStopwords = models.IntegerField(db_column='qtStopwords', blank=True, null=True)  # Field name made lowercase.
    qtStopwordsTotal = models.IntegerField(db_column='qtStopwordsTotal', blank=True, null=True)  # Field name made lowercase.
    qtAdverbios = models.IntegerField(db_column='qtAdverbios', blank=True, null=True)  # Field name made lowercase.
    qtAdverbiosTotal = models.IntegerField(db_column='qtAdverbiosTotal', blank=True, null=True)  # Field name made lowercase.
    qtToken = models.IntegerField(db_column='qtToken', blank=True, null=True)  # Field name made lowercase.
    qtTokenTotal = models.IntegerField(db_column='qtTokenTotal', blank=True, null=True)  # Field name made lowercase.
    tf = models.TextField(blank=True, null=True)  # This field type is a guess.
    tfLog = models.TextField(db_column='logNormalization', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tfDouble = models.TextField(db_column='doubleNormalization', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    max = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'documents'


class Global(models.Model):
    words = models.TextField(blank=True, null=True)  # This field type is a guess.
    qtStopwords = models.IntegerField(db_column='qtStopwords', blank=True, null=True)  # Field name made lowercase.
    qtAdverbios = models.IntegerField(db_column='qtAdverbios', blank=True, null=True)  # Field name made lowercase.
    qtTokens = models.IntegerField(db_column='qtTokens', blank=True, null=True)  # Field name made lowercase.
    qtDocument = models.TextField(db_column='qtDocument', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    idf = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'global'



class Package(models.Model):
    idpackages = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, default="", null=False)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False
        db_table = 'packages'
