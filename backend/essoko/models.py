from django.db import models


# GoDown Collection
class GoDown(models.Model):
    id = models.IntegerField(primary_key=True)

    godown_title = models.CharField(max_length=200, blank=True)
    godown_info = models.CharField(max_length=200, blank=True)

    latitude = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=200, blank=True)

    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'go_downs'


