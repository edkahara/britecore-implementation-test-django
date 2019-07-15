from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    """
    Product model. Defines columns for the product table.
    """

    name = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    Client model. Defines columns and relationships for the client table.
    """

    name = models.TextField()

    def __str__(self):
        return self.name


class Request(models.Model):
    """
    Client model. Defines columns for the request table.
    """

    title = models.CharField(max_length=50)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    priority = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    targetDate = models.DateField()
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s %s" % (self.title, self.client, self.priority)
