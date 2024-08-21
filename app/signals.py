from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def start_scheduler(sender, **kwargs):
    from .scheduler import scheduler
    scheduler.start()