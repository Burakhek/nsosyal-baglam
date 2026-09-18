from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
import json
import re
import unicodedata
from typing import Literal

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

SafetyLabel = Literal['benign', 'constructive_criticism', 'harassment', 'toxic_attack', 'ambiguous_review']
StyleLabel = Literal['literal', 'sarcasm_irony', 'uncertain']

URL_RE = re.compile(r'https?://\S+|www\.\S+', re.I)
MENTION_RE = re.compile(r'(?<![\w])@[\w_]+', re.UNICODE)
SPACE_RE = re.compile(r'\s+')
TOKEN_RE = re.compile(r"[a-zçğıöşü0-9']+", re.I)


def normalize_turkish(text: str) -> str:
    """Context-preserving Turkish normalization.

    Emojis, Turkish characters, punctuation and repeated letters are intentionally preserved.
    Only Unicode form, URLs, mentions and whitespace are normalized.
    """
    text = unicodedata.normalize('NFKC', text.strip())
    text = URL_RE.sub(' <URL> ', text)
    text = MENTION_RE.sub(' <USER> ', text)
    return SPACE_RE.sub(' ', text)


def tr_lower(text: str) -> str:
    # Python lower/casefold can produce a combining-dot sequence for Turkish İ.
    return text.translate(str.maketrans({'I': 'ı', 'İ': 'i'})).lower()


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(p in text for p in phrases)


def _has_root(tokens: list[str], roots: tuple[str, ...]) -> bool:
    return any(any(tok.startswith(root) for root in roots) for tok in tokens)


@dataclass
class ModerationResult:
    normalized_text: str
    safety_label: SafetyLabel
    style_label: StyleLabel
    harm_score: float
    sarcasm_score: float
    confidence: float
    decision: Literal['allow', 'warn', 'review']
    explanation: str
    technical_explanation: str
    engine: str
    model_version: str
    latency_ms: float


