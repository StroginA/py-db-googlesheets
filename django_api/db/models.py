from django.db import models

class Order(models.Model):
    orderId = models.IntegerField("Order ID")
    costUSD = models.FloatField("Cost, $")
    costRUB = models.FloatField("Cost, RUB")
    deliveryDate = models.DateField("Delivery Date")
    class Meta:
        managed = True

    def __str__(self):
        return self.orderId
