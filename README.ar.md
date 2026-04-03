# Auto Pilot

الوثائق الرسمية وملفات الإضافة الأساسية موجودة الآن في جذر المستودع.

- الوثائق الكاملة: [README.md](./README.md)
- دليل الاستخدام التفصيلي: [docs/06-usage-guide.md](./docs/06-usage-guide.md)
- 한국어: [README.ko.md](./README.ko.md)
- 日本語: [README.ja.md](./README.ja.md)
- 中文: [docs/i18n/zh.md](./docs/i18n/zh.md)
- العربية: [docs/i18n/ar.md](./docs/i18n/ar.md)

## التثبيت بسطر واحد

الإصدار stable الحالي `v0.1.1` يتطلب `curl` و`tar` و`python3`، ويُبقي نقطة الدخول المنشورة عبر slash command.

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

إذا أردت تجربة خط الإصدار التالي قبل نشره، فثبّت `develop` بشكل صريح:

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/develop/install.sh | env -u NO_COLOR bash
```

الإصدار المنشور حاليًا هو `v0.1.1`. استخدم `develop` فقط عندما تريد اختبار سلوك غير منشور. وعند إصدار stable tag التالي يجب تحديث stable install URL وأمثلة التشغيل وbaked-in stable ref معًا.

## التشغيل داخل Codex

### Stable `v0.1.1`

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

نقطة الدخول العامة الأساسية في stable هي `/auto-pilot:autopilot`. بعد التثبيت أعد تشغيل Codex مرة واحدة حتى يتم تحميل slash command بشكل صحيح.

بعد التثبيت مرة واحدة، يبدأ intake تلقائيًا للمشاريع الجديدة ويستأنف المشاريع الحالية تلقائيًا. وبعد إعادة التشغيل يمكنك أيضًا استخدام الاختصار الطبيعي:

```text
Build a budgeting app for freelancers ap
```

### Preview on `develop`

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

استخدم `$auto-pilot` فقط إذا كنت قد ثبّت الإصدار من `develop`. وبعد إعادة التشغيل يمكنك أيضًا استخدام الاختصار الطبيعي:

```text
Build a diary app my friend Dohyeon would love ap
```

تشرح الأقسام التالية سير العمل الحالي على `main`، وهو ما سيدخل في الإصدار stable القادم.
