from __future__ import annotations
from pathlib import Path
from time import perf_counter
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.services.moderation import ContextualDemoModerationEngine, evaluate_demo_model
from app.services.ranking import PostFeatures, rank_posts, exposure_metrics
from app.services.wellbeing import SessionFeatures, evaluate

app = FastAPI(title='NSosyal Bağlam API', version='0.2.0', description='NSosyal integration prototype API — not an official NSosyal service. Python 3.14 target build.')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8000', 'http://127.0.0.1:8000',
        'http://localhost:3000', 'http://127.0.0.1:3000',
        'http://localhost:3001', 'http://127.0.0.1:3001',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

moderation_engine = ContextualDemoModerationEngine()
ROOT = Path(__file__).resolve().parents[2]
METRICS_PATH = ROOT / 'evaluation' / 'results' / 'moderation_metrics.json'
moderation_metrics = evaluate_demo_model(METRICS_PATH)

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)

class RankRequest(BaseModel):
    fair: bool = True

class WellbeingRequest(BaseModel):
    session_duration_sec: float = Field(ge=0, le=86400)
    posts_scrolled: int = Field(ge=0, le=100000)
    viewed_posts: int = Field(ge=0, le=100000)
    rapid_skips: int = Field(ge=0, le=100000)
    total_dwell_sec: float = Field(ge=0, le=86400)
    reentry_count: int = Field(default=0, ge=0, le=1000)
    enabled: bool = True

class AppealRequest(BaseModel):
    moderation_result_id: str
    reason: str = Field(min_length=3, max_length=500)

POSTS = [
    PostFeatures(1,'TeknoMerak','large',120000,'Yerli yapay zekâ üzerine kısa bir kaynak listesi hazırladım.',0.91,0.87,0.82,0.89,980,16000),
    PostFeatures(2,'YeniFikir','small',420,'Türkçede ironi ve bağlamı anlamak için neden yalnızca kelime filtresi yetmiyor?',0.89,0.92,0.96,0.94,68,420),
    PostFeatures(3,'KodDefteri','medium',8500,'Bugün FastAPI ile küçük bir öneri sistemi deneyi yaptım.',0.82,0.84,0.91,0.92,160,4100),
    PostFeatures(4,'GündemHızlı','large',280000,'Herkes bunu konuşuyor! Detaylar burada.',0.67,0.49,0.40,0.97,1450,19500),
    PostFeatures(5,'MinikAtölye','small',180,'Yeni üreticilerin keşfedilmesi için pozisyon bazlı görünürlük ölçümü denedim.',0.86,0.90,0.95,0.88,42,260),
    PostFeatures(6,'BilimNotu','medium',21000,'Öneri sistemlerinde relevance ile exposure fairness arasındaki dengeyi nasıl ölçebiliriz?',0.94,0.93,0.94,0.78,290,7000),
    PostFeatures(7,'TekrarHaber','small',700,'SON DAKİKA SON DAKİKA SON DAKİKA aynı metin tekrar tekrar',0.58,0.32,0.22,0.99,90,500),
]

appeals = {}

@app.get('/api/health')
def health():
    return {
        'status':'ok',
        'project':'NSosyal Bağlam',
        'prototype':True,
        'app_version':'0.2.0',
        'python_target':'3.14',
        'ui':'single-origin-static',
        'moderation_engine':moderation_engine.version,
        'official_nsosyal_integration':False,
    }

@app.get('/api/feed')
def feed():
    return rank_posts(POSTS, fair=True)

@app.post('/api/moderation/analyze')
def moderation_analyze(req: AnalyzeRequest):
    try:
        return moderation_engine.analyze(req.text).__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/api/moderation/appeal')
def moderation_appeal(req: AppealRequest):
    appeal_id = f'APL-{len(appeals)+1:04d}'
    appeals[appeal_id] = {'id':appeal_id,'moderation_result_id':req.moderation_result_id,'reason':req.reason,'status':'pending_review','review_type':'simulated_prototype_queue'}
    return appeals[appeal_id]

