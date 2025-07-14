from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm
from  .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required  
from movies.models import Movie , Booking
from datetime import date
from movies.models import Movie , Show

# def home(request):
    # movies = Movie.objects.all()
    # return render(request, 'home.html', {'movies': movies})
def home(request):
    today = date.today()
    movies = Movie.objects.all()
    today_show = Show.objects.filter(date=today)
    return render(request, 'users/home.html', {'today_show': today_show})

def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')  #Extracts the username and password from the form.
            password=form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password) #Authenticates the user (verifies that credentials are valid).
            login(request ,user)    # Logs the user in if authentication is successful.

        return render('profile')  #Redirects the user to the 'profile' page after successful login.
    
    else:
        form=UserRegisterForm()            #If it''s not a POST (i.e., a GET request), it means the user is visiting the page for the first time. A blank registration form is shown.
    return render(request,'users/register.html',{'form':form})   #Renders the register.html template and passes the form to it using the key 'forms'.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'bookings': bookings
    })

@login_required
def reset_password(request):
    if request.method== 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else :
            form=PasswordChangeForm(user=request.user)
        return render(request,'users/reset_password.html',{'form' :form})

from django.db.models import Count

def recommend_movies(user):
    # Get top genre the user books
    booked_movies = Booking.objects.filter(user=user).values_list('movie__genre', flat=True)
    top_genres = booked_movies.annotate(count=Count('movie__genre')).order_by('-count')
    if top_genres:
        return Movie.objects.filter(genre=top_genres[0])
    return Movie.objects.all()[:5]  # fallback

def dashboard(request):
    recommendations = recommend_movies(request.user)
    return render(request, 'dashboard.html', {'recommendations': recommendations})
