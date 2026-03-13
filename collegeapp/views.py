from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, Faculty, Event, Gallery, Admission, StudentProfile
from .forms import UserRegisterForm, StudentProfileForm, ContactForm, AdmissionForm

def index(request):
    events = Event.objects.filter(is_upcoming=True)[:3]
    courses = Course.objects.all()[:3]
    context = {
        'events': events,
        'courses': courses,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def admissions(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.user = request.user
            admission.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('dashboard')
    else:
        form = AdmissionForm()
    return render(request, 'admissions.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def gallery(request):
    images = Gallery.objects.all()
    return render(request, 'gallery.html', {'images': images})

def faculty(request):
    faculty_members = Faculty.objects.all()
    return render(request, 'faculty.html', {'faculty_members': faculty_members})

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile_setup')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def dashboard(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        applications = Admission.objects.filter(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None
        applications = Admission.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'applications': applications,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_setup(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        if profile:
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = StudentProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        if profile:
            form = StudentProfileForm(instance=profile)
        else:
            form = StudentProfileForm()
    
    return render(request, 'profile_setup.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None
    return render(request, 'profile.html', {'profile': profile})