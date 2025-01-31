from django.shortcuts import render, redirect

from activity.models import Activity
from homework.models import Homework


def social_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    
    return render(request, "dashboard/social_login.html")


def home(request):

    return render(request, "dashboard/home.html", {"title": "dashboard"})


def profile(request):
    """
    return undone activities
    return undone homeworks
    """
    activities = Activity.objects.filter(user=request.user, is_finished=False)
    homeworks = Homework.objects.filter(user=request.user, is_finished=False)

    return render(request, "dashboard/profile.html", {
        "activities": activities,
        "homeworks": homeworks,
        "title": "profile"
    })
