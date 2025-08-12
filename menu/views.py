from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import jwt
from datetime import datetime, timezone, timedelta
now = datetime.now(timezone.utc)

def login_admin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT verify_admin(%s, %s)", [username, password])
            is_valid = cursor.fetchone()[0]
        
        if is_valid:
            payload = {
                "username": username,
                "exp": datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({
                "success": True, 
                "message": "berhasil login!",
                "token": token
            })
        else:
            return JsonResponse({"success": False, "error": "username atau password salah!"}, status=401)

def dashboard_view(request):
    if not hasattr(request, 'jwt_payload'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

    username = request.jwt_payload.get('username')
    return JsonResponse({'success': True, "username": username})

