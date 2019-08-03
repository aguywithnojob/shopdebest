from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images',default='')
    rating = models.IntegerField(default=3)
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=50)
    items_json = models.CharField(max_length = 5000)
    amount = models.CharField(max_length=50 ,default='0')
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=300)

    def __str__(self):
        return self.name

class orderUpdate(models.Model):
    update_name = models.CharField(max_length=300,default='')
    update_desc = models.CharField(max_length=3000,default='')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_name
