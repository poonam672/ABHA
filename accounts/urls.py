from django.db import router
from django.urls import include, path
from accounts.views import *

urlpatterns = [
    path('api/mobile-otp/',MobileAPi.as_view(),name='mobile-otp'),

    path('api/adhar-verify/',AAdharVerify.as_view(),name='adhar-verify'),
    path('api/adhar-otp-verify/',AAdharOTPVerify.as_view(),name='adhar-otp-verify'),
    path('api/mobile-verify/',MobileVerify.as_view(),name='mobile-verify'),
    path('api/mobile-otp-verify/',MobileOtpVerify.as_view(),name='mobile-otp-verify'),
    path('api/create-health-id/',CreateHealthId.as_view(),name='create-health-id'),
    path('api/qr-code/',QrCodeAPI.as_view(),name='qr-code'),
    path('api/get-card/',GetCardAPI.as_view(),name='get-card'),
    path('api/search-health-id/',searchByHealthId.as_view(),name='search-health-id'),
    path('api/exists-health-id/',existsByHealthId.as_view(),name='exists-health-id'),
    path('api/mobile-login/',MobileLogin.as_view(),name='mobile-login'),
    path('api/auth-cert/',AuthCert.as_view(),name='auth-cert'),
    path('api/get-response/',GetResponseAPI.as_view(),name='get-response'),





]