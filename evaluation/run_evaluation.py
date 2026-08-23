from pathlib import Path
import json, statistics, time, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from app.services.moderation import ContextualDemoModerationEngine, evaluate_demo_model
from app.services.ranking import PostFeatures, rank_posts, exposure_metrics
from app.services.wellbeing import SessionFeatures, evaluate

out=ROOT/'evaluation'/'results'; out.mkdir(parents=True,exist_ok=True)
mod=evaluate_demo_model(out/'moderation_metrics.json')
posts=[
    PostFeatures(1,'TeknoMerak','large',120000,'Yerli yapay zekâ üzerine kısa bir kaynak listesi hazırladım.',0.91,0.87,0.82,0.89,980,16000),
    PostFeatures(2,'YeniFikir','small',420,'Türkçede ironi ve bağlamı anlamak için neden yalnızca kelime filtresi yetmiyor?',0.89,0.92,0.96,0.94,68,420),
    PostFeatures(3,'KodDefteri','medium',8500,'Bugün FastAPI ile küçük bir öneri sistemi deneyi yaptım.',0.82,0.84,0.91,0.92,160,4100),
    PostFeatures(4,'GündemHızlı','large',280000,'Herkes bunu konuşuyor! Detaylar burada.',0.67,0.49,0.40,0.97,1450,19500),
    PostFeatures(5,'MinikAtölye','small',180,'Yeni üreticilerin keşfedilmesi için pozisyon bazlı görünürlük ölçümü denedim.',0.86,0.90,0.95,0.88,42,260),
    PostFeatures(6,'BilimNotu','medium',21000,'Öneri sistemlerinde relevance ile exposure fairness arasındaki dengeyi nasıl ölçebiliriz?',0.94,0.93,0.94,0.78,290,7000),
    PostFeatures(7,'TekrarHaber','small',700,'SON DAKİKA SON DAKİKA SON DAKİKA aynı metin tekrar tekrar',0.58,0.32,0.22,0.99,90,500),
]
b=rank_posts(posts,False); f=rank_posts(posts,True)
rank={'status':'ACTUAL_SYNTHETIC_PROTOTYPE','baseline_metrics':exposure_metrics(b),'fair_metrics':exposure_metrics(f),'baseline_order':[x['creator_name'] for x in b],'fair_order':[x['creator_name'] for x in f],'note':'Aynı sentetik aday kümesinde deterministik karşılaştırma.'}
(out/'ranking_metrics.json').write_text(json.dumps(rank,ensure_ascii=False,indent=2),encoding='utf-8')
scenarios={
'intentional':SessionFeatures(420,24,20,3,220,1,True),
'rapid':SessionFeatures(360,150,120,96,160,2,True),
'short_fast':SessionFeatures(50,35,30,24,55,0,True),
'disabled':SessionFeatures(400,200,180,150,90,2,False),
}
well={'status':'ACTUAL_CONTROLLED_SCENARIOS','scenarios':{k:evaluate(v) for k,v in scenarios.items()}}
(out/'wellbeing_metrics.json').write_text(json.dumps(well,ensure_ascii=False,indent=2),encoding='utf-8')
eng=ContextualDemoModerationEngine(); samples=['Mükemmel, yine uygulamayı çökerttin 👏','Fikir güzel ancak kaynaklar daha iyi açıklanmalı.','Oğlum bunu nasıl yaptın la 😂']
t=[]
for _ in range(60):
    for s in samples:
        a=time.perf_counter();eng.analyze(s);t.append((time.perf_counter()-a)*1000)
lat={'status':'ACTUAL_LOCAL_PROTOTYPE','moderation_ms_median':round(statistics.median(t),3),'moderation_ms_p95':round(sorted(t)[int(len(t)*.95)-1],3),'environment':'local container; not NSosyal production'}
(out/'latency_metrics.json').write_text(json.dumps(lat,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'moderation':mod,'ranking':rank,'wellbeing':well,'latency':lat},ensure_ascii=False,indent=2))
