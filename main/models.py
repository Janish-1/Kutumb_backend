from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobileno = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    dob = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=100)
    account_type = models.IntegerField(null=True)  # 1 is for volunteer , 2 is for member 3 is for Army member
    account_type_change_request = models.IntegerField(default=1,null=True,blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    otp = models.CharField(max_length=10,null=True, blank=True)
    blood_group = models.CharField(max_length=100,null=True, blank=True)
    pan_number = models.CharField(max_length=100,null=True, blank=True)
    batch = models.CharField(max_length=100,null=True, blank=True)
    batalian = models.CharField(max_length=100,null=True, blank=True)
    tax_benifit = models.BooleanField(default=False)
    adhaar = models.CharField(max_length=100,null=True,blank=True)
    awards = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.account_type_change_request not in [1, 2]:
            raise ValueError("Account type change request must be 1 or 2.")
        
        super().save(*args, **kwargs)

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=100,null=True,blank=True)
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    addeddateTime = models.DateTimeField(auto_now_add=True)
    addnpic = models.ImageField(upload_to='post_photos/',blank=True, null=True)
    update = models.TextField(null=True,blank=True)
    addnpic1 = models.ImageField(upload_to='post_photos/',blank=True, null=True)
    update1 = models.TextField(null=True,blank=True)
    addnpic2 = models.ImageField(upload_to='post_photos/',blank=True, null=True)
    update2 = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.comment

class Action(models.Model):   
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='action_icons/')
    order_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=12)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Image {self.id} - Added on {self.date_added}"    

class Request_Table(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    requested_for  = models.CharField(max_length=100)
    request_type = models.CharField(max_length=100)
    request_to_date = models.DateField(null=True, blank=True)
    requester_mobile_no = models.CharField(max_length=100)

class Transctions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    for_action = models.ForeignKey(Action, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=100)
    request_type = models.CharField(max_length=100)
    transction_id = models.IntegerField(null=True,blank=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=200,null=True,blank=True)
    payment_mode = models.CharField(max_length=100,null=True,blank=True)
    gateway = models.CharField(max_length=100,null=True,blank=True)
