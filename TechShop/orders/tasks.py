from celery import shared_task
from django.core.mail import send_mail
from .models import Order



"""Task to send an e-mail notification when an order is
 successfully created."""

@shared_task
def order_created(order_id):
    order= Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
        f'Ypu have successfully placed an order.' \
        f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@TechShop.com', [order.email])
    
    return mail_sent


