from django.db import models
from django.conf import settings

# Create your models here.

class Seller(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

class SellerDocument(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='seller_docs/')
    doc_type = models.CharField(max_length=100, help_text="e.g. ID, Business License")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} for {self.seller.business_name}"
