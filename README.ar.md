# Auto Pilot

الوثائق الرسمية وملفات الإضافة الأساسية موجودة الآن في جذر المستودع.

- الوثائق الكاملة: [README.md](./README.md)
- 한국어: [README.ko.md](./README.ko.md)
- 日本語: [README.ja.md](./README.ja.md)
- 中文: [docs/i18n/zh.md](./docs/i18n/zh.md)
- العربية: [docs/i18n/ar.md](./docs/i18n/ar.md)

## التثبيت بسطر واحد

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

للتثبيت المستقر استخدم `v0.1.1`. يجب أن يثبّت stable release tag نفس ذلك الإصدار، واستخدم `develop` فقط إذا أردت تجربة التغييرات القادمة قبل إصدار stable التالي.

## التشغيل داخل Codex

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

نقطة الدخول العامة الأساسية هي `$auto-pilot`. بعد التثبيت أعد تشغيل Codex مرة واحدة حتى يتم تحميل الـ skill بشكل صحيح.

بعد التثبيت مرة واحدة، يبدأ intake تلقائيًا للمشاريع الجديدة ويستأنف المشاريع الحالية تلقائيًا. وبعد إعادة التشغيل يمكنك أيضًا استخدام الاختصار الطبيعي:

```text
Build a diary app my friend Dohyeon would love ap
```
