# signals.py

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone

from .models import BusinessProfile

# Define a signal receiver to send email notifications for reminders
@receiver(post_save, sender=BusinessProfile)
def send_reminder_notification(sender, instance, created, **kwargs):
    if created:
        # Check if license expiration reminder is set
        if instance.license_expiration_reminder_days:
            expiration_date = instance.license_expiration
            reminder_days = instance.license_expiration_reminder_days
            reminder_date = expiration_date - timezone.timedelta(days=reminder_days)
            if reminder_date <= timezone.now().date():
                send_notification_email(instance.shop_name, 'License Expiration Reminder', expiration_date)

        # Check if VAT submission date reminder is set
        if instance.vat_submission_date_reminder_days:
            submission_date = instance.vat_submission_date
            reminder_days = instance.vat_submission_date_reminder_days
            reminder_date = submission_date - timezone.timedelta(days=reminder_days)
            if reminder_date <= timezone.now().date():
                send_notification_email(instance.shop_name, 'VAT Submission Date Reminder', submission_date)

        # Check if employee visa expiration reminder is set
        if instance.employee_visa_expiration_reminder_days:
            # Implement logic for employee visa expiration reminder
            visa_expiration_date = instance.employee_visa_expiration
            reminder_days = instance.employee_visa_expiration_reminder_days
            reminder_date = visa_expiration_date - timezone.timedelta(days=reminder_days)
            if reminder_date <= timezone.now().date():
                send_notification_email(instance.shop_name, 'Employee Visa Expiration Reminder', visa_expiration_date)

# Function to send email notification
def send_notification_email(shop_name, reminder_type, reminder_date):
    subject = f'Reminder: {reminder_type}'
    message = render_to_string('email/reminder_notification.html', {
        'shop_name': shop_name,
        'reminder_type': reminder_type,
        'reminder_date': reminder_date,
    })
    recipient_list = ['admin@example.com']  # Add recipient email addresses here
    send_mail(subject, message, 'noreply@example.com', recipient_list)
