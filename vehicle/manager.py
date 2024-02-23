from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
   
    def create_user(self,email,password=None,**extraFields):
        if not email:
            raise ValueError('The Email must be set')
        email=self.normalize_email(email)
        user = self.model(email=email,**extraFields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email, password=None, **extraFields):
        extraFields.setdefault('is_staff',True)
        extraFields.setdefault('is_superuser',True)
        extraFields.setdefault('is_active',True)

        if extraFields.get( 'is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extraFields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(email,password,**extraFields)