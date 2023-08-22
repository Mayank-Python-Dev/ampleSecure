import uuid
from django.db import models
from tasks.models import (
    TaskForFieldExecutive
)

# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class CaseInquiryForm(BaseModel):
    
