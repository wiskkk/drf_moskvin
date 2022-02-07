from innowise_tech_sup.celery import app
from django.core.mail import send_mail
from .models import Ticket


# @app.task
# def status_updated(ticket_id):
#     """
#     Задача для отправки уведомления по электронной почте при изменении статуса на "resolved".
#     """
#     ticket = Ticket.objects.get(id=ticket_id)
#     subject = f'ticket №{ticket_id}'
#     message = f'Dear {ticket.owner} your ticket has been resolved'
#     mail_sent = send_mail(subject,
#                           message,
#                           'artiom95moskvin@gmail.com',
#                           [ticket.email])
#     return mail_sent
@app.task
def status_updated(ticket_id):
    """
    Задача для отправки уведомления по электронной почте при изменении статуса на "resolved".
    """
    # ticket = Ticket.objects.all()
    ticket = Ticket.objects.get(id=ticket_id)
    print(str(ticket))
    subject = f'ticket №{ticket_id}'
    message = f'Dear  your ticket has been resolved'
    mail_sent = send_mail(subject,
                          message,
                          'artiom95moskvin@gmail.com',
                          [ticket.owner_email])
    return mail_sent
