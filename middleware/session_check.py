# middleware/session_check.py
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import redirect

class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.session.exists(request.session.session_key):
                return redirect(settings.LOGIN_URL)  # Force re-login if session invalid

        return self.get_response(request)
