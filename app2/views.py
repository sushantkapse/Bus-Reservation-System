from pyexpat.errors import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from app2.models import Bus,Booking

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            login(request, user)
            return redirect('home')
        
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if password1 != password2:
            print("sign")
            return redirect('signup')
        
        try:
            user = User.objects.create_user(username=username, password=password1,first_name=first_name, 
                last_name=last_name, 
                email=email)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            login(request, user)
            print(username)
            print(password1)
            # messages.success(request, "Account created successfully!")
            return redirect('home')
        except IntegrityError:
           
            return redirect('signup')
    return render(request, 'signup.html')

@login_required
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login') 



def admin_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            
            return redirect('admin_signup')
        try:
            # Create admin user
            user = User.objects.create_user(username=username, password=password1, is_staff=True)
            login(request, user)
           
            return redirect('admin_login')
        except IntegrityError:
            
            return redirect('admin_signup')
    return render(request, 'admin_signup.html')

# Admin Login View
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            
            return redirect('admin_login')
    return render(request, 'admin_login.html')


def admin_check(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_check)
def admin_dashboard_view(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard.html',{'users': users})


@user_passes_test(admin_check)
def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            # messages.error(request, "Passwords do not match.")
            return redirect('add_user')
        try:
            User.objects.create_user(username=username, password=password1)
            # messages.success(request, "User added successfully!")
            return redirect('admin_dashboard')
        except IntegrityError:
            # messages.error(request, "Username already exists.")
            return redirect('add_user')
    return render(request, 'add_user.html')

@user_passes_test(admin_check)
def update_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
            else:
                # messages.error(request, "Passwords do not match.")
                return redirect('update_user', user_id=user_id)
        user.username = username
        user.save()
        # messages.success(request, "User updated successfully!")
        return redirect('admin_dashboard')
    return render(request, 'update_user.html', {'user': user})

@user_passes_test(admin_check)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        # messages.success(request, "User deleted successfully!")
        return redirect('admin_dashboard')
    return render(request, 'delete_user.html', {'user': user})

def admin_check(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_check)
def admin_view_users(request):
    # users = User.objects.all()
    # return render(request, 'admin_view_users.html', {'users': users})
    user_id = request.GET.get('user_id', '')
    if user_id:
        users = User.objects.filter(id=user_id, is_staff=False)
    else:
        users = User.objects.filter(is_staff=False)
    return render(request, 'admin_view_users.html', {'users': users})

@user_passes_test(admin_check)
def admin_view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'admin_view_bookings.html', {'bookings': bookings})

@user_passes_test(admin_check)
def manage_buses_view(request):

    buses = Bus.objects.all()

    # Handle search functionality
    bus_id_query = request.GET.get('bus_id')
    if bus_id_query:
        buses = buses.filter(bus_id__icontains=bus_id_query)

    return render(request, 'manage_buses.html', {'buses': buses})
    # buses = Bus.objects.all()
    # return render(request, 'manage_buses.html', {'buses': buses})


@user_passes_test(admin_check)
def add_bus_view(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        bus_no = request.POST.get('bus_no')
        capacity = request.POST.get('capacity')
        start_point = request.POST.get('start_point')
        destination = request.POST.get('destination')
        seat_price = request.POST.get('seat_price')

        bus = Bus.objects.create(bus_id=bus_id, bus_no=bus_no, capacity=capacity,
                                 start_point=start_point, destination=destination, seat_price=seat_price)
        
        return redirect('manage_buses')
    return render(request, 'add_bus.html')

@user_passes_test(admin_check)
def update_bus_view(request, bus_id):
    bus = get_object_or_404(Bus, bus_id=bus_id)
    if request.method == 'POST':
        bus.bus_id = request.POST.get('bus_id')
        bus.bus_no = request.POST.get('bus_no')
        bus.capacity = request.POST.get('capacity')
        bus.start_point = request.POST.get('start_point')
        bus.destination = request.POST.get('destination')
        bus.seat_price = request.POST.get('seat_price')

        bus.save()
      
        return redirect('manage_buses')
    return render(request, 'update_bus.html', {'bus': bus})

@user_passes_test(admin_check)
def delete_bus_view(request, bus_id):
    bus = get_object_or_404(Bus, bus_id=bus_id)
    if request.method == 'POST':
        bus.delete()
       
        return redirect('manage_buses')
    return render(request, 'delete_bus.html', {'bus': bus})


def search_buses_view(request):
    start_point = request.GET.get('start_point')
    destination = request.GET.get('destination')
    
    buses = Bus.objects.all()

    if start_point:
        buses = buses.filter(start_point__icontains=start_point)
    
    if destination:
        buses = buses.filter(destination__icontains=destination)


    return render(request, 'Buses_list.html', {'buses': buses})


def book_bus_view(request, bus_id):
    bus = get_object_or_404(Bus, bus_id=bus_id)
    if request.method == 'POST':
        seats = int(request.POST.get('seats'))
        total_amount = seats * bus.seat_price
        booking = Booking.objects.create(user=request.user, bus=bus, seats=seats, total_amount=total_amount)
        request.session['booking_id'] = booking.id

        bus.available_seats -= seats
        bus.save()

        return redirect('booking_confirmation')
    
    return render(request, 'book_bus.html', {'bus': bus})

@login_required
def booking_confirmation_view(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    return render(request, 'book_confirmation.html', {'booking': booking})

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    bus = booking.bus
    bus.available_seats += booking.seats
    bus.save()


    booking.delete()
    return redirect('view_bookings')