# This labeled set is intentionally kept small and synthetic so the report evidence remains
# reproducible. The final demo engine adds a deterministic Turkish context layer on top of
# this statistical baseline; it is not claimed to be BERTurk or a production model.
SYNTHETIC_DATA = [
    ('Bu tasarımı gerçekten çok beğendim.', 'benign', 'literal'),
    ('Eline sağlık, gayet temiz olmuş.', 'benign', 'literal'),
    ('Oğlum bunu nasıl yaptın la 😂', 'benign', 'literal'),
    ('Bugün hava çok güzel, yürüyüşe çıkacağım.', 'benign', 'literal'),
    ('Bu paylaşım çok faydalı olmuş teşekkürler.', 'benign', 'literal'),
    ('Kanka efsane olmuş 😂', 'benign', 'literal'),
    ('Bence renk seçimi çok başarılı.', 'benign', 'literal'),
    ('Açıklama net, teşekkür ederim.', 'benign', 'literal'),
    ('Ben farklı düşünüyorum ama fikrine saygı duyuyorum.', 'constructive_criticism', 'literal'),
    ('Fikir güzel ancak kaynakların yeterince açıklanmadığını düşünüyorum.', 'constructive_criticism', 'literal'),
    ('Bu bölüm anlaşılır değil, biraz daha örnek eklenebilir.', 'constructive_criticism', 'literal'),
    ('Katılmıyorum; veriler bu sonucu desteklemiyor.', 'constructive_criticism', 'literal'),
    ('Kod çalışıyor ancak isimlendirmeler daha açık olabilir.', 'constructive_criticism', 'literal'),
    ('Sunum iyi ama problem tanımı daha ölçülebilir yazılmalı.', 'constructive_criticism', 'literal'),
    ('Bence bu yaklaşım yerine daha basit bir yöntem denenebilir.', 'constructive_criticism', 'literal'),
    ('Sonuç ilginç fakat test sayısı az.', 'constructive_criticism', 'literal'),
    ('Mükemmel, yine uygulamayı çökerttin 👏', 'benign', 'sarcasm_irony'),
    ('Harika ya, tam da ihtiyacımız olan şey bir hata daha.', 'benign', 'sarcasm_irony'),
    ('Kralsın, bunu da yanlış yaptın 😂', 'benign', 'sarcasm_irony'),
    ('Helal olsun, yine bütün işi sen batırdın.', 'benign', 'sarcasm_irony'),
    ('Ne kadar hızlısın, sadece iki saat geciktin.', 'benign', 'sarcasm_irony'),
    ('Süper, yine başa döndük.', 'benign', 'sarcasm_irony'),
    ('Şahane olmuş, hiçbir şey çalışmıyor.', 'benign', 'sarcasm_irony'),
    ('Tabii tabii, sen her şeyi biliyorsun zaten.', 'benign', 'sarcasm_irony'),
    ('Beni bu grupta sürekli küçümsemen hoş değil.', 'harassment', 'literal'),
    ('Her paylaşımımın altında benimle uğraşıyorsun, bırak artık.', 'harassment', 'literal'),
    ('Beni hedef gösterip durma.', 'harassment', 'literal'),
    ('Sürekli dalga geçmen rahatsız edici.', 'harassment', 'literal'),
    ('Benimle kişisel olarak uğraşmayı kes.', 'harassment', 'literal'),
    ('Her seferinde ismimi verip beni aşağılıyorsun.', 'harassment', 'literal'),
    ('Bu kişiye topluca yüklenmeyin, bu tacize dönüşüyor.', 'benign', 'literal'),
    ('İnsanları hedef alarak küçük düşürmek doğru değil.', 'constructive_criticism', 'literal'),
    ('Sen hiçbir şey bilmiyorsun, rezil birisin.', 'toxic_attack', 'literal'),
    ('Bu kadar beceriksiz biri görmedim.', 'toxic_attack', 'literal'),
    ('Yaptığın her şey berbat, senden bir şey olmaz.', 'toxic_attack', 'literal'),
    ('Saçmalamayı bırak, ne konuştuğunu bilmiyorsun.', 'toxic_attack', 'literal'),
    ('Senin fikirlerin tamamen değersiz.', 'toxic_attack', 'literal'),
    ('Bu kadar boş konuşmayı nasıl başarıyorsun?', 'toxic_attack', 'sarcasm_irony'),
    ('Aferin, yine herkesi kendinden soğuttun.', 'toxic_attack', 'sarcasm_irony'),
    ('Dahi arkadaşımız yine yanlış bilgi vermiş.', 'toxic_attack', 'sarcasm_irony'),
    ('Bunu da ancak sen yapardın.', 'ambiguous_review', 'uncertain'),
    ('İyiymiş gerçekten...', 'ambiguous_review', 'uncertain'),
    ('Sen bilirsin tabii.', 'ambiguous_review', 'uncertain'),
    ('Çok iyi olmuş (!) ', 'ambiguous_review', 'sarcasm_irony'),
    ('Vay be ne başarı ama.', 'ambiguous_review', 'sarcasm_irony'),
    ('Beni bitirdi 😂', 'benign', 'uncertain'),
    ('Bu maç beni bitirdi.', 'benign', 'literal'),
    ('Adamı resmen gömdü, tartışmada cevap veremedi.', 'benign', 'literal'),
    ('Sunum rakiplerini gömdü resmen.', 'benign', 'literal'),
    ('Bu yorumun tonu sert ama eleştiri kısmı anlaşılır.', 'constructive_criticism', 'literal'),
    ('çoook iyi olmuş 😂', 'benign', 'uncertain'),
    ('B U N U da mı yanlış yaptın?', 'ambiguous_review', 'uncertain'),
    ('Yine mi sen... neyse.', 'ambiguous_review', 'uncertain'),
    ('Bu paylaşımı anlamadım, açıklayabilir misin?', 'constructive_criticism', 'literal'),
    ('Burada kişiye değil fikre itiraz ediyorum.', 'constructive_criticism', 'literal'),
    ('Tam bir felaket olmuş, ama kişisel algılama; tasarımdan bahsediyorum.', 'constructive_criticism', 'literal'),
    ('Seninle değil, yönteminle ilgili sorunum var.', 'constructive_criticism', 'literal'),
    ('Bu yöntemi hiç başarılı bulmadım.', 'constructive_criticism', 'literal'),
    ('Bence sonuçlar abartılmış.', 'constructive_criticism', 'literal'),
    ('Bu gönderi bana komik geldi 😂', 'benign', 'literal'),
    ('Gülmekten öldüm 😂', 'benign', 'literal'),
    ('Bugünkü ders kafamı yedi.', 'benign', 'literal'),
    ('Proje patladı derken çok ilgi gördüğünü kastediyorum.', 'benign', 'literal'),
    ('Bu fikir uçmuş, bayağı yaratıcı olmuş.', 'benign', 'literal'),
    ('Sen var ya gerçekten ilginç birisin.', 'ambiguous_review', 'uncertain'),
    ('Aynen kardeşim kesin öyledir.', 'ambiguous_review', 'sarcasm_irony'),
    ('İnanılmaz mantıklı(!)', 'ambiguous_review', 'sarcasm_irony'),
    ('Sana katılmıyorum çünkü örnek yanlış seçilmiş.', 'constructive_criticism', 'literal'),
    ('Bu yorum gereksiz sert olmuş.', 'constructive_criticism', 'literal'),
    ('Kimseyi hedef almadan tartışabiliriz.', 'benign', 'literal'),
    ('Topluluğu aşağılamak yerine fikri tartışalım.', 'benign', 'literal'),
    ('Sürekli aynı kişiyi etiketleyip dalga geçmek doğru değil.', 'benign', 'literal'),
    ('Beni bir daha bu şekilde etiketleme.', 'harassment', 'literal'),
    ('Yeter artık, her gönderide bana sataşıyorsun.', 'harassment', 'literal'),
    ('Kişisel saldırıyı bırak.', 'harassment', 'literal'),
    ('Senden gerçekten bıktım, her yerde beni küçümsüyorsun.', 'harassment', 'literal'),
    ('Bu cümle bağlama göre sert algılanabilir.', 'benign', 'literal'),
    ('Bugün harikasın.', 'benign', 'literal'),
    ('Tabii, en iyi fikir yine senden çıktı (!) ', 'ambiguous_review', 'sarcasm_irony'),
]

# Context layer used by the live demo. The statistical TF-IDF/LogReg baseline is kept
# unchanged for report reproducibility; this layer adds transparent Turkish safety/context
# handling for obvious cases that a 79-example baseline cannot reliably cover.
SAFE_SOCIAL_PHRASES = (
    'merhaba', 'selam', 'günaydın', 'iyi akşamlar', 'iyi geceler', 'hoş geldin',
    'nasılsın', 'nasılsınız', 'iyi misin', 'iyi misiniz', 'ne haber', 'naber',
    'teşekkür ederim', 'teşekkürler', 'rica ederim', 'eline sağlık', 'geçmiş olsun',
    'kolay gelsin', 'görüşürüz', 'kendine iyi bak', 'iyi çalışmalar',
)
POSITIVE_WORDS = (
    'harika', 'mükemmel', 'süper', 'şahane', 'efsane', 'kralsın', 'aferin',
    'helal olsun', 'inanılmaz', 'çok iyi', 'ne kadar hızlı',
)
NEGATIVE_EVENT_WORDS = (
    'çökert', 'batır', 'yanlış', 'hata', 'gecik', 'çalışmıyor', 'bozul', 'başa döndük',
    'mahvet', 'rezil et', 'yine olmadı', 'hiçbir şey çalışmıyor',
)
AMBIGUOUS_PHRASES = (
    'sen bilirsin', 'bunu da ancak sen yapardın', 'yine mi sen', 'neyse',
    'iyiymiş gerçekten', 'ilginç birisin', 'vay be ne başarı',
)
HARASSMENT_PHRASES = (
    'beni hedef göster', 'benimle uğraş', 'bana sataş', 'beni küçümse', 'beni aşağıla',
    'sürekli dalga geç', 'kişisel saldırıyı bırak', 'bir daha bu şekilde etiketleme',
    'her gönderide bana', 'her paylaşımımın altında',
)
THREAT_PHRASES = (
    'seni öldür', 'seni gebert', 'seni döver', 'seni mahveder', 'sana zarar ver',
    'sizi öldür', 'sizi gebert', 'sizi döver', 'sana gününü göster', 'seni parçala',
)

# High-confidence insult stems. Matching is done after Turkish-aware de-obfuscation and
# common suffix handling. Stems that have innocent lexical collisions are handled separately.
DIRECT_INSULT_ROOTS = (
    'salak', 'aptal', 'gerizekal', 'ahmak', 'budala', 'beceriksiz', 'rezil',
    'değersiz', 'serefsiz', 'şerefsiz', 'terbiyesiz', 'iğrenç', 'dangalak',
    'yavşak', 'yavsak', 'pezevenk', 'kaltak', 'kahpe', 'puşt', 'pust',
    'hıyar', 'hiyar', 'ezik', 'embesil', 'moron', 'gerzek', 'lavuk', 'dallama', 'dalyarak', 'dingil',
    'idiot', 'stupid', 'asshole', 'bitch',
)

# Strong profanity patterns. We intentionally do not use a generic 'am' or generic 'sik*'
# prefix because those create Turkish false positives (e.g. 'ama', 'amca', 'siklet').
STRONG_PROFANITY_EXACT = {
    'amk', 'aq', 'mk', 'amq', 'siktir', 'siktirgit', 'sik', 'sikeyim', 'sikiyim',
    'sikerim', 'sikik', 'orospu', 'orospucocugu', 'orospuçocuğu', 'orospuçocugu',
    'piç', 'pic', 'yarrak', 'yarak', 'amcık', 'amcik', 'göt', 'got', 'götlek', 'gotlek',
    'götveren', 'gotveren', 'ibne', 'pezevenk', 'yavşak', 'yavsak', 'puşt', 'pust',
    'fuck', 'fucking', 'shit',
}
STRONG_PROFANITY_PREFIXES = (
    'siktir', 'orospu', 'orospuc', 'amına', 'amina', 'amını', 'amini', 'amcık', 'amcik',
    'yarrak', 'yarak', 'götveren', 'gotveren', 'pezevenk', 'yavşak', 'yavsak',
    'piç', 'pic', 'ibne', 'puşt', 'pust', 'fuck',
)

