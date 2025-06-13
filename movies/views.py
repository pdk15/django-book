from django.shortcuts import render , redirect , get_object_or_404
from .models import Movie , Theater , Seat , Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError 

'''def movie_list(request):  #Defines a view function that handles requests to see the list of movies.
    search_query=request.Get.get('search')  #Retrieves the search query parameter from the URL,
    if search_query:         
        movies=Movie.object.filter(name__icontains=search_query)  #If a search term exists, filters the Movie model to only include movies whose name contains the search term, case-insensitively.
    else:
        movies=Movie.objects.all()  #If there's no search query, it retrieves all movies.
    return render(request ,'movies/movie_list.html',{'movies' : movies}) '''  #Renders the template movie_list.html and passes the list of movies into the template context under the name movies


def movie_list(request):
    movies = Movie.objects.all()
    for movie in movies:
        print(movie.cast)  #  Debug print
    return render(request, "movies/movie_list.html", {"movies": movies})

def theater_list(request, movie_id):
    movie=get_object_or_404(Movie , id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request ,'movies/theater_list.html',{'movies' : movie , 'theaters' :theater})

@login_required(login_url='/login/')
def book_seat(request, theater_id):
    theater=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theater)
    if request.method== 'POST':
        selected_seat=request.POST.getlist('seats')
        error_seats=[]
        if not selected_seat:
            return render(request, "movies/seat_selection.html" , {'theater' : theater , 'seats':seats , 'error' : "No seat selected"})
        for seat_id in selected_seat:
            seat= get_object_or_404(Seat, id =seat_id, theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user = request.user,
                    seat = seat,
                    movie = theater.movie,
                    theater = theater
                )
                seat.is_booked=True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats :
            error_message = f" The following seats are already booked {','.join(error_seats)}"
            return render(request , 'movies/seat_selection.html' ,{'theater' :theater , 'seats' : seats , 'error' : "No seat selected"})
        return redirect('profile')
                
    return render(request , 'movies/seat_selection.html',{'theater' :theater , 'seats' : seats})