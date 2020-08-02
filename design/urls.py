"""design URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('sar/', include('sar.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
#    path('', include('sar.urls')),
]

USERS_REGISTRATION_OPEN = True

USERS_VERIFY_EMAIL = True

USERS_AUTO_LOGIN_ON_ACTIVATION = True

USERS_EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3

# Specifies minimum length for passwords:
USERS_PASSWORD_MIN_LENGTH = 5

# Specifies maximum length for passwords:
USERS_PASSWORD_MAX_LENGTH = 18

# the complexity validator, checks the password strength
USERS_CHECK_PASSWORD_COMPLEXITY = True

USERS_SPAM_PROTECTION = False  # important!

#  ---------------------------------------------------------
#  Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '331336857@qq.com'
EMAIL_HOST_PASSWORD = 'zxcvbnm.'
DEFAULT_FROM_EMAIL = '331336857@qq.com'