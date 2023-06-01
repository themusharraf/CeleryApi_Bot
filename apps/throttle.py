from rest_framework.throttling import UserRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    rate = '3/minute'