@app.get('/api/moderation/appeals/{appeal_id}')
def get_appeal(appeal_id: str):
    if appeal_id not in appeals:
        raise HTTPException(status_code=404, detail='İtiraz kaydı bulunamadı.')
    return appeals[appeal_id]

@app.post('/api/ranking/rank')
def ranking(req: RankRequest):
    start = perf_counter()
    rows = rank_posts(POSTS, fair=req.fair)
    return {'method':'fair' if req.fair else 'baseline','items':rows,'metrics':exposure_metrics(rows),'latency_ms':round((perf_counter()-start)*1000,2),'ranking_version':'fair-reranker-1.0' if req.fair else 'baseline-1.0'}

@app.post('/api/ranking/compare')
def ranking_compare():
    start = perf_counter()
    baseline = rank_posts(POSTS, fair=False)
    fair = rank_posts(POSTS, fair=True)
    return {
        'baseline':baseline,'fair':fair,
        'baseline_metrics':exposure_metrics(baseline),
        'fair_metrics':exposure_metrics(fair),
        'latency_ms':round((perf_counter()-start)*1000,2),
        'note':'Sentetik üretici/gönderi verisi üzerinde prototip karşılaştırmasıdır.'
    }

@app.get('/api/ranking/explanation/{post_id}')
def ranking_explanation(post_id: int):
    rows = rank_posts(POSTS, fair=True)
    row = next((r for r in rows if r['id']==post_id), None)
    if not row:
        raise HTTPException(status_code=404, detail='Gönderi bulunamadı.')
    reasons=[]
    if row['relevance']>=.85: reasons.append('İlgi alanlarıyla yüksek uyum')
    if row['originality']>=.9: reasons.append('Özgünlük sinyali güçlü')
    if row['under_exposure']>=.5 and row['quality']>=.7: reasons.append('Kaliteli fakat görece az görünür üretici')
    return {'post_id':post_id,'reasons':reasons,'fairness_adjustment':row['fairness_adjustment'],'final_score':row['final_score']}

@app.post('/api/wellbeing/event')
def wellbeing_event(req: WellbeingRequest):
    start=perf_counter()
    out=evaluate(SessionFeatures(**req.model_dump()))
    out['latency_ms']=round((perf_counter()-start)*1000,2)
    return out

@app.get('/api/wellbeing/session')
def wellbeing_session():
    return evaluate(SessionFeatures(210,78,72,50,128,1,True))

@app.post('/api/wellbeing/nudge-response')
def wellbeing_response(response: Literal['break_5','continue','hide_today']):
    return {'accepted':True,'response':response,'stored':'aggregate_demo_only'}

@app.get('/api/metrics/moderation')
def metrics_moderation():
    return moderation_metrics

@app.get('/api/metrics/ranking')
def metrics_ranking():
    baseline=rank_posts(POSTS, fair=False); fair=rank_posts(POSTS, fair=True)
    return {'status':'ACTUAL_SYNTHETIC_PROTOTYPE','baseline':exposure_metrics(baseline),'fair':exposure_metrics(fair)}

@app.get('/api/metrics/wellbeing')
def metrics_wellbeing():
    scenarios={
        'intentional':SessionFeatures(420,24,20,3,220,1,True),
        'rapid':SessionFeatures(360,150,120,96,160,2,True),
        'short_fast':SessionFeatures(50,35,30,24,55,0,True),
    }
    return {'status':'ACTUAL_CONTROLLED_SCENARIOS','scenarios':{k:evaluate(v) for k,v in scenarios.items()}}

@app.post('/api/demo/reset')
def demo_reset():
    appeals.clear()
    return {'status':'reset','message':'Demo verileri başlangıç durumuna döndürüldü.'}

STATIC_DIR = Path(__file__).resolve().parents[1] / 'static'
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
@app.get('/')
def root_ui():
    return FileResponse(STATIC_DIR / 'index.html')
