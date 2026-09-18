from app.services.moderation import ContextualDemoModerationEngine

M = ContextualDemoModerationEngine()


def r(text):
    return M.analyze(text)


def test_standalone_strong_profanity_is_not_silently_allowed():
    out = r('amk')
    assert out.decision in {'warn', 'review'}
    assert out.harm_score >= .45


def test_targeted_strong_profanity_goes_to_review():
    out = r('Sen tam bir orospusun.')
    assert out.decision == 'review'
    assert out.harm_score >= .75


def test_obfuscated_insult_is_detected():
    out = r('Sen s.a.l.a.k.s.ı.n')
    assert out.decision == 'review'


def test_ascii_turkish_insult_variant_is_detected():
    out = r('Sen serefsizsin.')
    assert out.decision == 'review'


def test_reported_abuse_is_not_treated_as_direct_attack():
    out = r('Bana salak dedi, bu hiç hoş değildi.')
    assert out.decision == 'allow'
    assert out.harm_score < .25


def test_rejecting_abuse_is_safe_context():
    out = r('Kimseye aptal demek doğru değil.')
    assert out.decision == 'allow'


def test_literal_animal_word_is_not_false_positive():
    out = r('Köpeğim bugün çok neşeli.')
    assert out.decision != 'review'


def test_malzeme_does_not_trigger_mal_insult():
    out = r('Bu malzeme çok dayanıklı.')
    assert out.decision != 'review'


def test_sikildim_does_not_trigger_profanity():
    out = r('Bugün evde çok sıkıldım.')
    assert out.decision != 'review'


def test_person_targeted_contextual_insult_is_detected():
    out = r('Sen malsın.')
    assert out.decision == 'review'


def test_unknown_low_confidence_text_is_not_forced_to_fake_high_confidence():
    out = r('zxqv prtkl mnop')
    assert out.confidence < .80
    assert out.decision == 'warn'


def test_confidence_means_classifier_confidence_not_safety():
    out = r('Sen salaksın.')
    assert out.confidence >= .80
    assert out.harm_score >= .70
    assert out.decision == 'review'


def test_obfuscated_strong_profanity_inflection_is_detected():
    out = r('Sen p.i.ç.s.i.n')
    assert out.decision == 'review'


def test_direct_imperative_profanity_is_reviewed():
    out = r('Siktir git.')
    assert out.decision == 'review'


def test_profane_object_criticism_warns_not_silent_allow():
    out = r('Bu sistem bok gibi.')
    assert out.decision == 'warn'
    assert out.harm_score >= .35


def test_plain_positive_material_sentence_is_safe():
    out = r('Bu malzeme çok iyi ve dayanıklı.')
    assert out.decision == 'allow'


def test_plain_positive_pet_sentence_is_safe():
    out = r('Köpeğim çok tatlı.')
    assert out.decision == 'allow'
