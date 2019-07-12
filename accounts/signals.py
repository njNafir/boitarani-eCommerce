from django.dispatch import Signal

user_loged_in_signal = Signal(providing_args=['instance', 'request'])