from django.db import models
from users.models import CustomUser  # Updated import
from django.conf import settings

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'seller'})
    shop_name = models.CharField(max_length=120)
    address   = models.TextField(blank=True)
    def __str__(self): return self.shop_name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

    @staticmethod
    def ensure_default_categories():
        default_names = ['Food', 'Toy', 'Cloth', 'Medicine', 'Carrier']
        for name in default_names:
            Category.objects.get_or_create(name=name)

class Product(models.Model):
    name   = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    stock  = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image  = models.ImageField(upload_to="products/", blank=True)
    def __str__(self): return self.name

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role':'user'})
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")       # pending/shipped/delivered
    payment_status = models.CharField(max_length=20, default="unpaid") # unpaid/paid
    def __str__(self): return f"Order #{self.id}"

class OrderItem(models.Model):
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty     = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty     = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receipts')
    pdf = models.FileField(upload_to='receipts/')
    created_at = models.DateTimeField(auto_now_add=True)
    order_summary = models.TextField(blank=True)  # Optional: store summary for quick display

    def __str__(self):
        return f"Receipt #{self.id} for {self.user.username}"
