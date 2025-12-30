from django.db import models
from django.conf import settings


class Seller(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now=True),
    business_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

def seller_document_path(instance, filename):
    # dynamic path based on seller's business name
    # sanitize business name to avoid path issues
    safe_name = "".join([c for c in instance.seller.business_name if c.isalnum() or c in (' ', '-', '_')]).strip()
    return f'seller_docs/{safe_name}/{filename}'

class SellerDocument(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to=seller_document_path)
    doc_type = models.CharField(max_length=100, help_text="e.g. ID, Business License")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} for {self.seller.business_name}"


