from app.services.ranking import PostFeatures, rank_posts, exposure_metrics
from app.services.wellbeing import SessionFeatures, evaluate


def test_adalet_controlled_dataset_improves_small_creator_opportunity_without_relevance_loss():
    posts = [
        PostFeatures(1,'largeA','large',120000,'A',.91,.87,.82,.89,980,16000),
        PostFeatures(2,'smallA','small',420,'B',.89,.92,.96,.94,68,420),
        PostFeatures(3,'mediumA','medium',8500,'C',.82,.84,.91,.92,160,4100),
        PostFeatures(4,'largeB','large',280000,'D',.67,.49,.40,.97,1450,19500),
        PostFeatures(5,'smallB','small',180,'E',.86,.90,.95,.88,42,260),
        PostFeatures(6,'mediumB','medium',21000,'F',.94,.93,.94,.78,290,7000),
        PostFeatures(7,'smallBad','small',700,'G',.58,.32,.22,.99,90,500),
    ]
    b = exposure_metrics(rank_posts(posts, fair=False))
    f = exposure_metrics(rank_posts(posts, fair=True))
    assert f['small_creator_top5_share'] >= b['small_creator_top5_share']
    assert f['mean_relevance_top5'] >= b['mean_relevance_top5']
    assert all(x['creator_name'] != 'smallBad' for x in rank_posts(posts, fair=True)[:5])


def test_denge_threshold_boundary_is_stable():
    under = evaluate(SessionFeatures(179, 100, 80, 60, 160, 1, True))
    over = evaluate(SessionFeatures(180, 100, 80, 60, 160, 1, True))
    assert under['nudge'] is False
    assert over['nudge'] is True


def test_denge_balanced_long_session_does_not_nudge():
    r = evaluate(SessionFeatures(900, 60, 55, 4, 700, 1, True))
    assert r['nudge'] is False
    assert r['state'] == 'balanced'
