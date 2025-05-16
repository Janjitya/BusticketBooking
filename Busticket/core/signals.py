from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Schedule, Seat

@receiver(post_save, sender=Schedule)
def create_seat_for_schedule(sender, instance, created, **kwargs):
    if created:
        total_seats = instance.bus.total_seats
        for i in range(1, total_seats+1):
            Seat.objects.create(schedule=instance, seat_number=f"S{i}")
