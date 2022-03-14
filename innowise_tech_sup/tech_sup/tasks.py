from django.core.mail import send_mail

from innowise_tech_sup.celery import app

from .models import Ticket


@app.task
def status_updated(ticket_id):
    """
    Задача для отправки уведомления по электронной почте при изменении статуса
    на "resolved".
    """
    ticket = Ticket.objects.get(id=ticket_id)
    subject = f'ticket №{ticket_id}'
    message = f'Dear {ticket.owner} your ticket has been resolved i do myself'
    mail_sent = send_mail(subject,
                          message,
                          'artiom95moskvin@gmail.com',
                          [ticket.owner.email],
                          fail_silently=False)
    return mail_sent
