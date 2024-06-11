from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(_("quantity"))
    subtotal = models.FloatField(_("subtotal"))

    def __str__(self):
        return f"User Id: {self.user.id}|Product: {self.product.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Card(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="cards")
    card_name = models.CharField(_("Card Name"), max_length=120)
    card_number = models.CharField(_("Card Number"), max_length=16)
    expiry_date = models.DateField(_("Expiration Date"))
    cvv = models.CharField(_("CVV"), max_length=3)

    def __str__(self):
        return f"User Id: {self.user.id}|Card Number: {self.card_number}"


class Discount(models.Model):
    code = models.CharField(_("Code"), max_length=60)
    max_limit_price = models.FloatField(_("Max Limit Price"))
    percentage = models.FloatField(_("Percentage"))
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))

    def __str__(self):
        return self.code


class Branch(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    region = models.ForeignKey('common.Region', on_delete=models.CASCADE, related_name="branches")
    zip_code = models.CharField(_("Zip Code"), max_length=10)
    street = models.CharField(_("Street"), max_length=120)
    address = models.TextField(_("Address"))
    longitude = models.FloatField(_("Longitude"))
    latitude = models.FloatField(_("Latitude"))

    def __str__(self):
        return f"Name: {self.name}|Region: {self.region.name}"


class DeliveryTariff(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="delivery_tariffs")
    high = models.FloatField(_("High"))
    width = models.FloatField(_("Width"))
    weight = models.FloatField(_("Weight"))
    price = models.FloatField(_("Price"))
    regions = models.ManyToManyField('common.Region', related_name="delivery_tariffs")
    delivery_time = models.TimeField(_("Delivery Time"))

    def __str__(self):
        return f"Branch: {self.branch.name}|Price: {self.price}"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = "created", _("Created")
        IN_PROGRESS = "in_progress", _("In progress")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        FINISHED = "finished", _("Finished")

    class PaymentStatus(models.TextChoices):
        CREATED = "created", _("Created")
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        CANCELLED = "cancelled", _("Cancelled")

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        PAYME = "payme", _("Payme")
        CLICK = "click", _("Click")

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(_("Status"), max_length=60, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    items = models.ManyToManyField(CartItem, related_name="orders")
    total_price = models.FloatField(_("Total Price"))
    address = models.ForeignKey('accounts.UserAddress', on_delete=models.CASCADE, related_name="orders")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    payment_status = models.CharField(_("Payment Status"), max_length=60, choices=PaymentStatus.choices, null=True,blank=True)
    payment_method = models.CharField(_("Payment Method"), max_length=60, null=True, blank=True)
    delivery_tariff = models.ForeignKey(DeliveryTariff, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="orders")



