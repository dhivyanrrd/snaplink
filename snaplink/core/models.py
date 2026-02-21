from django.db import models
from django.contrib.auth.models import User
import random
import string
class ShortURL(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    original_url=models.URLField(max_length=500)
    short_code=models.CharField(max_length=10,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        if not self.short_code:
            characters=string.ascii_letters +string.digits
            self.short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args,**kwargs)   
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:30]}"

class ClickAnalytics(models.Model):
    short_url=models.ForeignKey(ShortURL,on_delete=models.CASCADE,related_name='click')
    clicked_at=models.DateTimeField(auto_now_add=True)
    ip_address=models.GenericIPAddressField(null=True,blank=True)
    device_type=models.CharField(max_length=20,default='unknown')

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.clicked_at}"
