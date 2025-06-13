from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    name = models.CharField(max_length=255)  # Movie title
    image = models.ImageField(upload_to="movies/")  # Poster or image file stored in media/movies/
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5 (fix: you missed '=' after 'rate')
    cast = models.TextField()     
    description = models.TextField(blank=True, null=True)  # Optional field to list cast names
    
    def __str__(self):
        return self.name  # Shows movie name when printed or in admin panel


class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')  # Each theater is showing one movie at a specific time.
    time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):  
        return f'{self.seat_number} in {self.theater.name} '
        
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who booked the seat
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)  # The seat being booked
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # The movie being watched
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)  # The theater where it's booked
    booked_at = models.DateTimeField(auto_now_add=True)  # Auto-filled with booking time
    
    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'
