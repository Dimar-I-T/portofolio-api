import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response =  get_response
    
    def __call__(self, request):
        if not request.path.startswith('/api-admin/'):
            return self.get_response(request)
        
        if request.path.startswith('/api-admin/login-admin'):
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')

        if auth_header is None or not auth_header.startswith('Bearer '):
            return JsonResponse({'success': False, 'message': 'Token tidak ditemukan'}, status=401)
        
        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({'success': False, 'message': 'Token sudah expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'success': False, 'message': 'Token tidak valid'}, status=401)
        
        return self.get_response(request)