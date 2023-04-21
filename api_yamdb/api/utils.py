from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def confirmation_code_send_email(user):
    '''Функция для генерации отправке кода потдтверждения на email.'''
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )
