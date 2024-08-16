from django.core.mail import send_mail


def send_confirmation_code(email, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=f'Код подтверждения: {confirmation_code}',
        from_email='yamdb@yamdb.com',
        recipient_list=['to@example.com'],
        fail_silently=True,
    )
