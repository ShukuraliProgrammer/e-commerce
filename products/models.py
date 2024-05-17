from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import Media
from products.utitls import validate_rating
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(_("name"), max_length=255)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Category") # Bo'limlar
        verbose_name_plural = _("Categories")
        
    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    name = models.CharField(_("name"), max_length=255)
    price = models.FloatField(_("price")) # 2.03
    short_description = models.TextField(_("short description"))
    description = models.TextField(_("description"))
    quanttity = models.IntegerField(_("quantity"))
    instructions = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    in_stock = models.BooleanField(_("in stock"), default=True)
    brand = models.CharField(_("brand"), max_length=255)
    discount = models.IntegerField(_("discount"), help_text=_("in percentage"))
    thumbnail = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductColour(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colours")
    colour = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.id}|Colour: {self.colour.id}"
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.id}|Image: {self.image.id}"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    value = models.CharField(_("value"), max_length=255)

    def __str__(self):
        return f"Product: {self.product.id}|Size: {self.value}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    review = models.TextField(_("review"))
    rank = models.IntegerField(_("rank"), validators=[validate_rating])
    email = models.EmailField(_("email"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.id}|User: {self.user.id}"


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="wishlists")

    def __str__(self):
        return f"Product: {self.product.id}|User: {self.user.id}"