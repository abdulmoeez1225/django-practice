from django.db import models


# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)


class Product(models.Model):
    # sku = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=225)
    description = models.TextField()
    print = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT)
    # by default, it will generate the product_set field in promotion table
    # if you want to customize the name then you have to add the related_name
    # promotions = models.ManyToManyField(Promotion, related_name='products')
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    uint_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # IF WE DELETE THE CUSTOMER WHICH IS PARENT THERE CHILD MODEL FILE WILL BE ALSO DELETED
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    # IF WE TRY TO DELETE THE CUSTOMER IT WILL NOT ALLOW US TO DELETE IT
    # WE SHOULD HAVE TO DELETE THEIR REFERENCE CHILD FIRST THEN DELETE THE PARENT
    # customer = models.OneToOneField(Customer, on_delete=models.PROTECT)

    # IF WE DELETE THE CUSTOMER WHICH IS PARENT THERE CHILD MODEL FIELD WILL BE SET TO NULL
    # customer = models.OneToOneField(Customer, on_delete=models.SET_NULL,primary_key=True)

    # IF WE WANT TO MAKE THE FIELD BY DEFAULT AS PRIMARY KEY THEN WE ADD primary_key
    # customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, primary_key=True)

    # for the one to many relation the we have to add ForeginKey
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
