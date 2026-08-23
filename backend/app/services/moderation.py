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
MENTION_RE = re.compile(r'@[\w_]+', re.UNICODE)
SPACE_RE = re.compile(r'\s+')


def normalize_turkish(text: str) -> str:
    """Context-preserving Turkish normalization.

    Emojis, Turkish characters, punctuation and repeated letters are intentionally preserved.
    Only Unicode form, URLs, mentions and whitespace are normalized.
    """
    text = unicodedata.normalize('NFKC', text.strip())
    text = URL_RE.sub(' <URL> ', text)
    text = MENTION_RE.sub(' <USER> ', text)
    return SPACE_RE.sub(' ', text)


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


class ContextualDemoModerationEngine:
    """Real, local, reproducible ML prototype trained on a labeled synthetic dataset.

    This is intentionally NOT presented as BERTurk. It exists so the prototype has a
    measurable contextual classifier without requiring network/model downloads.
    """

    def __init__(self) -> None:
        self.safety_model = self._build_model()
        self.style_model = self._build_model()
        texts = [normalize_turkish(x[0]) for x in SYNTHETIC_DATA]
        safety = [x[1] for x in SYNTHETIC_DATA]
        style = [x[2] for x in SYNTHETIC_DATA]
        self.safety_model.fit(texts, safety)
        self.style_model.fit(texts, style)
        self.version = 'demo-tfidf-logreg-1.0'

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

        safety_label = safety_classes[int(safety_probs.argmax())]
        style_label = style_classes[int(style_probs.argmax())]
        safety_conf = float(max(safety_probs))
        style_conf = float(max(style_probs))
        confidence = round((safety_conf + style_conf) / 2, 4)
        harm_score = round(float(sum(p for c, p in zip(safety_classes, safety_probs) if c in {'harassment', 'toxic_attack'})), 4)
        sarcasm_score = round(float(style_probs[style_classes.index('sarcasm_irony')]), 4) if 'sarcasm_irony' in style_classes else 0.0

        # Conservative prototype decision: high-risk OR low confidence gets review; ambiguity gets warning.
        if harm_score >= 0.58:
            decision = 'review'
        elif safety_label == 'ambiguous_review' or confidence < 0.52 or sarcasm_score >= 0.55:
            decision = 'warn'
        else:
            decision = 'allow'

        explanations = {
            'benign': 'İfade, prototip model tarafından çoğunlukla zararsız içerik olarak yorumlandı.',
            'constructive_criticism': 'İfade kişiye saldırmak yerine fikir, yöntem veya içerik hakkında eleştiri örüntüsüne daha yakın görünüyor.',
            'harassment': 'İfade belirli bir kişiyi tekrar eden biçimde hedef alma veya rahatsız etme örüntüsüne yakın görünüyor.',
            'toxic_attack': 'İfade kişiye yönelik aşağılayıcı veya saldırgan bir anlatım örüntüsüne yakın görünüyor.',
            'ambiguous_review': 'İfadenin anlamı bağlama göre değişebilir; otomatik karar yerine kullanıcıya uyarı göstermek daha güvenlidir.',
        }
        style_text = {
            'literal': 'literal/doğrudan',
            'sarcasm_irony': 'sarkastik/ironik',
            'uncertain': 'belirsiz',
        }[style_label]
        latency = round((perf_counter() - start) * 1000, 2)
        return ModerationResult(
            normalized_text=normalized,
            safety_label=safety_label, style_label=style_label,
            harm_score=harm_score, sarcasm_score=sarcasm_score,
            confidence=confidence, decision=decision,
            explanation=explanations[safety_label],
            technical_explanation=f'Güvenlik sınıfı={safety_label}; anlatım biçimi={style_text}; TF-IDF kelime+karakter n-gram LogisticRegression demo modeli.',
            engine='ContextualDemoModerationEngine', model_version=self.version,
            latency_ms=latency,
        )


def evaluate_demo_model(output_path: Path) -> dict:
    """Evaluate on a deterministic held-out split; result is explicitly synthetic-prototype evidence."""
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
