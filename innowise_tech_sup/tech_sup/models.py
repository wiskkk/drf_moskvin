from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    ticket_status = [('u', 'unresolved'), ('r', 'resolved'), ('p', 'paused')]

    status = models.CharField(max_length=1, blank=False, choices=ticket_status)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Answer(models.Model):
    answer_text = models.TextField(max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="parent", on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )
    ticket = models.ForeignKey(Ticket, verbose_name="ticket", on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return self.answer_text
