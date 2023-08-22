from django.db import models

# Create your models here.
import uuid
from django.db import models
from account.models import (
    RiskCoordinator,
    SuperAdminAndAdmin,
    FieldExecutive
)
from cases.models import (
    Case
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


class TaskStatus(models.TextChoices):
    NewCase = "New Case"
    Assigned = "Assigned"
    ReAssigned = "Re-Assigned"
    DropCase = "Drop Case"
    Done = "Done"


class TaskForRiskCoordinator(BaseModel):
    user = models.ForeignKey(
        SuperAdminAndAdmin, on_delete=models.CASCADE, related_name="assigned_tasks")
    risk_coordinator = models.ForeignKey(
        RiskCoordinator, on_delete=models.CASCADE, related_name="risk_coordinator_tasks")
    case = models.ForeignKey(Case, on_delete=models.CASCADE,related_name="cases")
    status = models.CharField(max_length=64, choices=TaskStatus.choices)

    def __str__(self):
        return f"{self.user.username} -> {self.risk_coordinator.username} : Case - {self.case.uid}"
    
    class Meta:
        verbose_name_plural = _('Task For Risk Co-Ordinator')

    def save(self, *args, **kwargs):
        self.status = TaskStatus.NewCase
        super(TaskForRiskCoordinator, self).save(*args, **kwargs)


class TaskForFieldExecutive(BaseModel):
    task = models.ForeignKey(TaskForRiskCoordinator, on_delete=models.CASCADE,
                             related_name="risk_coordinator_assigned_task")
    field_executive = models.ForeignKey(
        FieldExecutive, on_delete=models.CASCADE, related_name="field_executive_tasks")

    class Meta:
        verbose_name_plural = _("Task For Field Executive")

    def __str__(self):
        return f"{self.task.uid} -> {self.field_executive.username} : Case - {self.task.case.uid}"

    # def save(self, *args, **kwargs):
    #     super(TaskForFieldExecutive, self).save(*args, **kwargs)
