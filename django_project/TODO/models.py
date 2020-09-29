from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class TO_DO_ITEM(models.Model):
    TEAMS_CHOICES = (
        ('IT-POSTPAID', 'IT-Postpaid'), ('IT-PREPAID', 'IT-Prepaid'),
        ('IT', 'IT'),
        ('FINANCE', 'Finance'), ('RA', 'RA')
    )
    STATUS_CHOICES = (
        ('STARTED', 'Started'),
        ('WORKING', 'Working'),
        ('TRANSFERED', 'Transfered'),
        ('DONE', 'Done'),
        ('Suspended', 'SUSPENDED'),
        ('WAITING', 'Waiting'),
    )
    SOURCE_CHOICES = (
        ('IT', 'it'),
        ('SHOPS', 'Shops'),
        ('RA', 'ra'),
        ('FINANCE', 'Finance'),
        ('OFFICE', 'Office')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User, related_name='created_by', on_delete=models.DO_NOTHING)
    assigned_to = models.OneToOneField(
        User, related_name='assigned_to', on_delete=models.DO_NOTHING)
    assigned_team = models.CharField(
        max_length=50, choices=TEAMS_CHOICES, default='IT-POSTPAID')
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='STARTED')
    source = models.CharField(
        max_length=30, choices=SOURCE_CHOICES, default='IT')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('to_do_item', kwargs={'pk': self.pk})
