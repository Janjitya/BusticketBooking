from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('passenger', 'Passenger'),
    )
    role = models.CharField(max_length=10, default="passenger", choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.role} "
    

class Profile(models.Model):
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='user/profiles/', blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.mobile} "
    
class Bus(models.Model):
    BUS_TYPE_CHOICES = (
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    )
    SEAT_TYPE_CHOICES =(
        ('Sleeper', 'Sleeper'),
        ('Seater', 'Seater'),
    )
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    bus_type = models.CharField(choices=BUS_TYPE_CHOICES, max_length=15)
    seat_type = models.CharField(choices=SEAT_TYPE_CHOICES, max_length=15)
    total_seats = models.PositiveIntegerField()
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.DurationField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.number} - {self.destination}"
    
class Schedule(models.Model):

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedule")
    travel_date = models.DateField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bus.name} - {self.travel_date}"
    
class Booking(models.Model):
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_numbers = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_time = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.passenger.username} - {self.bus.name} - {self.schedule.travel_date}"
    



    
    

    
    
    
