from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    r=client.get('/api/health'); assert r.status_code==200; assert r.json()['prototype'] is True

def test_empty_moderation_rejected():
    r=client.post('/api/moderation/analyze', json={'text':''}); assert r.status_code==422

def test_ranking_compare():
    r=client.post('/api/ranking/compare'); assert r.status_code==200; assert 'baseline' in r.json() and 'fair' in r.json()

def test_end_to_end_core_flow():
    m=client.post('/api/moderation/analyze',json={'text':'Fikir güzel ancak kaynaklar daha iyi açıklanmalı.'}); assert m.status_code==200
    feed=client.get('/api/feed'); assert feed.status_code==200 and len(feed.json())>0
    rank=client.post('/api/ranking/rank',json={'fair':True}); assert rank.status_code==200
    w=client.post('/api/wellbeing/event',json={'session_duration_sec':360,'posts_scrolled':150,'viewed_posts':120,'rapid_skips':96,'total_dwell_sec':160,'reentry_count':2,'enabled':True}); assert w.status_code==200 and w.json()['nudge'] is True
