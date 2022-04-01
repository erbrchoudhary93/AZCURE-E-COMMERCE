from email.policy import default
from unicodedata import category
from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category= models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=1000)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/image",default="")
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email= models.CharField(max_length=5,default="")
    phone=models.CharField(max_length=50,default="")
    desc=models.CharField(max_length=10000,default="")
 
    
    def __str__(self):
        return self.name
    
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email= models.CharField(max_length=111,default="")
    address1= models.CharField(max_length=500,default="")
    address2= models.CharField(max_length=500,default="")
    city= models.CharField(max_length=50,default="")
    state= models.CharField(max_length=50,default="")
    zip_code=models.CharField(max_length=20)
    phone=models.CharField(max_length=50,default="")
    razorpay_order_id=models.CharField(max_length=500,default="")
    razorpay_payment_id=models.CharField(max_length=500,default="")
    razorpay_signature=models.CharField(max_length=500,default="")
   
   
    
    def __str__(self):
        return self.name
    
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.CharField(max_length=500,default="")
    update_desc=models.CharField(max_length=5000)
    timestep=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:20]+"...."
    
