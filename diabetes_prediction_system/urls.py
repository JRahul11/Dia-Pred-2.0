from django.contrib import admin
from django.urls import path
from auth_app.views import user_login, user_signup, user_logout, user_np
from main_app.views import home, predict, history, about, report

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication
    path("", user_login, name='login'),
    path("signup/", user_signup, name='signup'),
    path("logout/", user_logout, name="logout"),
    path("forgotpassword/", user_np, name="user_np"),

    # Main Project
    path("home/", home, name='home'),
    path("predict/", predict, name='predict'),
    path("history/", history, name='history'),
    path("history/<str>", history, name='history'),
    path("about/", about, name='about'),
    path("report/<patient_id>", report, name='report')
]
