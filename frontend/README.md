# Frontend kaynak konumu

Bu sürümde ayrı bir Node/Next.js geliştirme sunucusu kullanılmaz.

Gerçek prototip arayüzü **tek origin** üzerinden FastAPI tarafından servis edilir:

- `backend/static/index.html`
- `backend/static/styles.css`
- `backend/static/app.js`

Bunun amacı jüri demosunu sadeleştirmek ve Windows kurulumunda npm/port/PowerShell sorunlarını kaldırmaktır.
