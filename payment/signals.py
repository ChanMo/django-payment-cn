from django.dispatch import Signal

pay_done = Signal(providing_args=["user", "number", "action", "extra"])
