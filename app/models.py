from django.db import models

# Create your models here.
class UserProfile(models.Model):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)  

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"