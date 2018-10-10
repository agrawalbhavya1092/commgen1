from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

class UsersRoles(models.Model):
    user = models.ForeignKey('User',on_delete = models.CASCADE,db_column = 'CG_UM_ALTER_EMPLID')
    group = models.ForeignKey('Group',on_delete = models.CASCADE,db_column = 'CG_UM_ROLE_ID')
    class Meta:
        db_table = 'CM_User_roles_mapping_tbl'

class RolesPermissions(models.Model):
    group = models.ForeignKey('Group',on_delete = models.CASCADE,db_column = 'CG_ROLE_ID')
    permissions = models.ForeignKey('Permissions',on_delete = models.CASCADE,db_column = 'CG_PERMISSION_ID')

    class Meta:
        db_table = 'CM_role_perm_mapping_tbl'


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    # is_superuser = models.BooleanField(
    #     _('superuser status'),
    #     default=False,
    #     help_text=_(
    #         'Designates that this user has all permissions without '
    #         'explicitly assigning them.'
    #     ),
    # )
    groups = models.ManyToManyField(
        'Group',
        through = 'UsersRoles',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    # user_permissions = models.ManyToManyField(
    #     'Permissions',
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     related_name="user_set",
    #     related_query_name="user",
    # )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

# accounts.models.py

class UserManager(BaseUserManager):
    def create_user(self, email, emp_id=None,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            emp_id=emp_id
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,emp_id, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            emp_id=emp_id,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,emp_id,password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            emp_id=emp_id,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    TITLE_CHOICES = (('Mr.','Mr'),('Mrs.','Mrs'),('Ms.','Ms'),)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_column = 'CG_UM_EMAIL'
    )
    first_name = models.CharField(_('first name'), max_length=255, blank=True,db_column = 'CG_UM_FIRST_NAME')
    pref_first_name = models.CharField(_('preferred first name'), max_length=255, blank=True,db_column = 'CG_UM_PREF_FIRST_NAME')
    emp_id = models.CharField(max_length=10, blank=True,db_column = 'CG_UM_ALTER_EMPLID',primary_key=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True,db_column = 'CG_UM_LAST_NAME')
    pref_last_name = models.CharField(_('preferred last name'), max_length=255, blank=True,db_column = 'CG_UM_PREF_LAST_NAME')
    middle_name = models.CharField(_('middle name'), max_length=255, blank=True,db_column = 'CG_UM_MIDDLE_NAME')
    title = models.CharField(_('title'), max_length=5, blank=True,choices = TITLE_CHOICES, db_column = 'CG_UM_TITLE')
    pref_language = models.CharField(_('preferred language'), max_length=3, blank=True,db_column = 'CG_UM_PREF_LANG')
    active = models.BooleanField(default=True,db_column = 'CG_UM_STATUS')
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['emp_id'] # Email & Password are required by default.


    objects = UserManager()


    def get_full_name(self):
        # The user is identified by their email address
        return ' '+self.first_name+' '+self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    class Meta:
        db_table = 'CM_User_Prfl_tbl'


class PermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(app_label, model),
        )


class Permissions(models.Model):
    id = models.IntegerField(_('id'),primary_key=True,db_column = 'CG_PERMISSION_ID')
    name = models.CharField(_('name'), max_length=255,db_column = 'CG_PERMISSION_NAME')
    status = models.CharField(_('status'), max_length=20,blank=True,db_column = 'CG_PERMISSION_STATUS')
    description = models.TextField(_('description'),blank = True,db_column = 'CG_PERMISSION_DESCRIPTION')    
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
    )
    codename = models.CharField(_('codename'), max_length=100)
    objects = PermissionManager()

    class Meta:
        db_table = 'CM_permission_tbl'
        # verbose_name_plural = _('permissions')
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model',
                    'codename')

    def __str__(self):
        return "%s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name,
        )

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    id = models.IntegerField(primary_key = True,db_column = 'CG_ROLE_ID')
    name = models.CharField(_('name'), max_length=255, unique=True,db_column = 'CG_ROLE_NAME')
    status = models.CharField(_('status'), max_length=20,blank=True,db_column = 'CG_ROLE_STATUS')
    description = models.TextField(_('description'),blank = True,db_column = 'CG_ROLE_DESCRIPTION')
    permissions = models.ManyToManyField(
        'Permissions',
        through = 'RolesPermissions',
        # verbose_name=_('permissions'),
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        db_table = 'CM_role_tbl'
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        db_table = 'Role'


