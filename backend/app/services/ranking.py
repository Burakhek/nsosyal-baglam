from __future__ import annotations
from dataclasses import dataclass, asdict
from math import log1p
from typing import Iterable

@dataclass
class PostFeatures:
    id: int
    creator_name: str
    creator_size: str
    followers: int
    text: str
    relevance: float
    quality: float
    originality: float
    freshness: float
    recent_engagement: int
    baseline_exposure: int


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def normalized_engagement(post: PostFeatures) -> float:
    return clamp(log1p(post.recent_engagement) / log1p(1500))


def relative_velocity(post: PostFeatures) -> float:
    # Smoothed denominator prevents tiny creators from exploding numerically.
    ratio = (post.recent_engagement + 8.0) / (post.baseline_exposure + 120.0)
    return clamp(ratio * 4.0)


def under_exposure(post: PostFeatures) -> float:
    # Uses observed prior exposure, not a moral judgment about follower count.
    return clamp(1.0 - log1p(post.baseline_exposure) / log1p(20000))


def baseline_score(post: PostFeatures) -> float:
    return round(
        0.50 * post.relevance +
        0.35 * normalized_engagement(post) +
        0.15 * post.freshness,
        5
    )


def fair_score(post: PostFeatures) -> tuple[float, float]:
    quality_gate = clamp((post.quality - 0.45) / 0.55)
    fairness_adjustment = 0.16 * under_exposure(post) * quality_gate * clamp(post.relevance / 0.65)
    popularity_dependency = 0.05 * clamp(log1p(post.baseline_exposure) / log1p(20000))
    score = (
        0.34 * post.relevance +
        0.18 * post.quality +
        0.11 * post.originality +
        0.11 * relative_velocity(post) +
        0.10 * post.freshness +
        fairness_adjustment -
        popularity_dependency
    )
    return round(score, 5), round(fairness_adjustment, 5)


def rank_posts(posts: Iterable[PostFeatures], fair: bool = True) -> list[dict]:
    rows = []
    for p in posts:
        base = baseline_score(p)
        fair_val, adjustment = fair_score(p)
        row = asdict(p)
        row.update({
            'normalized_engagement': round(normalized_engagement(p), 4),
            'relative_velocity': round(relative_velocity(p), 4),
            'under_exposure': round(under_exposure(p), 4),
            'baseline_score': base,
            'fairness_adjustment': adjustment,
            'final_score': fair_val if fair else base,
        })
        rows.append(row)
    rows.sort(key=lambda r: r['final_score'], reverse=True)
    for i, r in enumerate(rows, 1):
        r['rank'] = i
    return rows


def exposure_metrics(ranked: list[dict]) -> dict:
    if not ranked:
        return {'creator_diversity': 0, 'small_creator_topk_share': 0, 'exposure_gini': 0}
    topk = ranked[: min(5, len(ranked))]
    small = sum(1 for r in topk if r['creator_size'] == 'small') / len(topk)
    creators = len(set(r['creator_name'] for r in topk))
    # Position-based exposure weight, then Gini over creators in top-k.
    weights = [1 / (i + 1) for i in range(len(topk))]
    per_creator = {}
    for r, w in zip(topk, weights):
        per_creator[r['creator_name']] = per_creator.get(r['creator_name'], 0) + w
    vals = sorted(per_creator.values())
    n = len(vals)
    if n <= 1 or sum(vals) == 0:
        gini = 0.0
    else:
        gini = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(vals)) / (n * sum(vals))
    return {
        'creator_diversity_top5': creators,
        'small_creator_top5_share': round(small, 4),
        'exposure_gini_top5': round(gini, 4),
        'mean_relevance_top5': round(sum(r['relevance'] for r in topk) / len(topk), 4),
    }
