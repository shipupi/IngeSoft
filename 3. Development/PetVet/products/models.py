from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class  Products(models.Model):
	name = models.CharField(max_length=100)
	# email = models.EmailField()
	descripcion = models.CharField(max_length=1000)
	precio =models.IntegerField()
	stock =models.IntegerField()
	imagen =models.CharField(max_length=1000)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.name