from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
	    return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
            on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    available=models.BooleanField(default=True)
    stock =models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        print(reverse('products:product_detail', args=[self.id, self.slug]))
        print('ahí lo imprimí')
        return reverse('products:product_detail', args=[self.id, self.slug])

