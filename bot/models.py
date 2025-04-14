from django.db import models

# Create your models here.


class User(models.Model):
    referal_count = models.IntegerField(default=0)
    chat_id = models.BigIntegerField(null=True, blank=True, default=0)
    interface_language = models.CharField(max_length=10)
    photo = models.CharField(max_length=255, null=True, blank=True, )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True,
                            choices=[('ADMIN', 'Admin'), ('USER', 'Foydalanuvchi')],
                            default='USER')
    def __str__(self):
        return self.chat_id


class Referral(models.Model):
    referrer_id = models.BigIntegerField()
    referred_user_id = models.BigIntegerField()


class Otziv(models.Model):
    RATING=[
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4),
        ('5',5)
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.CharField(max_length=1,choices=RATING)
    opinion=models.TextField(null=True,blank=True)
    objection=models.TextField(null=True,blank=True)
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.opinion

class PdfFileId(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file_id=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_id