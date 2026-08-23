from app.services.moderation import normalize_turkish, ContextualDemoModerationEngine
from app.services.ranking import PostFeatures, rank_posts
from app.services.wellbeing import SessionFeatures, evaluate

def test_turkish_unicode_preserved():
    assert 'çoook' in normalize_turkish('  çoook iyi olmuş 😂  ')
    assert '😂' in normalize_turkish('çoook iyi olmuş 😂')

def test_moderation_runs():
    result = ContextualDemoModerationEngine().analyze('Mükemmel, yine uygulamayı çökerttin 👏')
    assert 0 <= result.confidence <= 1
    assert result.decision in {'allow','warn','review'}

def test_low_quality_small_creator_not_auto_boosted():
    posts=[
        PostFeatures(1,'smallbad','small',100,'tekrar tekrar',.55,.15,.2,.9,80,100),
        PostFeatures(2,'largegood','large',100000,'kaliteli içerik',.9,.9,.9,.8,900,12000),
    ]
    ranked=rank_posts(posts, fair=True)
    assert ranked[0]['creator_name']=='largegood'

def test_high_relevance_large_creator_not_suppressed():
    posts=[
        PostFeatures(1,'large','large',100000,'relevant',.98,.95,.9,.9,1000,15000),
        PostFeatures(2,'small','small',200,'less relevant',.55,.9,.95,.9,50,200),
    ]
    assert rank_posts(posts, fair=True)[0]['creator_name']=='large'

def test_wellbeing_intentional_no_nudge():
    out=evaluate(SessionFeatures(420,24,20,3,220,1,True))
    assert out['nudge'] is False

def test_wellbeing_rapid_nudge():
    out=evaluate(SessionFeatures(360,150,120,96,160,2,True))
    assert out['nudge'] is True

def test_wellbeing_short_fast_no_nudge():
    out=evaluate(SessionFeatures(50,35,30,24,55,0,True))
    assert out['nudge'] is False

def test_wellbeing_disabled():
    out=evaluate(SessionFeatures(400,200,180,150,90,2,False))
    assert out['state']=='disabled'