# Words such as "mal", "öküz", "eşek", "it", "köpek" can be literal nouns. They become
# abusive only with a clear person target / second-person inflection.
CONTEXTUAL_INSULT_WORDS = {'mal', 'öküz', 'okuz', 'eşek', 'esek', 'it', 'köpek', 'kopek'}
SECOND_PERSON_ROOTS = ('sen', 'seni', 'sana', 'senin', 'siz', 'sizi', 'size', 'sizin')
PERSON_TARGET_WORDS = ('adam', 'herif', 'kişi', 'kisi', 'insan', 'çocuk', 'cocuk', 'kadın', 'kadin', 'erkek')
CRITIQUE_OBJECTS = (
    'sistem', 'tasarım', 'kod', 'uygulama', 'yöntem', 'sonuç', 'veri', 'kaynak',
    'sunum', 'proje', 'fikir', 'model', 'algoritma', 'arayüz', 'rapor', 'bölüm', 'metin',
)
CRITIQUE_MARKERS = (
    'bence', 'katılmıyorum', 'ancak', 'fakat', 'ama', 'daha iyi', 'daha açık',
    'daha anlaşılır', 'eksik', 'yetersiz', 'desteklemiyor', 'geliştirilebilir',
    'iyileştirilebilir', 'örnek eklenebilir', 'açıklanabilir',
)
OBJECT_NEGATIVE_WORDS = ('berbat', 'kötü', 'başarısız', 'yanlış', 'yetersiz', 'zayıf', 'hatalı', 'eksik', 'saçma')
PROFANE_OBJECT_PHRASES = ('bok gibi', 'boktan', 'rezaletin dibi')
PLAIN_POSITIVE_WORDS = ('güzel', 'iyi', 'başarılı', 'dayanıklı', 'tatlı', 'faydalı', 'yararlı', 'seviyorum', 'beğendim')
IDIOM_SAFE_PHRASES = (
    'gülmekten öldüm', 'kafamı yedi', 'maç beni bitirdi', 'proje patladı',
    'fikir uçmuş', 'rakiplerini gömdü', 'tartışmada gömdü',
)
META_SAFETY_PHRASES = (
    'demek doğru değil', 'söylemek doğru değil', 'hakaret etmeyelim',
    'hakaret etmek doğru değil', 'küfür etmeyelim', 'küfür etmek doğru değil',
    'aşağılamayalım', 'kimseyi aşağılamayalım', 'kişiye hakaret etmeyelim',
    'bu bir hakaret', 'bu bir küfür', 'hakaret sayılır', 'küfür sayılır',
    'kelimesi hakaret', 'sözcüğü hakaret', 'ifadesi hakaret',
)
REPORTING_PHRASES = (
    'bana dedi', 'bana demiş', 'bana yazdı', 'bana söyledi', 'ona dedi', 'ona demiş',
    'diye hakaret etti', 'diye küfür etti', 'kelimesini kullandı', 'sözcüğünü kullandı',
    'ifadesini kullandı', 'alıntı olarak', 'örnek olarak',
)

