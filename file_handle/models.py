from django.db import models
from django.contrib.auth.models import User
# Create your models here.
User.USERNAME_FIELD = 'email'
User._meta.get_field('email')._unique = True
User.REQUIRED_FIELDS = ['username']

USER_TYPE = (
    ('UPLOADER', 'File Uploader'),
    ('RECEPIENT', 'File Recepient'),
    ('NONE', 'Not Assigned')
)


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        default='NONE', choices=USER_TYPE, max_length=9)

    def __str__(self):
        return self.user.email


class FileManager(models.Model):
    file_uploader = models.ForeignKey(
        CustomUser, limit_choices_to={'user_type': 'UPLOADER'}, on_delete=models.CASCADE, related_name='uploader')
    file_recepient = models.ForeignKey(
        CustomUser, limit_choices_to={'user_type': 'RECEPIENT'}, on_delete=models.CASCADE, related_name='recepient')
    file = models.FileField(upload_to="", blank=False, null=False)
