from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.db.models import Count
import user_agents
from django.core.cache import cache
from .serializers import RegisterSerializer, UserSerializer, ShortURLSerializer
from .models import ShortURL, ClickAnalytics
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User created successfully",
        })

class ShortenURLView(generics.CreateAPIView):
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class URLAnalyticsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, short_code):
        try:
            url_obj = ShortURL.objects.get(short_code=short_code, user=request.user)
        except ShortURL.DoesNotExist:
            return Response({"error": "URL not found"}, status=404)

        clicks = ClickAnalytics.objects.filter(short_url=url_obj)
        total_clicks = clicks.count()
        device_counts = clicks.values('device_type').annotate(count=Count('device_type'))
        devices = {item['device_type']: item['count'] for item in device_counts}
        last_click = clicks.order_by('-clicked_at').first()

        return Response({
            'short_code': short_code,
            'original_url': url_obj.original_url,
            'total_clicks': total_clicks,
            'clicks_by_device': devices,
            'last_clicked': last_click.clicked_at if last_click else None
        })

def redirect_to_original(request, short_code):
    original_url = cache.get(f'url:{short_code}')

    if not original_url:
        try:
            url_obj = ShortURL.objects.get(short_code=short_code, is_active=True)
            original_url = url_obj.original_url
            cache.set(f'url:{short_code}', original_url, timeout=3600)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound("URL not found")
    else:
        url_obj = ShortURL.objects.get(short_code=short_code)

    ua_string = request.META.get('HTTP_USER_AGENT', '')
    if ua_string:
        ua = user_agents.parse(ua_string)
        device = 'mobile' if ua.is_mobile else 'tablet' if ua.is_tablet else 'desktop'
    else:
        device = 'unknown'

    ClickAnalytics.objects.create(
        short_url=url_obj,
        ip_address=request.META.get('REMOTE_ADDR'),
        device_type=device
    )

    return redirect(original_url)



def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')