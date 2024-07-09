from django.db import models
from django.core.cache import cache



class ProductQuerySet(models.QuerySet):
    def all(self):
        cache_key = "all_products"

        products = cache.get(cache_key)

        if products is None:
            products = super().all()
            cache.set(cache_key, products)

        return products


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
