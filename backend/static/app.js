(() => {
  'use strict';

  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => [...root.querySelectorAll(s)];
  const esc = (v='') => String(v).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const pct = v => `${Math.round(Number(v || 0) * 100)}%`;
  const api = async (path, options={}) => {
    const r = await fetch(path, {headers:{'Content-Type':'application/json'}, ...options});
    if (!r.ok) { let detail = `HTTP ${r.status}`; try { const j=await r.json(); detail=j.detail||detail; } catch{} throw new Error(detail); }
    return r.json();
  };

  const I = (name, cls='') => {
    const paths = {
      home:'<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10.5V20h5v-5h3v5h5v-9.5"/>',
      search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
      image:'<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9" r="1.5"/><path d="m21 15-5-5L5 20"/>',
      bell:'<path d="M18 8a6 6 0 0 0-12 0c0 7-3 6-3 8h18c0-2-3-1-3-8"/><path d="M10 20h4"/>',
      message:'<path d="M21 12a8 8 0 0 1-8 8H7l-4 2 1.5-4.5A8 8 0 1 1 21 12Z"/>',
      user:'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
      sliders:'<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
      flask:'<path d="M9 3h6M10 3v5l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7.5 15h9"/>',
      more:'<circle cx="5" cy="12" r="1" fill="currentColor"/><circle cx="12" cy="12" r="1" fill="currentColor"/><circle cx="19" cy="12" r="1" fill="currentColor"/>',
      reply:'<path d="M21 15a8 8 0 1 1-4-7"/><path d="M21 4v7h-7"/>',
      repeat:'<path d="m17 1 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 23-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
      heart:'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8Z"/>',
      chart:'<path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/>',
      bookmark:'<path d="M6 3h12v18l-6-4-6 4V3Z"/>',
      scale:'<path d="M12 3v18M5 7h14M5 7l-3 6h6L5 7Zm14 0-3 6h6l-3-6ZM8 21h8"/>',
      spark:'<path d="M12 3 10.5 8.5 5 10l5.5 1.5L12 17l1.5-5.5L19 10l-5.5-1.5L12 3Z"/><path d="m5 3 .7 2.3L8 6l-2.3.7L5 9l-.7-2.3L2 6l2.3-.7L5 3Z"/>',
      filter:'<path d="M4 6h16M7 12h10M10 18h4"/>',
      arrow:'<path d="m15 18-6-6 6-6"/>',
      calendar:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
      check:'<path d="m5 12 4 4L19 6"/>',
      shield:'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
      database:'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
      download:'<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
      info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
      camera:'<path d="M4 7h4l2-2h4l2 2h4v12H4V7Z"/><circle cx="12" cy="13" r="4"/>',
      poll:'<path d="M5 19V9M12 19V5M19 19v-7"/>',
      smile:'<circle cx="12" cy="12" r="9"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>',
      pin:'<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2"/>',
      close:'<path d="m6 6 12 12M18 6 6 18"/>'
    };
    return `<span class="nav-icon ${cls}"><svg viewBox="0 0 24 24" aria-hidden="true">${paths[name]||''}</svg></span>`;
  };

  const state = {
    page:'home', feedMode:'normal', moderation:null, ranking:null, wellbeing:null,
    metrics:{moderation:null, ranking:null, wellbeing:null}, activeProfileTab:'timeline', activeExploreTab:'trends',
    composer:'Mükemmel, yine uygulamayı çökerttin 👏', prefs:{context:true,fair:true,balance:true,explain:true}
  };

  const nav = [
    ['home','Ana Sayfa','home'],['explore','Keşfet','search'],['media','Medya','image'],['notifications','Bildirimler','bell'],['messages','Mesajlar','message'],['profile','Profil','user'],['preferences','Tercihler','sliders'],['research','Jüri / Araştırma','flask']
  ];

  const trends = [
    ['Türkiye gündemi','#TEKNOFEST2026','24,8 B gönderi'],['Bilim ve teknoloji','Yapay Zekâ','8.492 gönderi'],['İstanbul gündemi','Vapur','3.106 gönderi'],['Spor · Gündemde','Final Gecesi','17,1 B gönderi']
  ];

  const seedPosts = {
    1:{name:'TeknoMerak',handle:'teknomerak',initials:'TM',tone:'blue',verified:true,age:'18 dk',visual:'city',replies:28,reshares:74,likes:612,views:'18,4 B'},
    2:{name:'YeniFikir',handle:'yenifikir',initials:'YF',tone:'green',age:'26 dk',visual:'lab',replies:19,reshares:43,likes:389,views:'9,8 B'},
    3:{name:'KodDefteri',handle:'koddefteri',initials:'KD',tone:'amber',age:'34 dk',replies:12,reshares:29,likes:270,views:'7,2 B'},
    4:{name:'GündemHızlı',handle:'gundemhizli',initials:'GH',tone:'rose',verified:true,age:'40 dk',replies:87,reshares:110,likes:903,views:'25,1 B'},
    5:{name:'MinikAtölye',handle:'minikatolye',initials:'MA',tone:'green',age:'51 dk',visual:'eco',replies:9,reshares:32,likes:224,views:'5,4 B'},
    6:{name:'BilimNotu',handle:'bilimnotu',initials:'BN',tone:'blue',verified:true,age:'1 sa',replies:15,reshares:55,likes:430,views:'12,2 B'},
    7:{name:'TekrarHaber',handle:'tekrarhaber',initials:'TH',tone:'amber',age:'1 sa',replies:5,reshares:8,likes:31,views:'1,1 B'}
  };

  function renderNav(){
    $('#leftNav').innerHTML = nav.map(([id,label,icon]) => `<button class="nav-btn ${state.page===id?'active':''}" data-nav="${id}" type="button">${I(icon)}<span class="label">${label}</span></button>`).join('');
    $('#mobileNav').innerHTML = nav.slice(0,5).map(([id,label,icon]) => `<button class="${state.page===id?'active':''}" data-nav="${id}" aria-label="${label}">${I(icon)}</button>`).join('');
    $$('[data-nav]').forEach(b=>b.onclick=()=>go(b.dataset.nav));
  }

  function renderRightRail(){
    const rail=$('#rightRail');
    if (state.page==='media'){rail.classList.add('hidden');return;} rail.classList.remove('hidden');
    rail.innerHTML=`<div class="search-wrap">${I('search')}<input class="search" placeholder="NSosyal'de ara" aria-label="NSosyal'de ara"></div>
      <section class="trend-section"><div class="rail-heading"><h2>Gündemdekiler</h2><button data-nav="explore">Tümünü gör</button></div>
      ${trends.map(t=>`<div class="trend-item"><small>${esc(t[0])}</small><strong>${esc(t[1])}</strong><span>${esc(t[2])}</span></div>`).join('')}</section>
      <div class="quick-evidence"><strong>NSosyal Bağlam</strong><p>BAĞLAM · ADALET · DENGE aynı karar katmanında. Bu ekran bağımsız TEKNOFEST prototipidir.</p></div>
      <p class="disclaimer">Resmî NSosyal özelliği değildir. Arayüz, kamuya açık NSosyal ürün yapısından esinlenen entegrasyon prototipidir.</p>`;
    rail.querySelector('[data-nav]')?.addEventListener('click',()=>go('explore'));
  }

  function go(page){
    state.page=page; renderNav(); renderRightRail(); renderPage(); window.scrollTo({top:0,behavior:'instant'}); $('#mainColumn').focus({preventScroll:true});
  }

  function head(title, extra=''){
    return `<header class="page-head"><div class="page-head-row"><div class="page-title">${esc(title)}</div>${extra||'<span class="prototype-chip">BAĞIMSIZ PROTOTİP</span>'}</div></header>`;
  }

  function moderationCard(){
    const m=state.moderation;
    if(!m || !state.prefs.context) return '';
    const decision = m.decision==='allow'?'Yayınlanabilir':m.decision==='review'?'İnceleme öner': 'Bağlamı kontrol et';
    return `<div class="context-assistant" id="contextAssistant">
      <div class="context-top"><div class="context-icon">⚠</div><div class="context-copy">
        <div class="context-label">BAĞLAM <span>Yayınlamadan önce</span></div>
        <div class="context-message">${esc(m.explanation)} ${m.style_label==='sarcasm_irony'?'Anlatım biçimi ironi/sarkazm sinyali taşıyor.':''}</div>
      </div><button class="icon-btn" id="dismissContext" aria-label="Öneriyi kapat">✕</button></div>
      <dl class="metric-mini"><div><dt>Karar</dt><dd>${decision}</dd></div><div><dt>Güven</dt><dd>${pct(m.confidence)}</dd></div><div><dt>Zarar riski</dt><dd>${pct(m.harm_score)}</dd></div><div><dt>İroni / sarkazm</dt><dd>${pct(m.sarcasm_score)}</dd></div></dl>
      <div class="context-actions"><button class="primary" id="rewriteBtn">Düzenle</button><button class="ghost" id="publishAnyway">Yine de Yayınla</button><button class="ghost" id="appealBtn">İtiraz et</button><span class="inline-status">${esc(m.model_version)} · ${m.latency_ms} ms</span></div>
    </div>`;
  }

  function feedPost(item){
    const s=seedPosts[item.id]||seedPosts[3]; const discover = state.feedMode==='fair' && Number(item.fairness_adjustment)>0.04 && Number(item.quality)>=.7;
    return `<article class="post" data-post="${item.id}">
      ${discover?`<div class="discovery-tag">${I('scale')} Keşif fırsatı · görece az görünür ama kaliteli içerik</div>`:''}
      <div class="post-row"><div class="avatar avatar-${s.tone}">${s.initials}</div><div class="post-main">
        <div class="post-head"><div class="identity"><strong>${esc(s.name)}</strong>${s.verified?'<span class="verified">✓</span>':''}<span class="handle">@${esc(s.handle)} · ${esc(s.age)}</span></div><button class="icon-btn" aria-label="Gönderi seçenekleri">${I('more')}</button></div>
        <p class="post-text">${esc(item.text)}</p>
        ${s.visual?`<div class="post-visual ${s.visual}" role="img" aria-label="Gönderi için sentetik prototip medya alanı"></div>`:''}
        ${state.feedMode==='fair'?`<button class="reason-link" data-reason="${item.id}">Neden görüyorum?</button>`:''}
        <div class="post-actions"><button class="action-btn">${I('message')} ${s.replies}</button><button class="action-btn">${I('repeat')} ${s.reshares}</button><button class="action-btn like-btn">${I('heart')} ${s.likes}</button><span class="action-btn">${I('chart')} ${s.views}</span><button class="action-btn">${I('bookmark')}</button></div>
      </div></div>
    </article>`;
  }

  function balanceCard(){
    const w=state.wellbeing;if(!w || !w.nudge || !state.prefs.balance) return '';
    return `<aside class="balance-card" id="balanceCard"><div class="balance-row"><div class="balance-icon">${I('spark')}</div><div class="balance-copy"><strong>DENGE · Kısa bir ara iyi gelebilir</strong><p>${esc(w.reason)} Bu bir davranış örüntüsü desteğidir; tanı değildir.</p><button class="link-btn" id="break5">5 dakikalık hatırlatıcı kur</button></div><button class="icon-btn" id="dismissBalance">✕</button></div></aside>`;
  }

  function renderHome(){
    const items = state.ranking?.items || [];
    const html = `${head('Ana Sayfa')}<div class="top-tabs"><button class="active">Sana özel</button><button>Takip edilenler</button></div>
      <section class="composer"><div class="composer-row"><div class="avatar avatar-amber">DA</div><div class="composer-main"><textarea id="composerText" maxlength="1000" aria-label="Gönderi metni">${esc(state.composer)}</textarea><div class="composer-tools"><div class="tool-icons"><button class="tool-btn" aria-label="Görsel ekle">${I('camera')}</button><button class="tool-btn" aria-label="Anket ekle">${I('poll')}</button><button class="tool-btn" aria-label="Emoji ekle">${I('smile')}</button><button class="tool-btn" aria-label="Konum ekle">${I('pin')}</button></div><span class="char-count" id="charCount">${state.composer.length}/1000</span><button class="primary" id="publishBtn">Yayınla</button></div></div></div>${moderationCard()}</section>
      <div class="feed-mode"><div class="feed-mode-label">${I('filter')} Akış modu</div><div class="segmented"><button class="${state.feedMode==='normal'?'active':''}" data-mode="normal">Normal</button><button class="${state.feedMode==='fair'?'active fair':''}" data-mode="fair">Adil Görünürlük</button></div></div>
      ${items[0]?feedPost(items[0]):''}${balanceCard()}${items.slice(1,6).map(feedPost).join('')}`;
    $('#mainColumn').innerHTML=html;
    bindHome();
  }

  function bindHome(){
    const ta=$('#composerText');
    if(ta){ ta.addEventListener('input',e=>{state.composer=e.target.value;$('#charCount').textContent=`${state.composer.length}/1000`; debounceAnalyze();}); }
    $$('[data-mode]').forEach(b=>b.onclick=async()=>{state.feedMode=b.dataset.mode; await loadRanking(); renderHome();});
    $$('.like-btn').forEach(b=>b.onclick=()=>b.classList.toggle('liked'));
    $$('[data-reason]').forEach(b=>b.onclick=()=>openReason(Number(b.dataset.reason)));
    $('#dismissContext')?.addEventListener('click',()=>{$('#contextAssistant')?.remove();});
    $('#rewriteBtn')?.addEventListener('click',()=>{state.composer='Bu yaklaşımın neden sonuç vermediğini birlikte tartışalım.'; analyzeComposer(true);});
    $('#publishAnyway')?.addEventListener('click',()=>toast('Gönderi prototip akışında yayınlandı.'));
    $('#publishBtn')?.addEventListener('click',()=>toast(state.moderation?.decision==='review'?'Gönderi önce inceleme akışına yönlendirildi.':'Gönderi prototip akışında yayınlandı.'));
    $('#appealBtn')?.addEventListener('click',openAppeal);
    $('#dismissBalance')?.addEventListener('click',()=>$('#balanceCard')?.remove());
    $('#break5')?.addEventListener('click',()=>{api('/api/wellbeing/nudge-response?response=break_5',{method:'POST'}).then(()=>toast('5 dakikalık demo hatırlatıcı kaydedildi.'));});
  }

  let analyzeTimer;
  function debounceAnalyze(){clearTimeout(analyzeTimer);analyzeTimer=setTimeout(()=>analyzeComposer(),350)}
  async function analyzeComposer(rerender=false){
    if(!state.composer.trim()){state.moderation=null;if(rerender)renderHome();return;}
    try{state.moderation=await api('/api/moderation/analyze',{method:'POST',body:JSON.stringify({text:state.composer})}); if(rerender||state.page==='home')renderHome();}
    catch(e){toast(e.message)}
  }

  async function loadRanking(){
    try{state.ranking=await api('/api/ranking/rank',{method:'POST',body:JSON.stringify({fair:state.feedMode==='fair'})});}
    catch(e){toast(`Sıralama yüklenemedi: ${e.message}`)}
  }

  async function loadWellbeing(){
    try{state.wellbeing=await api('/api/wellbeing/event',{method:'POST',body:JSON.stringify({session_duration_sec:360,posts_scrolled:150,viewed_posts:120,rapid_skips:96,total_dwell_sec:160,reentry_count:2,enabled:true})});}
    catch(e){console.warn(e)}
  }

  async function openReason(id){
    try{const data=await api(`/api/ranking/explanation/${id}`);$('#reasonBody').innerHTML=`<ul class="reason-list">${(data.reasons||[]).map(r=>`<li>${esc(r)}</li>`).join('')||'<li>Bu gönderi için belirgin bir ek adalet sinyali yok.</li>'}</ul><div class="reason-delta">Adalet düzeltmesi: <strong>${Number(data.fairness_adjustment).toFixed(4)}</strong>. Bu değer tek başına takipçi sayısına göre verilmez; kalite ve ilgililik kapılarıyla birlikte kullanılır.</div>`;$('#reasonDialog').showModal();}
    catch(e){toast(e.message)}
  }

  function openAppeal(){const m=state.moderation;$('#appealDecision').textContent=`Karar: ${m?.decision||'warn'}`;$('#appealConfidence').textContent=`Güven: ${m?pct(m.confidence):'—'}`;$('#appealBody').innerHTML=`<div class="decision-summary"><strong>Karar: ${esc(m?.decision||'warn')}</strong><span>Güven: ${m?pct(m.confidence):'—'}</span></div><label class="field-label">Neden yeniden incelenmeli?<textarea id="appealReason" minlength="3" maxlength="500" required>İfadenin bağlamının ve anlatım biçiminin birlikte yeniden değerlendirilmesini rica ediyorum.</textarea></label>`;$('#sendAppeal').classList.remove('hidden');$('#appealDialog').showModal();}

  function renderExplore(){
    $('#mainColumn').innerHTML=`<div class="explore-head"><div class="search-wrap">${I('search')}<input id="exploreSearch" class="search" placeholder="Arama yap" aria-label="Arama yap"></div></div>
      <div class="tabs-3">${[['trends','Trendler'],['tags','Etiketler'],['news','Haberler']].map(t=>`<button data-etab="${t[0]}" class="${state.activeExploreTab===t[0]?'active':''}">${t[1]}</button>`).join('')}</div><div id="exploreContent"></div>`;
    renderExploreContent();
    $$('[data-etab]').forEach(b=>b.onclick=()=>{state.activeExploreTab=b.dataset.etab;renderExplore()});
  }
  function renderExploreContent(){const c=$('#exploreContent');if(!c)return;
    if(state.activeExploreTab==='trends')c.innerHTML=`<div class="section-intro"><h1>Gündemde</h1><p>Öne çıkan başlıklar</p></div>${trends.map((t,i)=>`<div class="explore-trend"><div class="trend-no">${i+1}</div><div class="trend-body"><small>${esc(t[0])}</small><strong>${esc(t[1])}</strong><span>${esc(t[2])}</span></div></div>`).join('')}`;
    else if(state.activeExploreTab==='tags')c.innerHTML=`<div class="section-intro"><h1>Etiketler</h1><p>İlgi alanlarına göre keşfet</p></div>${['#MilliTeknolojiHamlesi','#YapayZekâ','#Sürdürülebilirlik','#GençGirişim'].map((x,i)=>`<div class="explore-trend"><div class="trend-no">#</div><div class="trend-body"><strong>${x}</strong><span>${[12600,8492,4300,2180][i].toLocaleString('tr-TR')} gönderi</span></div></div>`).join('')}`;
    else c.innerHTML=`<div class="section-intro"><h1>Haberler</h1><p>Kamusal gündemden örnek prototip içerikler</p></div>${(state.ranking?.items||[]).slice(0,4).map(feedPost).join('')}`;
  }

  function renderProfile(){
    const first=state.ranking?.items?.[0];
    $('#mainColumn').innerHTML=`${head('Selin Arı',`<span style="font-size:10px;color:var(--muted)">284 gönderi</span>`)}<div class="profile-cover"></div><section class="profile-body"><div class="profile-top"><div class="profile-avatar-wrap"><div class="avatar large avatar-blue">SA</div></div><div class="profile-actions"><button class="secondary">•••</button><button class="primary" id="followBtn">Takip et</button></div></div><div class="profile-name">Selin Arı <span class="verified">✓</span></div><div class="profile-handle">@selinari</div><p class="profile-bio">Şehir, kültür ve teknoloji üzerine notlar. Projeler, üretim ve gündelik hayat.</p><div class="profile-meta">${I('calendar')} Ağustos 2025'te katıldı · Türkiye</div><div class="profile-stats"><div><strong>312</strong> <span>Takip Edilen</span></div><div><strong>18,7 B</strong> <span>Takipçi</span></div><div><strong>284</strong> <span>Gönderi</span></div></div></section><div class="tabs-3">${[['timeline','Zaman Çizelgesi'],['media','Medya'],['replies','Yanıtlar']].map(t=>`<button data-ptab="${t[0]}" class="${state.activeProfileTab===t[0]?'active':''}">${t[1]}</button>`).join('')}</div><div id="profileContent"></div>`;
    renderProfileContent(first); $$('[data-ptab]').forEach(b=>b.onclick=()=>{state.activeProfileTab=b.dataset.ptab;renderProfile()});
    $('#followBtn').onclick=e=>{e.target.textContent=e.target.textContent==='Takip et'?'Takip ediliyor':'Takip et';e.target.classList.toggle('secondary')};
  }
  function renderProfileContent(first){const c=$('#profileContent');if(!c)return;if(state.activeProfileTab==='timeline')c.innerHTML=`<article class="post"><div class="post-row"><div class="avatar avatar-blue">SA</div><div class="post-main"><div class="post-head"><div class="identity"><strong>Selin Arı</strong><span class="verified">✓</span><span class="handle">@selinari · 18 dk</span></div><button class="icon-btn" aria-label="Gönderi seçenekleri">${I('more')}</button></div><p class="post-text">Türkçe yapay zekâ sistemlerinde yalnızca kelimeleri değil, bağlamı ve anlatım biçimini de birlikte değerlendirmek gerekiyor.</p><div class="post-visual city" role="img" aria-label="Selin Arı için sentetik prototip medya alanı"></div><div class="post-actions"><button class="action-btn">${I('message')} 28</button><button class="action-btn">${I('repeat')} 74</button><button class="action-btn like-btn">${I('heart')} 612</button><span class="action-btn">${I('chart')} 18,4 B</span><button class="action-btn">${I('bookmark')}</button></div></div></div></article>`;else if(state.activeProfileTab==='media')c.innerHTML='<div class="data-grid"><div class="post-visual city"></div><div class="post-visual lab"></div><div class="post-visual eco"></div><div class="post-visual city"></div></div>';else c.innerHTML=`<article class="post"><div class="post-row"><div class="avatar avatar-blue">SA</div><div class="post-main"><div class="identity"><strong>Selin Arı</strong><span class="verified">✓</span><span class="handle">@selinari · 2 sa</span></div><p class="post-text">@emreyalcin Kaynak listesini gördüm; özellikle Türkçe veri setleri bölümü çok faydalı olmuş.</p></div></div></article>`}

  function renderPreferences(){
    const settings=[['context','BAĞLAM yazım desteği','Yayınlamadan önce olası zarar, belirsizlik ve anlatım biçimi sinyallerini gösterir.'],['fair','Adil Görünürlük modu','Kaliteli ve ilgili içeriklerde önceki görünürlük bağımlılığını azaltan deneysel sıralama.'],['balance','DENGE mola önerileri','Kaydırma hızı, hızlı geçiş ve oturum süresi birlikte belirginleştiğinde isteğe bağlı hatırlatma.'],['explain','Neden görüyorum? açıklamaları','Adil sıralama sinyallerini kullanıcıya okunabilir biçimde açıklar.']];
    $('#mainColumn').innerHTML=`${head('Bağlam ve Veri Tercihleri')}<div class="settings-intro">Bu sayfa NSosyal Bağlam prototipinin hangi sinyalleri işlediğini ve hangi verileri bilerek toplamadığını gösterir. Tercihler yalnızca demo oturumunda etkilidir.</div><div class="section-label">Modül kontrolleri</div>${settings.map(s=>`<div class="setting-row"><div><div class="setting-title">${esc(s[1])}</div><div class="setting-desc">${esc(s[2])}</div></div><button class="switch ${state.prefs[s[0]]?'on':''}" data-pref="${s[0]}" aria-label="${esc(s[1])}"></button></div>`).join('')}<div class="section-label">Veri minimizasyonu</div><div class="data-grid"><div class="data-box"><h3>İşlenen prototip verileri</h3><ul><li>Gönderi metni</li><li>Sentetik gönderi kalite/ilgililik sinyalleri</li><li>Oturum özeti: süre, kaydırma, hızlı geçiş, görüntüleme süresi</li><li>İtiraz gerekçesi</li></ul></div><div class="data-box"><h3>Toplanmayan veriler</h3><ul><li>GPS / kesin konum</li><li>Mikrofon veya kamera</li><li>Kişiler / rehber</li><li>Özel mesaj içeriği</li><li>Diğer uygulamalardaki davranış</li></ul></div></div>`;
    $$('[data-pref]').forEach(b=>b.onclick=()=>{const k=b.dataset.pref;state.prefs[k]=!state.prefs[k];b.classList.toggle('on',state.prefs[k]);toast(`${b.previousElementSibling.querySelector('.setting-title').textContent}: ${state.prefs[k]?'açık':'kapalı'}`)});
  }

  function renderResearch(){
    const m=state.metrics.moderation||{}, r=state.metrics.ranking||{}, w=state.metrics.wellbeing||{};
    const base=r.baseline||{}, fair=r.fair||{}; const rapid=w.scenarios?.rapid||{};
    $('#mainColumn').innerHTML=`<section class="research-head"><div class="research-kicker">${I('flask')} PROTOTİP / DEMO</div><h1>Jüri ve Araştırma Kanıtları</h1><p>Bu ekrandaki değerler gerçek kullanıcı saha sonucu değildir. Moderasyon küçük sentetik veri kümesi; sıralama sentetik üretici/gönderi verisi; DENGE ise kontrollü senaryolar ile ölçülmüştür.</p></section><section class="metric-strip"><div class="metric-card"><strong>${m.macro_f1!==undefined?Number(m.macro_f1).toFixed(3):'—'}</strong><span>BAĞLAM Macro F1</span><small>${m.test_size||'—'} sentetik test örneği</small></div><div class="metric-card"><strong>${base.small_creator_top5_share!==undefined?`${pct(base.small_creator_top5_share||0)} → ${pct(fair.small_creator_top5_share||0)}`:'—'}</strong><span>Küçük üretici Top-5 payı</span><small>${base.small_creator_top5_share!==undefined?`+${Math.round((fair.small_creator_top5_share-base.small_creator_top5_share)*100)} yüzde puan`:'—'}</small></div><div class="metric-card"><strong>${rapid.scroll_velocity??'—'}</strong><span>DENGE kaydırma/dk</span><small>Kontrollü hızlı senaryo</small></div></section><div class="table-wrap"><div style="display:flex;align-items:center;gap:8px;margin-bottom:10px"><strong>Teknik kanıt özeti</strong><span class="pill purple">SENTETİK / KONTROLLÜ</span></div><table class="research-table"><thead><tr><th>Modül</th><th>Kanıt</th><th>Sonuç</th><th>Durum</th></tr></thead><tbody><tr><td>BAĞLAM</td><td>Macro precision / recall</td><td>${fmt(m.macro_precision)} / ${fmt(m.macro_recall)}</td><td><span class="pill blue">Ölçüldü</span></td></tr><tr><td>ADALET</td><td>Top-5 ort. ilgililik</td><td>${fmt(base.mean_relevance_top5)} → ${fmt(fair.mean_relevance_top5)}</td><td><span class="pill blue">Ölçüldü</span></td></tr><tr><td>ADALET</td><td>Küçük üretici payı</td><td>${pct(base.small_creator_top5_share||0)} → ${pct(fair.small_creator_top5_share||0)}</td><td><span class="pill blue">Ölçüldü</span></td></tr><tr><td>DENGE</td><td>Hızlı senaryo</td><td>${rapid.nudge?'Mola önerisi gösterildi':'Öneri yok'}</td><td><span class="pill blue">Kontrollü</span></td></tr><tr><td>Şeffaflık</td><td>İtiraz + açıklama</td><td>Çalışan prototip akışı</td><td><span class="pill blue">Çalışıyor</span></td></tr></tbody></table></div><div class="research-note">${I('info')} Model şu anda BERTurk değildir. Yerel, ölçülebilir prototip motoru TF-IDF kelime + karakter n-gram özellikleri ve Logistic Regression kullanır. Gerçek NSosyal API entegrasyonu ve gerçek kullanıcı saha testi yapılmış gibi sunulmaz.</div>`;
  }
  const fmt=v=>v===undefined?'—':Number(v).toFixed(3);

  function renderMedia(){
    const items=state.ranking?.items||[];
    $('#mainColumn').innerHTML=`<div style="min-height:100vh;background:#171c23;color:white"><div style="height:55px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:0 15px;border-bottom:1px solid #323944"><span>☰</span><strong>NSosyal</strong><span style="text-align:right">◯</span></div><div style="display:flex;gap:15px;padding:12px 14px;border-bottom:1px solid #323944;overflow:hidden">${Object.values(seedPosts).slice(0,6).map(s=>`<div style="text-align:center;min-width:52px"><div class="avatar small avatar-${s.tone}" style="margin:auto;border:2px solid var(--blue)">${s.initials}</div><span style="font-size:9px;color:#bcc5ce">@${s.handle}</span></div>`).join('')}</div><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:2px;padding:2px">${items.slice(0,6).map((p,i)=>`<div class="post-visual ${seedPosts[p.id]?.visual||['city','lab','eco'][i%3]}" style="height:${i%3===0?280:210}px;margin:0;border:0;border-radius:0"><div style="position:absolute;left:10px;right:10px;bottom:8px;color:white;font-size:10px;z-index:3;text-shadow:0 1px 3px #000"><strong>@${seedPosts[p.id]?.handle||'kullanici'}</strong><br>${esc(p.text).slice(0,75)}…</div></div>`).join('')}</div></div>`;
  }

  function renderSimple(kind){
    const data = kind==='notifications' ? [['Selin Arı gönderini beğendi.','12 dk'],['Emre Yalçın gönderini yeniden paylaştı.','38 dk'],['#TEKNOFEST2026 etiketinde yeni paylaşımlar var.','1 sa']] : [['Selin Arı','Proje notlarını gördüm, akşam detayları konuşalım.'],['Emre Yalçın','Sıralama karşılaştırmasını gönderdim.'],['İklim Günlüğü','Kaynak listesine yeni bir rapor ekledim.']];
    $('#mainColumn').innerHTML=`${head(kind==='notifications'?'Bildirimler':'Mesajlar')}${kind==='messages'?`<div class="explore-head"><div class="search-wrap">${I('search')}<input class="search" placeholder="Mesajlarda ara"></div></div>`:''}${data.map((x,i)=>`<div class="setting-row" style="grid-template-columns:auto 1fr"><div class="avatar small avatar-${['blue','green','rose'][i]}">${['SA','EY','İG'][i]}</div><div><div class="setting-title">${esc(x[0])}</div><div class="setting-desc">${esc(x[1])}</div></div></div>`).join('')}`;
  }

  function renderPage(){
    const map={home:renderHome,explore:renderExplore,profile:renderProfile,preferences:renderPreferences,research:renderResearch,media:renderMedia,notifications:()=>renderSimple('notifications'),messages:()=>renderSimple('messages')};
    (map[state.page]||renderHome)();
  }

  function toast(message){let t=$('.toast');if(!t){t=document.createElement('div');t.className='toast';document.body.appendChild(t)}t.textContent=message;t.classList.add('show');clearTimeout(t._timer);t._timer=setTimeout(()=>t.classList.remove('show'),2200)}

  async function loadMetrics(){
    try{const [m,r,w]=await Promise.all([api('/api/metrics/moderation'),api('/api/metrics/ranking'),api('/api/metrics/wellbeing')]);state.metrics={moderation:m,ranking:r,wellbeing:w};if(state.page==='research')renderResearch();}catch(e){console.warn('metrics',e)}
  }

  function bindDialogs(){
    $('#cancelAppeal').onclick=()=>$('#appealDialog').close();
    $('#appealForm').addEventListener('submit',async e=>{e.preventDefault();const reason=$('#appealReason')?.value||'';try{const data=await api('/api/moderation/appeal',{method:'POST',body:JSON.stringify({moderation_result_id:'DEMO-MOD-001',reason})});$('#appealBody').innerHTML=`<div class="success-box"><div class="success-mark">✓</div><strong>İtiraz simüle kuyruğa alındı</strong><p style="font-size:11px;color:var(--muted)">Takip kodu: ${esc(data.id)} · durum: ${esc(data.status)}</p></div>`;$('#sendAppeal').classList.add('hidden');setTimeout(()=>{},0);}catch(err){toast(err.message)}});
    $('#closeReason').onclick=()=>$('#reasonDialog').close();
  }

  async function init(){
    renderNav(); renderRightRail(); bindDialogs();
    await Promise.all([loadRanking(),loadWellbeing()]);
    await analyzeComposer(false);
    renderPage(); loadMetrics();
    $('#composePrimary').onclick=()=>{go('home');setTimeout(()=>$('#composerText')?.focus(),50)};
  }

  init();
})();
