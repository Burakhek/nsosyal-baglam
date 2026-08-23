from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

@dataclass
class SessionFeatures:
    session_duration_sec: float
    posts_scrolled: int
    viewed_posts: int
    rapid_skips: int
    total_dwell_sec: float
    reentry_count: int = 0
    enabled: bool = True


def evaluate(features: SessionFeatures) -> dict:
    if not features.enabled:
        return {**asdict(features), 'state': 'disabled', 'nudge': False, 'reason': 'Dijital iyilik hâli önerileri kullanıcı tarafından kapatılmış.'}
    active_minutes = max(features.session_duration_sec / 60.0, 0.25)
    scroll_velocity = features.posts_scrolled / active_minutes
    mean_dwell = features.total_dwell_sec / max(features.viewed_posts, 1)
    rapid_skip_ratio = features.rapid_skips / max(features.viewed_posts, 1)

    persistent = features.session_duration_sec >= 180
    rapid_pattern = scroll_velocity >= 18 and rapid_skip_ratio >= 0.60 and mean_dwell <= 3.2
    nudge = bool(persistent and rapid_pattern)
    state: Literal['balanced','rapid_pattern','break_suggestion']
    if nudge:
        state = 'break_suggestion'
    elif rapid_pattern:
        state = 'rapid_pattern'
    else:
        state = 'balanced'
    reason = (
        'Son birkaç dakikada yüksek kaydırma hızı, kısa görüntüleme süresi ve yüksek hızlı-geçiş oranı birlikte görüldü.'
        if nudge else
        'Bu oturumda mola önerisi için gerekli davranış örüntüsü ve süre koşulları birlikte oluşmadı.'
    )
    return {
        **asdict(features),
        'scroll_velocity': round(scroll_velocity, 2),
        'mean_dwell_time': round(mean_dwell, 2),
        'rapid_skip_ratio': round(rapid_skip_ratio, 3),
        'state': state,
        'nudge': nudge,
        'reason': reason,
        'thresholds': {
            'min_session_sec': 180,
            'scroll_velocity': 18,
            'rapid_skip_ratio': 0.60,
            'max_mean_dwell_sec': 3.2,
        },
        'disclaimer': 'Davranış örüntüsü değerlendirmesidir; tıbbi veya psikolojik tanı değildir.'
    }
