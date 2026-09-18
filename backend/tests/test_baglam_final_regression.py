from app.services.moderation import ContextualDemoModerationEngine

M = ContextualDemoModerationEngine()


def check(text):
    return M.analyze(text)


def test_normal_checkin_is_high_confidence_safe():
    r = check('Nasılsın, iyi misin?')
    assert r.safety_label == 'benign'
    assert r.style_label == 'literal'
    assert r.decision == 'allow'
    assert r.confidence >= .85
    assert r.harm_score <= .08
    assert r.sarcasm_score <= .08


def test_greeting_is_safe():
    r = check('Merhaba, nasılsın?')
    assert r.decision == 'allow'
    assert r.harm_score < .1


def test_polite_thanks_is_safe():
    r = check('Teşekkür ederim, çok yardımcı oldun.')
    assert r.decision == 'allow'
    assert r.safety_label == 'benign'


def test_sarcastic_contrast_detected_without_false_harm():
    r = check('Harika, yine sistemi çökerttin.')
    assert r.style_label == 'sarcasm_irony'
    assert r.sarcasm_score >= .75
    assert r.harm_score < .3
    assert r.decision == 'warn'


def test_object_criticism_not_personal_attack():
    r = check('Bu sistem berbat, daha iyi bir yöntem gerekiyor.')
    assert r.safety_label == 'constructive_criticism'
    assert r.decision == 'allow'
    assert r.harm_score < .2


def test_constructive_project_feedback_is_allowed():
    r = check('Bence kaynaklar yetersiz, daha açık açıklanabilir.')
    assert r.safety_label == 'constructive_criticism'
    assert r.decision == 'allow'


def test_targeted_insult_goes_to_review():
    r = check('Sen salaksın.')
    assert r.safety_label == 'toxic_attack'
    assert r.decision == 'review'
    assert r.harm_score >= .7


def test_inflected_targeted_insult_goes_to_review():
    r = check('Sen gerçekten beceriksizsin.')
    assert r.decision == 'review'
    assert r.harm_score >= .7


def test_explicit_threat_goes_to_review():
    r = check('Seni öldürürüm.')
    assert r.decision == 'review'
    assert r.harm_score >= .85


def test_safe_idiom_not_misread_as_violence():
    r = check('Gülmekten öldüm 😂')
    assert r.safety_label == 'benign'
    assert r.decision == 'allow'
    assert r.harm_score < .1


def test_ambiguous_short_phrase_warns():
    r = check('İyiymiş gerçekten...')
    assert r.decision == 'warn'
    assert r.safety_label == 'ambiguous_review'


def test_harassment_context_is_not_silently_allowed():
    r = check('Her gönderide bana sataşıyorsun, bırak artık.')
    assert r.safety_label == 'harassment'
    assert r.decision == 'review'


def test_meta_discussion_of_insult_is_not_attack():
    r = check('Kimseye salak demek doğru değil.')
    assert r.decision == 'allow'
    assert r.harm_score < .2


def test_negated_insult_is_not_direct_attack():
    r = check('Sen salak değilsin.')
    assert r.decision == 'allow'
    assert r.harm_score < .2


def test_plain_neutral_sentence_has_sane_risk_scores():
    r = check('Bugün hava çok güzel, yürüyüşe çıkacağım.')
    assert r.decision == 'allow'
    assert r.confidence >= .75
    assert r.harm_score <= .14
    assert r.sarcasm_score <= .12
