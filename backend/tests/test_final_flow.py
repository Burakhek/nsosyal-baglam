from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def setup_function():
    client.post('/api/demo/reset')


def test_baglam_returns_traceable_result_id():
    r = client.post('/api/moderation/analyze', json={'text': 'Mükemmel, yine uygulamayı çökerttin 👏'})
    assert r.status_code == 200
    data = r.json()
    assert data['id'].startswith('MOD-')
    stored = client.get(f"/api/moderation/results/{data['id']}")
    assert stored.status_code == 200
    assert stored.json()['normalized_text'] == data['normalized_text']


def test_appeal_is_linked_to_real_moderation_result():
    m = client.post('/api/moderation/analyze', json={'text': 'İyiymiş gerçekten...'}).json()
    r = client.post('/api/moderation/appeal', json={
        'moderation_result_id': m['id'],
        'reason': 'Bağlamın yeniden değerlendirilmesini istiyorum.'
    })
    assert r.status_code == 200
    assert r.json()['moderation_result_id'] == m['id']
    assert r.json()['status'] == 'pending_review'


def test_appeal_rejects_unknown_result():
    r = client.post('/api/moderation/appeal', json={
        'moderation_result_id': 'MOD-9999',
        'reason': 'Bu karar tekrar incelenmeli.'
    })
    assert r.status_code == 404


def test_safe_post_publishes_and_enters_feed():
    text = 'Bugün hava çok güzel, yürüyüşe çıkacağım.'
    r = client.post('/api/posts/publish', json={'text': text, 'override_warning': False})
    assert r.status_code == 200
    assert r.json()['published'] is True
    feed = client.post('/api/ranking/rank', json={'fair': False}).json()['items']
    assert any(item['text'] == text and item['creator_name'] == 'Deniz Aksoy' for item in feed)


def test_warning_requires_explicit_override_then_publishes():
    text = 'Mükemmel, yine uygulamayı çökerttin 👏'
    first = client.post('/api/posts/publish', json={'text': text, 'override_warning': False}).json()
    assert first['published'] is False
    assert first['status'] == 'warning_requires_confirmation'
    second = client.post('/api/posts/publish', json={'text': text, 'override_warning': True}).json()
    assert second['published'] is True


def test_review_cannot_be_silently_overridden():
    text = 'Sen hiçbir şey bilmiyorsun, rezil birisin.'
    r = client.post('/api/posts/publish', json={'text': text, 'override_warning': True}).json()
    assert r['published'] is False
    assert r['status'] == 'queued_for_review'


def test_adalet_explanation_is_available_for_ranked_item():
    ranked = client.post('/api/ranking/rank', json={'fair': True}).json()['items']
    r = client.get(f"/api/ranking/explanation/{ranked[0]['id']}")
    assert r.status_code == 200
    assert r.json()['reasons']
    assert 'fairness_adjustment' in r.json()


def test_denge_response_is_recorded():
    r = client.post('/api/wellbeing/nudge-response?response=break_5')
    assert r.status_code == 200
    assert r.json()['accepted'] is True
    assert r.json()['response'] == 'break_5'
    assert r.json()['id'].startswith('NR-')


def test_reset_removes_runtime_user_posts():
    text = 'Bugün hava çok güzel, yürüyüşe çıkacağım.'
    client.post('/api/posts/publish', json={'text': text, 'override_warning': False})
    client.post('/api/demo/reset')
    feed = client.post('/api/ranking/rank', json={'fair': False}).json()['items']
    assert not any(item['id'] >= 1000 for item in feed)
