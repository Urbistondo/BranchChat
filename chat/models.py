import uuid

from django.contrib.auth import get_user_model
from django.db import models

from model_utils import Choices


User = get_user_model()


class Ticket(models.Model):
    STATUS = Choices(
        ('in_progress', 'In progress'),
        ('resolved', 'Resolved'),
        ('waiting', 'Waiting'),
    )

    CATEGORY = Choices(
        ('delay', 'Delay'),
        ('loan_approval', 'Loan approval'),
        ('loan_disbursement', 'Loan disbursement'),
        ('general_info', 'General information inquiry'),
        ('info_update', 'User information update'),
        ('undetermined', 'Not determined'),
    )

    PRIORITY = Choices(
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='user')
    agent = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name='agent')
    has_disconnected = models.BooleanField(default=False, null=False)
    category = models.TextField(max_length=140, choices=CATEGORY, default=CATEGORY.undetermined, null=False)
    priority = models.TextField(max_length=140, choices=PRIORITY, default=PRIORITY.medium, null=False)
    status = models.CharField(max_length=60, choices=STATUS, default=STATUS.waiting, null=False)
    subject = models.TextField(max_length=140, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    # def __str__(self):
    #     return self.id


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, null=False, editable=False, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    ticket = models.ForeignKey(Ticket, null=False, editable=False, on_delete=models.CASCADE)

    sent_at = models.DateTimeField(auto_now_add=True, null=False)

    # def __str__(self):
    #     return '%s - %s - %s' % (self.author, self.ticket.id, self.sent_at)


class CannedMessage(models.Model):
    CATEGORY = Choices(
        ('undetermined', 'Undetermined'),
        ('apology', 'Apologize'),
        ('greeting', 'Greet'),
        ('thank', 'Thank'),
        ('wait', 'Wait'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(max_length=500)
    category = models.TextField(max_length=140, choices=CATEGORY, default=CATEGORY.undetermined, null=False)

    # def __str__(self):
    #     return '%s - %s' % (self.id, self.category)
