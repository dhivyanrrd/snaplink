from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ShortURL, ClickAnalytics
from .serializers import RegisterSerializer, UserSerializer,ShortURL,ShortURLSerializer
from rest_framework import status
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
import user_agents
from django.db.models import Count
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
    serializer_class=ShortURLSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def redirect_to_original(request, short_code):
    from django.core.cache import cache
    
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

    from .models import ClickAnalytics
    ClickAnalytics.objects.create(
        short_url=url_obj,
        ip_address=request.META.get('REMOTE_ADDR'),
        device_type=device
    )

    return redirect(original_url)

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