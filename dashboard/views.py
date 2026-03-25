from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import ApiSnapshot
from .services import (
    fetch_constructor_standings,
    fetch_driver_standings,
    fetch_latest_results,
    fetch_live_sessions,
    fetch_news,
    fetch_schedule,
)

CACHE_TTL = timedelta(minutes=10)


def _get_payload(source, fetcher):
    snapshot = ApiSnapshot.objects.filter(source=source).first()
    if snapshot and timezone.now() - snapshot.updated_at < CACHE_TTL:
        return snapshot.payload

    payload = fetcher()
    ApiSnapshot.objects.update_or_create(source=source, defaults={'payload': payload})
    return payload


def home(request):
    context = {
        'driver_standings': _get_payload('driver_standings', fetch_driver_standings),
        'constructor_standings': _get_payload('constructor_standings', fetch_constructor_standings),
        'schedule': _get_payload('schedule', fetch_schedule),
        'latest_results': _get_payload('latest_results', fetch_latest_results),
        'live_sessions': _get_payload('live_sessions', fetch_live_sessions),
        'news': _get_payload('news', fetch_news),
        'last_updated': timezone.now(),
    }
    return render(request, 'dashboard/home.html', context)


def live_data(request):
    payload = {
        'driver_standings': _get_payload('driver_standings', fetch_driver_standings),
        'constructor_standings': _get_payload('constructor_standings', fetch_constructor_standings),
        'live_sessions': _get_payload('live_sessions', fetch_live_sessions),
        'updated_at': timezone.now().isoformat(),
    }
    return JsonResponse(payload)
