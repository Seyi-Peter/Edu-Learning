# middleware/auto_logout.py
import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        timeout = getattr(settings, 'AUTO_LOGOUT_DELAY', 600)  # 600 seconds = 10 min
        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity')

        if last_activity:
            delta = now - datetime.datetime.fromisoformat(last_activity)
            if delta.total_seconds() > timeout:
                from django.contrib.auth import logout
                logout(request)
                return redirect(settings.LOGIN_URL)  # Redirect to login page

        request.session['last_activity'] = now.isoformat()
