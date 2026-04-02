# auto-pilot

هذا هو مستودع Codex المحلي للإضافة `Auto Pilot`.

## اللغات

- English: [`README.md`](/Users/minsu/Documents/Codex/README.md)
- 한국어: [`README.ko.md`](/Users/minsu/Documents/Codex/README.ko.md)
- 日本語: [`README.ja.md`](/Users/minsu/Documents/Codex/README.ja.md)
- 中文: [`README.zh.md`](/Users/minsu/Documents/Codex/README.zh.md)
- العربية: `README.ar.md`

## المحتويات

- [جذر إضافة Auto Pilot](/Users/minsu/Documents/Codex/auto-pilot)
- [إعداد marketplace المحلي للمستودع](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- سكربتات لإدارة intake وإنشاء الحالة والاستئناف

## الميزات الأساسية

- تحويل الطلب القصير للمشروع إلى جلسة intake
- عرض سؤال واحد فقط في كل مرة
- استخدام نمط `1. Question` / `Questions remaining: N`
- إنشاء `docs/spec.md` و `docs/progress.md` و `docs/next.md` و `autopilot/state.json` و `autopilot/blockers.json` تلقائياً بعد الإجابة الأخيرة
- الاحتفاظ بحالة قابلة للاستئناف في جلسات Codex اللاحقة
