import uuid
from django.db import models
from account.models import (
    Client
)
from django.utils.translation import gettext as _

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class IssuanceType(models.TextChoices):
    Pre_Issuance = "Pre Issuance"
    Post_Issuance = "Post Issuance"
    Not_Applicable = "Not Applicable"


class TypeOfCheck(models.TextChoices):
    Profile_Check = "Profile Check"
    Discreet_Check  = "Discreet Check"
    Mystery_Shopping = "Mystery Shopping"
    Doctor_Seeding = "Doctor Seeding"
    Account_Verification = "Account Verification"
    Document_Verification = "Document Verification"
    Number_Verification = "Number Verification"
    Mystery_Calling = "Mystery Calling"


class TypeOfVisit(models.TextChoices):
    Direct = "Direct"
    Appointment  = "Appointment"
    Discreet_Only = "Discreet Only"


class TurnAroundTime(models.TextChoices):
    WT = "WT"
    NA = "NA"
    OT = "OT"
    

class CaseStatus(models.TextChoices):
    Positive  = "Positive"
    Negative = "Negative"
    Highly_Negative = "Highly Negative"
    # InconclusiveReferred = "Inconclusive / Referred"
    Suspicious = "Suspicious"

class Case(BaseModel):
    client = models.ForeignKey(Client,related_name="client_cases",on_delete=models.CASCADE)
    issuance_type = models.CharField(_('Issuance Type'),max_length=64,choices=IssuanceType.choices)
    type_of_check = models.CharField(_('Type Of Check'),max_length=64,choices=TypeOfCheck.choices)
    type_of_visit = models.CharField(_('Type Of Visit'),max_length=64,choices=TypeOfVisit.choices)
    appointment_status = models.TextField(_('Appointment Status'),null=True,blank=True,default="")
    refered_by = models.CharField(_('Refered By'),max_length=255)
    in_date = models.DateField(_('In Date'),auto_now_add=False,editable=True)
    in_time = models.TimeField(_('In Time'),auto_now_add=False,editable=True)
    consider_date = models.DateField(_('Consider Date'),auto_now_add=False,editable=True)
    #Holiday
    due_date = models.DateField(_('Due Date'),auto_now_add=False,editable=True)
    out_date = models.DateField(_('Out Date'),auto_now_add=False,editable=True)
    delayed_reason = models.TextField(_('Delayed Reason'),null=True,blank=True,default="")
    turn_around_time = models.CharField(_('Turn Around Time'),max_length=64,choices=TurnAroundTime.choices)
    turn_around_time_in_days = models.CharField(_('TAT In Days'),max_length=64)
    mail_subject_line = models.CharField(_('Mail Subject Line'),max_length=256)
    policy_number = models.CharField(_('Policy Number'),max_length=256,unique=True)
    application_number = models.CharField(_('Application Number'),max_length=256,unique=True)
    urn = models.CharField(_('URN'),max_length=64) 
    customer_name = models.CharField(_('Customer Name'),max_length=256)
    father_name = models.CharField(_('father Name'),max_length=256)
    address = models.TextField(_('Address'))
    city = models.CharField(_('City'),max_length=256)
    pincode = models.CharField(_('Pincode'),max_length=64)
    state = models.CharField(_('State'),max_length=64)
    contact_number = models.CharField(_('Contact Number'),max_length=64)
    scope_of_investigation = models.TextField(_("Scope of Investigation"))
    investigatior_name = models.CharField(_('Investigatior Name'),max_length=64)
    remark = models.TextField(_("Remark - As per Rece. Findings"),null=True,blank=True,default="")
    case_status = models.CharField(_('Case Status'),max_length=64,choices=CaseStatus.choices)
    reason = models.TextField(_("If Highly Negative/ Negative/ Suspicious - Reason"),null=True,blank=True,default="")

    class Meta:
        verbose_name_plural = "Case"
    
    def __str__(self):
        return f"{self.uid} -- {self.client.username} -- {self.policy_number}"