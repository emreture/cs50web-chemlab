from django.db import models
from customers.models import Customer

# Create your models here.


class TestMethod(models.Model):
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    unit = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.number} {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=16)
    tests = models.ManyToManyField(TestMethod, related_name="products")

    def __str__(self):
        return f"{self.name}"


class Sample(models.Model):
    number = models.IntegerField()
    receipt_date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="samples")
    sampling_date = models.DateTimeField(blank=True, null=True)
    sampling_point = models.CharField(max_length=64, blank=True)
    report_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.number} {self.product} {self.customer}"


class Result(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.DO_NOTHING, related_name="results")
    test_method = models.ForeignKey(TestMethod, on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.sample.number} {self.test_method.name} {self.result} {self.test_method.unit}"
