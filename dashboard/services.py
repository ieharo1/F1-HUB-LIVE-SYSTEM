from __future__ import annotations

from datetime import datetime, timezone
import requests

TIMEOUT = 10
JOLPICA = 'https://api.jolpi.ca/ergast/f1'
OPENF1 = 'https://api.openf1.org/v1'
NEWS_RSS = 'https://www.formula1.com/content/fom-website/en/latest/all.xml'


def _safe_get(url: str):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        if 'xml' in response.headers.get('content-type', '').lower():
            return response.text
        return response.json()
    except Exception:
        return None


def fetch_driver_standings():
    data = _safe_get(f'{JOLPICA}/current/driverStandings.json')
    if not data:
        return [
            {'position': '1', 'driver': 'Max Verstappen', 'constructor': 'Red Bull', 'points': '0', 'wins': '0'},
            {'position': '2', 'driver': 'Charles Leclerc', 'constructor': 'Ferrari', 'points': '0', 'wins': '0'},
            {'position': '3', 'driver': 'Lando Norris', 'constructor': 'McLaren', 'points': '0', 'wins': '0'},
        ]

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    result = []
    for item in standings:
        result.append(
            {
                'position': item['position'],
                'driver': f"{item['Driver']['givenName']} {item['Driver']['familyName']}",
                'constructor': item['Constructors'][0]['name'],
                'points': item['points'],
                'wins': item['wins'],
            }
        )
    return result


def fetch_constructor_standings():
    data = _safe_get(f'{JOLPICA}/current/constructorStandings.json')
    if not data:
        return [
            {'position': '1', 'name': 'Red Bull', 'points': '0', 'wins': '0'},
            {'position': '2', 'name': 'Ferrari', 'points': '0', 'wins': '0'},
            {'position': '3', 'name': 'McLaren', 'points': '0', 'wins': '0'},
        ]

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    return [
        {
            'position': item['position'],
            'name': item['Constructor']['name'],
            'points': item['points'],
            'wins': item['wins'],
        }
        for item in standings
    ]


def fetch_schedule(limit: int = 6):
    data = _safe_get(f'{JOLPICA}/current.json')
    if not data:
        return []
    races = data['MRData']['RaceTable']['Races'][:limit]
    result = []
    for race in races:
        result.append(
            {
                'round': race['round'],
                'name': race['raceName'],
                'circuit': race['Circuit']['circuitName'],
                'country': race['Circuit']['Location']['country'],
                'date': race['date'],
            }
        )
    return result


def fetch_latest_results(limit: int = 10):
    data = _safe_get(f'{JOLPICA}/current/last/results.json')
    if not data:
        return []
    races = data['MRData']['RaceTable']['Races']
    if not races:
        return []
    return [
        {
            'position': row['position'],
            'driver': f"{row['Driver']['givenName']} {row['Driver']['familyName']}",
            'constructor': row['Constructor']['name'],
            'points': row['points'],
            'status': row['status'],
        }
        for row in races[0]['Results'][:limit]
    ]


def fetch_live_sessions(limit: int = 6):
    data = _safe_get(f'{OPENF1}/sessions?session_type=Race&year={datetime.now(timezone.utc).year}')
    if not data:
        return []

    ordered = sorted(data, key=lambda x: x.get('date_start', ''), reverse=True)
    return [
        {
            'meeting': row.get('meeting_name', 'N/A'),
            'session': row.get('session_name', 'Race'),
            'country': row.get('country_name', 'N/A'),
            'date_start': row.get('date_start', 'N/A'),
            'status': row.get('session_status', 'scheduled'),
        }
        for row in ordered[:limit]
    ]


def fetch_news():
    xml_data = _safe_get(NEWS_RSS)
    if not xml_data:
        return []

    items = []
    chunks = xml_data.split('<item>')[1:8]
    for chunk in chunks:
        title = _extract(chunk, 'title')
        link = _extract(chunk, 'link')
        pub_date = _extract(chunk, 'pubDate')
        description = _extract(chunk, 'description')
        items.append(
            {
                'title': title,
                'link': link,
                'published': pub_date,
                'description': description[:180] + '...' if description else '',
            }
        )
    return items


def _extract(raw: str, tag: str) -> str:
    start = raw.find(f'<{tag}>')
    end = raw.find(f'</{tag}>')
    if start == -1 or end == -1:
        return ''
    value = raw[start + len(tag) + 2 : end]
    return (
        value.replace('<![CDATA[', '')
        .replace(']]>', '')
        .replace('&amp;', '&')
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .strip()
    )