LEET_TRANS = str.maketrans({'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '$': 's'})
ASCII_FOLD = str.maketrans({'ç':'c', 'ğ':'g', 'ö':'o', 'ş':'s', 'ü':'u', 'Ç':'c', 'Ğ':'g', 'Ö':'o', 'Ş':'s', 'Ü':'u'})
SPACED_WORD_RE = re.compile(r'(?<!\w)(?:[a-zçğıöşü0-9$][\s._*\-]+){2,}[a-zçğıöşü0-9$](?!\w)', re.I)
SECOND_PERSON_SUFFIX_RE = re.compile(r'(?:sın|sin|sun|sün|sınız|siniz|sunuz|sünüz)$')


def _fold_for_match(text: str) -> str:
    """Build a matching form without changing the text shown to the user.

    Handles common leetspeak and spaced/censored spellings while preserving Turkish dotless-ı
    so innocent words like 'sıkıldım' are not confused with a profanity token.
    """
    low = tr_lower(text)
    low = low.translate(LEET_TRANS)
    # Join only sequences that look intentionally split into single characters: s.a.l.a.k etc.
    low = SPACED_WORD_RE.sub(lambda m: re.sub(r'[\s._*\-]+', '', m.group(0)), low)
    return low


def _token_forms(text: str) -> list[str]:
    base = _fold_for_match(text)
    raw = TOKEN_RE.findall(base)
    forms: list[str] = []
    for tok in raw:
        forms.append(tok)
        folded = tok.translate(ASCII_FOLD)
        if folded != tok:
            forms.append(folded)
        # Obfuscated profanity often stretches letters. This variant is for lexicon matching only.
        collapsed = re.sub(r'(.)\1{2,}', r'\1', folded)
        if collapsed not in forms:
            forms.append(collapsed)
    return forms


def _root_hits(tokens: list[str], roots: tuple[str, ...]) -> list[str]:
    hits = []
    for tok in tokens:
        for root in roots:
            if tok.startswith(root):
                hits.append(root)
                break
    return hits


def _strong_profanity_hits(tokens: list[str]) -> list[str]:
    hits: list[str] = []
    for tok in tokens:
        if tok in STRONG_PROFANITY_EXACT or any(tok.startswith(p) for p in STRONG_PROFANITY_PREFIXES):
            hits.append(tok)
    return hits


def _contextual_insult_hit(tokens: list[str], targeted: bool) -> bool:
    if not targeted:
        return False
    for tok in tokens:
        if tok in CONTEXTUAL_INSULT_WORDS:
            return True
        for w in CONTEXTUAL_INSULT_WORDS:
            if tok.startswith(w) and SECOND_PERSON_SUFFIX_RE.search(tok[len(w):]):
                return True
    return False


def _looks_targeted(low: str, tokens: list[str], insult_hits: list[str]) -> bool:
    token_set = set(tokens)
    if '<user>' in low or any(t in token_set for t in SECOND_PERSON_ROOTS):
        return True
    if any(t in token_set for t in PERSON_TARGET_WORDS):
        return True
    # Turkish predicative insult forms: salaksın, aptalsınız, etc.
    for tok in tokens:
        for root in insult_hits:
            if tok.startswith(root) and SECOND_PERSON_SUFFIX_RE.search(tok[len(root):]):
                return True
    return False


def _negated_or_rejected_insult(low: str, tokens: list[str], insult_hits: list[str]) -> bool:
    if not insult_hits:
        return False
    # Keep this deliberately narrow. "X değil, Y'sin" should not become safe merely because
    # a negation token appears somewhere in the sentence.
    if any(x in low for x in META_SAFETY_PHRASES):
        return True
    if any(x in low for x in REPORTING_PHRASES):
        return True
    if any(w in low.split() for w in ('bana', 'ona', 'bize', 'onlara')) and any(v in low for v in ('dedi', 'demiş', 'demisti', 'demişti', 'yazdı', 'yazmış', 'söyledi', 'söylemiş')):
        return True
    if 'kimseye' in low and ('demek' in low or 'söylemek' in low) and ('doğru değil' in low or 'yanlış' in low):
        return True
    if ('değilsin' in low or 'degilsin' in low) and len(set(insult_hits)) == 1 and not any(x in low for x in (' ama ', ' fakat ', ' ancak ')):
        return True
    if re.search(r'\b(?:salak|aptal|gerizekalı|gerizekali|ahmak|budala|beceriksiz|şerefsiz|serefsiz)\s+değil\b', low):
        return True
    return False


class ContextualDemoModerationEngine:
    """Hybrid Turkish context prototype: statistical baseline + transparent safety rules.

    The TF-IDF word/character n-gram LogisticRegression model stays as the reproducible
    statistical baseline. The live demo adds a deterministic Turkish context/profanity layer
    for high-confidence cases, obfuscation handling, target-vs-object distinction, negation,
    reporting/meta context and common sarcasm contrasts. No cloud API or BERTurk is required.
    """

    def __init__(self) -> None:
        self.safety_model = self._build_model()
        self.style_model = self._build_model()
        texts = [normalize_turkish(x[0]) for x in SYNTHETIC_DATA]
        safety = [x[1] for x in SYNTHETIC_DATA]
        style = [x[2] for x in SYNTHETIC_DATA]
        self.safety_model.fit(texts, safety)
        self.style_model.fit(texts, style)
        self.version = 'hybrid-tr-context-3.0'

    @staticmethod
    def _build_model():
        features = FeatureUnion([
            ('word', TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ('char', TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1, sublinear_tf=True)),
        ])
        return __import__('sklearn.pipeline').pipeline.Pipeline([
            ('features', features),
            ('clf', LogisticRegression(max_iter=1200, class_weight='balanced', random_state=42)),
        ])

    @staticmethod
    def _rule_layer(normalized: str) -> dict:
        low = _fold_for_match(normalized)
        tokens = _token_forms(normalized)
        token_set = set(tokens)
        insult_hits = _root_hits(tokens, DIRECT_INSULT_ROOTS)
        provisional_target = (
            '<user>' in low
            or any(t in token_set for t in SECOND_PERSON_ROOTS)
            or any(t in token_set for t in PERSON_TARGET_WORDS)
        )
        contextual_insult = _contextual_insult_hit(tokens, provisional_target)
        strong_hits = _strong_profanity_hits(tokens)
        profane_object = _contains_any(low, PROFANE_OBJECT_PHRASES)
        obscene_emoji = '🖕' in normalized
        has_insult = bool(insult_hits or contextual_insult)
        targeted = _looks_targeted(low, tokens, insult_hits) or contextual_insult
        if ('siktir' in token_set or any(t.startswith('siktir') for t in tokens)) and any(t in token_set for t in ('git', 'gidin', 'defol')):
            targeted = True
        has_threat = _contains_any(low, THREAT_PHRASES)
        has_harassment = _contains_any(low, HARASSMENT_PHRASES)
        has_object = _contains_any(low, CRITIQUE_OBJECTS)
        has_critique_marker = _contains_any(low, CRITIQUE_MARKERS)
        has_object_negative = _contains_any(low, OBJECT_NEGATIVE_WORDS)
        has_safe_social = _contains_any(low, SAFE_SOCIAL_PHRASES)
        has_idiom_safe = _contains_any(low, IDIOM_SAFE_PHRASES)
        meta_or_report = _negated_or_rejected_insult(low, tokens, insult_hits + strong_hits)
        has_positive = _contains_any(low, POSITIVE_WORDS)
        has_plain_positive = _contains_any(low, PLAIN_POSITIVE_WORDS)
        has_negative_event = _contains_any(low, NEGATIVE_EVENT_WORDS)
        explicit_sarcasm = (
            '(!)' in low
            or 'tabii tabii' in low
            or ('aynen' in low and ('kesin' in low or 'tabii' in low))
            or (has_positive and has_negative_event and ('yine' in low or ',' in low or 'ama' in low))
            or ('ne kadar hızlı' in low and ('sadece' in low or 'gecik' in low))
        )
        ambiguous = _contains_any(low, AMBIGUOUS_PHRASES) or ('...' in low and len(tokens) <= 8)

        # Priority: explicit threat > quoted/rejected profanity > targeted profanity/insult >
        # untargeted profanity > harassment > sarcasm > object criticism > safe context.
        if has_threat:
            return {
                'safety': 'toxic_attack', 'style': 'literal', 'strength': .99,
                'harm': .98, 'sarcasm': .02,
                'explanation': 'İfade doğrudan tehdit/saldırı örüntüsü taşıdığı için yüksek riskli olarak değerlendirildi.',
                'reason': 'explicit_threat_pattern',
            }

        if (has_insult or strong_hits) and meta_or_report:
            return {
                'safety': 'constructive_criticism' if _contains_any(low, META_SAFETY_PHRASES) else 'benign',
                'style': 'literal', 'strength': .92,
                'harm': .06, 'sarcasm': .02,
                'explanation': 'Aşağılayıcı/küfürlü sözcük doğrudan saldırı amacıyla değil; alıntı, bildirim, reddetme veya üst-bağlam içinde kullanılıyor.',
                'reason': 'quoted_reported_or_rejected_abuse',
            }

        if strong_hits and targeted:
            return {
                'safety': 'toxic_attack', 'style': 'literal', 'strength': .99,
                'harm': .97, 'sarcasm': .03,
                'explanation': 'İfade kişiye yöneltilmiş açık küfür/aşağılama örüntüsü taşıyor; yayın öncesi insan incelemesi önerildi.',
                'reason': 'targeted_strong_profanity',
            }

        if has_insult and targeted:
            return {
                'safety': 'toxic_attack', 'style': 'literal', 'strength': .98,
                'harm': .94, 'sarcasm': .04,
                'explanation': 'İfade kişiye yöneltilmiş doğrudan aşağılayıcı/saldırgan sözcük örüntüsü taşıyor.',
                'reason': 'targeted_direct_insult',
            }

        if obscene_emoji and targeted:
            return {
                'safety': 'toxic_attack', 'style': 'literal', 'strength': .96,
                'harm': .90, 'sarcasm': .04,
                'explanation': 'İfade kişiye yöneltilmiş açık saldırgan jest/argo sinyali taşıyor; inceleme önerildi.',
                'reason': 'targeted_abusive_emoji',
            }

        if profane_object:
            return {
                'safety': 'ambiguous_review', 'style': 'literal', 'strength': .92,
                'harm': .48, 'sarcasm': .03,
                'explanation': 'İfade kişi hedeflemekten çok nesne/fikir hakkında kaba veya küfürlü bir değerlendirme içeriyor; yayın öncesi dilin gözden geçirilmesi önerildi.',
                'reason': 'profane_object_criticism',
            }

        # Strong profanity without a clear person target should never silently become "safe".
        # It receives a reversible warning rather than an automatic personal-attack claim.
        if strong_hits:
            return {
                'safety': 'ambiguous_review', 'style': 'literal', 'strength': .96,
                'harm': .62, 'sarcasm': .03,
                'explanation': 'İfade açık küfür/argo sinyali içeriyor; belirgin kişi hedefi bulunmadığı için doğrudan kişisel saldırı denmedi, ancak yayın öncesi bağlam kontrolü önerildi.',
                'reason': 'untargeted_strong_profanity',
            }

        if has_harassment:
            return {
                'safety': 'harassment', 'style': 'literal', 'strength': .92,
                'harm': .76, 'sarcasm': .04,
                'explanation': 'İfade tekrar eden hedef alma veya rahatsız etme bağlamına işaret ediyor; insan incelemesi daha güvenli.',
                'reason': 'harassment_context',
            }

        if explicit_sarcasm:
            return {
                'safety': 'benign', 'style': 'sarcasm_irony', 'strength': .94,
                'harm': .08, 'sarcasm': .94,
                'explanation': 'Övgü biçimindeki ifade ile olumsuz olay aynı cümlede çeliştiği için ironi/sarkazm sinyali güçlü; tek başına kişisel saldırı kabul edilmedi.',
                'reason': 'sarcastic_contrast',
            }

        # Profanity aimed at an object/idea is still coarse language, but not necessarily a person attack.
        # Mild object criticism without profanity remains allowed.
        if has_object and (has_critique_marker or has_object_negative):
            return {
                'safety': 'constructive_criticism', 'style': 'literal', 'strength': .91,
                'harm': .06, 'sarcasm': .03,
                'explanation': 'Olumsuz değerlendirme kişiye değil fikir, yöntem, sistem veya içerik gibi bir nesneye yöneliyor; eleştiri olarak yorumlandı.',
                'reason': 'object_focused_criticism',
            }

        if has_idiom_safe:
            return {
                'safety': 'benign', 'style': 'literal', 'strength': .92,
                'harm': .03, 'sarcasm': .03,
                'explanation': 'İfade Türkçede mecaz/deyimsel kullanım örüntüsüne uyuyor; doğrudan zarar veya saldırı anlamı çıkarılmadı.',
                'reason': 'safe_idiom',
            }

        if has_safe_social and not has_insult and not has_threat and not strong_hits and not has_object_negative:
            return {
                'safety': 'benign', 'style': 'literal', 'strength': .97,
                'harm': .02, 'sarcasm': .01,
                'explanation': 'İfade selamlaşma, hâl-hatır sorma veya nezaket bağlamında; zararsız ve doğrudan iletişim olarak yorumlandı.',
                'reason': 'safe_social_checkin',
            }

        if ambiguous:
            return {
                'safety': 'ambiguous_review', 'style': 'uncertain', 'strength': .76,
                'harm': .10, 'sarcasm': .48,
                'explanation': 'İfade kısa veya bağlama bağımlı; niyetin kesinleşmesi için temkinli bir uyarı daha uygun.',
                'reason': 'context_ambiguity',
            }

        if has_plain_positive and not (has_insult or strong_hits or has_threat or has_harassment or explicit_sarcasm or profane_object):
            return {
                'safety': 'benign', 'style': 'literal', 'strength': .92,
                'harm': .03, 'sarcasm': .03,
                'explanation': 'İfade olumlu/zararsız gündelik değerlendirme örüntüsünde; belirgin saldırı, tehdit veya argo sinyali bulunmadı.',
                'reason': 'plain_positive_context',
            }

        if has_insult:
            return {
                'safety': 'toxic_attack', 'style': 'literal', 'strength': .88,
                'harm': .80, 'sarcasm': .04,
                'explanation': 'İfade aşağılayıcı/saldırgan sözcük örüntüsü içeriyor; hedef bağlamı tam açık olmasa da inceleme önerildi.',
                'reason': 'direct_insult_without_explicit_target',
            }

        return {'reason': 'statistical_backoff'}

    def analyze(self, text: str) -> ModerationResult:
        start = perf_counter()
        normalized = normalize_turkish(text)
        if not normalized:
            raise ValueError('Gönderi metni boş olamaz.')
        if len(normalized) > 1000:
            raise ValueError('Gönderi metni 1000 karakteri aşamaz.')

        safety_probs = self.safety_model.predict_proba([normalized])[0]
        safety_classes = list(self.safety_model.classes_)
        style_probs = self.style_model.predict_proba([normalized])[0]
        style_classes = list(self.style_model.classes_)

        base_safety_label = str(safety_classes[int(safety_probs.argmax())])
        base_style_label = str(style_classes[int(style_probs.argmax())])
        safety_conf = float(max(safety_probs))
        style_conf = float(max(style_probs))
        base_confidence = (safety_conf + style_conf) / 2
        # Coverage is used only to avoid presenting an unfamiliar sentence as highly certain.
        # It does not change the report's held-out baseline metrics.
        word_vectorizer = next(t for n, t in self.safety_model.named_steps['features'].transformer_list if n == 'word')
        lexical_tokens = TOKEN_RE.findall(tr_lower(normalized))
        known_tokens = sum(1 for t in lexical_tokens if t in word_vectorizer.vocabulary_)
        word_coverage = known_tokens / max(1, len(lexical_tokens))
        base_harm = float(sum(p for c, p in zip(safety_classes, safety_probs) if c in {'harassment', 'toxic_attack'}))
        base_sarcasm = float(style_probs[style_classes.index('sarcasm_irony')]) if 'sarcasm_irony' in style_classes else 0.0

        rule = self._rule_layer(normalized)
        if rule.get('safety'):
            safety_label: SafetyLabel = rule['safety']
            style_label: StyleLabel = rule['style']
            rule_strength = float(rule['strength'])
            confidence = clamp(0.90 * rule_strength + 0.10 * base_confidence)
            harm_score = clamp(0.92 * float(rule['harm']) + 0.08 * base_harm)
            sarcasm_score = clamp(0.92 * float(rule['sarcasm']) + 0.08 * base_sarcasm)
            explanation = rule['explanation']
        else:
            safety_label = base_safety_label
            style_label = base_style_label
            harm_score = base_harm
            sarcasm_score = base_sarcasm
            confidence = base_confidence

            # Do not manufacture high confidence for unseen text. A small 79-example baseline can be
            # uncertain; uncertainty should surface as a reversible warning rather than a false "safe".
            if safety_label in {'benign', 'constructive_criticism'} and harm_score < .35 and sarcasm_score < .45:
                harm_score = min(.18, harm_score * .50)
                if style_label == 'literal':
                    sarcasm_score = min(.15, sarcasm_score * .50)
                if word_coverage >= .60 and base_confidence >= .40:
                    confidence = max(.78, base_confidence)

            explanations = {
                'benign': 'İfade, prototip model tarafından zararsız içerik sınıfına daha yakın yorumlandı.',
                'constructive_criticism': 'İfade kişiye saldırmak yerine fikir, yöntem veya içerik hakkında eleştiri örüntüsüne daha yakın görünüyor.',
                'harassment': 'İfade belirli bir kişiyi tekrar eden biçimde hedef alma veya rahatsız etme örüntüsüne yakın görünüyor.',
                'toxic_attack': 'İfade kişiye yönelik aşağılayıcı veya saldırgan bir anlatım örüntüsüne yakın görünüyor.',
                'ambiguous_review': 'İfadenin anlamı bağlama göre değişebilir; otomatik karar yerine kullanıcıya uyarı göstermek daha güvenlidir.',
            }
            explanation = explanations[safety_label]

        # Decision policy: clear harm -> review; profanity/ambiguity/sarcasm/low confidence -> warning.
        if harm_score >= 0.72 or (safety_label in {'toxic_attack', 'harassment'} and harm_score >= .68):
            decision = 'review'
        elif safety_label == 'ambiguous_review' or sarcasm_score >= 0.65:
            decision = 'warn'
        elif confidence < 0.56:
            decision = 'warn'
            if rule.get('reason') == 'statistical_backoff':
                explanation += ' Model, verdiği karardan yeterince emin olmadığı için kesin güvenli kararı vermek yerine bağlam kontrolü önerdi.'
        else:
            decision = 'allow'

        style_text = {
            'literal': 'literal/doğrudan',
            'sarcasm_irony': 'sarkastik/ironik',
            'uncertain': 'belirsiz',
        }[style_label]
        latency = round((perf_counter() - start) * 1000, 2)
        return ModerationResult(
            normalized_text=normalized,
            safety_label=safety_label,
            style_label=style_label,
            harm_score=round(harm_score, 4),
            sarcasm_score=round(sarcasm_score, 4),
            confidence=round(confidence, 4),
            decision=decision,
            explanation=explanation,
            technical_explanation=(
                f'Güvenlik sınıfı={safety_label}; anlatım biçimi={style_text}; '
                f'yerel TF-IDF kelime+karakter n-gram LogisticRegression taban modeli + '
                f'şeffaf Türkçe bağlam/küfür katmanı; bağlam_yolu={rule.get("reason", "statistical_backoff")}. '
                'Arayüzdeki model güveni ve sinyal yüzdeleri kalibre edilmiş olasılık değildir.'
            ),
            engine='ContextualDemoModerationEngine',
            model_version=self.version,
            latency_ms=latency,
        )


def evaluate_demo_model(output_path: Path) -> dict:
    """Evaluate the statistical baseline on a deterministic held-out split.

    This keeps the technical-report evidence comparable. It does not claim to measure every
    deterministic context rule in the final demo engine.
    """
    texts = [normalize_turkish(x[0]) for x in SYNTHETIC_DATA]
    labels = [x[1] for x in SYNTHETIC_DATA]
    train_x, test_x, train_y, test_y = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )
    model = ContextualDemoModerationEngine._build_model()
    model.fit(train_x, train_y)
    pred = model.predict(test_x)
    metrics = {
        'status': 'ACTUAL_SYNTHETIC_PROTOTYPE',
        'dataset_type': 'synthetic prototype dataset',
        'metric_scope': 'statistical baseline only; final demo also uses deterministic Turkish context rules',
        'train_size': len(train_x), 'test_size': len(test_x),
        'macro_f1': round(float(f1_score(test_y, pred, average='macro')), 4),
        'weighted_f1': round(float(f1_score(test_y, pred, average='weighted')), 4),
        'macro_precision': round(float(precision_score(test_y, pred, average='macro', zero_division=0)), 4),
        'macro_recall': round(float(recall_score(test_y, pred, average='macro', zero_division=0)), 4),
        'labels': sorted(set(labels)),
        'confusion_matrix': confusion_matrix(test_y, pred, labels=sorted(set(labels))).tolist(),
        'classification_report': classification_report(test_y, pred, zero_division=0, output_dict=True),
        'limitations': 'Synthetic small dataset; these values are not NSosyal production performance or a BERTurk benchmark.'
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    return metrics
