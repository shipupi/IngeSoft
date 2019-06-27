from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class  Product(models.Model):
	name = models.CharField(max_length=100)
	# email = models.EmailField()
	description = models.CharField(max_length=1000)
	price =models.IntegerField()
	stock =models.IntegerField()
	image =models.ImageField(upload_to="images/")
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.name