# Auto Pilot

> اسأل مرة واحدة، ثبّت الملخص، واستمر في البناء.

[English](../../README.md) | [한국어](./ko.md) | [日本語](./ja.md) | [中文](./zh.md) | العربية

دليل الاستخدام التفصيلي: [`docs/06-usage-guide.md`](../../docs/06-usage-guide.md)

## ثبّت بسطر واحد

الإصدار stable الحالي `v0.1.1` يتطلب `curl` و`tar` و`python3`، ويُبقي نقطة الدخول المنشورة عبر slash command.

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

إذا أردت تجربة خط الإصدار التالي قبل نشره، فثبّت `develop` بشكل صريح:

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/develop/install.sh | env -u NO_COLOR bash
```

الإصدار المنشور حاليًا هو `v0.1.1`. استخدم `develop` فقط عندما تريد اختبار سلوك غير منشور. وعند إصدار stable tag التالي يجب تحديث stable install URL وأمثلة التشغيل وbaked-in stable ref معًا.

## شغّل داخل Codex

### Stable `v0.1.1`

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

استخدم `/auto-pilot:autopilot` كنقطة الدخول العامة الأساسية في stable.
بعد التثبيت، أعد تشغيل Codex مرة واحدة حتى يصبح slash command متاحًا.
بعد التثبيت مرة واحدة، يبدأ intake تلقائيًا للمشاريع الجديدة ويستأنف المشاريع الحالية تلقائيًا.
بعد إعادة التشغيل يمكنك أيضًا استخدام الاختصار الطبيعي `Build a budgeting app for freelancers ap`.

### Preview on `develop`

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

استخدم `$auto-pilot` فقط إذا كنت قد ثبّت الإصدار من `develop`.
بعد إعادة التشغيل يمكنك أيضًا استخدام الاختصار الطبيعي `Build a diary app my friend Dohyeon would love ap`.

تشرح الأقسام التالية سير العمل الحالي على `main`، وهو ما سيدخل في الإصدار stable القادم.

هذا المجلد هو الجذر الرسمي لإضافة Codex المسماة `Auto Pilot`. تقوم الإضافة بتحويل طلب قصير مثل `Build me a budgeting app` إلى سير تنفيذ intake-first.

بدلًا من التوقف كل بضع خطوات لإعادة طلب السياق، يقوم Auto Pilot بما يلي:

- يجمع الحد الأدنى من المدخلات المطلوبة مرة واحدة
- يحفظ عقد مشروع قابلًا لإعادة الاستخدام
- ينشئ ملفات spec وprogress وnext-step وruntime state
- يمنح Codex بنية قابلة للاستئناف عبر الجلسات

## Why It Exists

الطلبات القصيرة مريحة، لكنها غالبًا لا تكفي لعمل ذاتي طويل.

يسد Auto Pilot هذه الفجوة عبر:

- intake بسؤال واحد في كل مرة
- definition of done واضح
- blocker policy افتراضي
- حالة مشروع قابلة للاستئناف

الهدف بسيط: babysitting أقل، وتقدم أكثر.

## What It Does

- يحول طلب مشروع قصير إلى جلسة intake منظمة
- يستخدم نمط UX من نوع `1. Question` / `Questions remaining: N`
- يكتب `docs/spec.md` و`docs/progress.md` و`docs/next.md` و`autopilot/state.json` و`autopilot/blockers.json`
- وفي المشاريع ذات الواجهة للمستخدم ينشئ أيضًا `docs/design.md` بحيث يبدأ العمل من design brief واضح بدلًا من واجهة generic افتراضية
- يحتفظ بحالة كافية لكي تستأنف جلسة Codex التالية من حيث توقفت
- وصف التصميم هنا يعني إنشاء design brief مبني على curated references، وليس الادعاء بأنه أنهى بحثًا واسعًا عبر الويب
- يبقي الكود الرسمي للإضافة والوثائق ومنطق التثبيت جميعها في جذر المستودع

## Quick Start

ابدأ جلسة intake جديدة:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a diary app my friend Dohyeon would love"
```

أجب عن السؤال الحالي:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "مستخدمون صغار السن يريدون تطبيق يوميات دافئًا وخاصًا يمكن تزيينه كل يوم"
```

تحقق من الوضع الحالي والحالة:

```bash
python3 scripts/autopilot.py status \
  --workspace /tmp/my-project
```

بعد الإجابة الأخيرة، ينشئ Auto Pilot الملفات التالية:

- `docs/spec.md`
- `docs/design.md` للمشاريع ذات الواجهة للمستخدم
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. يبدأ prompt قصير عملية intake.
2. يطرح Auto Pilot سؤالًا واحدًا في كل مرة.
3. تُطبَّع الإجابات إلى عقد مشروع.
4. وفي المشاريع ذات الواجهة للمستخدم، يُنشأ أيضًا `docs/design.md` اعتمادًا على theme وvibe وdesign direction.
5. تُنشأ runtime state للتنفيذ والاستئناف لاحقًا.
6. يمكن لـ Codex المتابعة من الملفات المحفوظة بدلًا من إعادة اكتشاف السياق.

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/05-how-it-works.md`: شرح مرئي لتدفق intake وstate وresume
- `docs/06-usage-guide.md`: دليل مفصل للتثبيت والتشغيل وresume وCLI وتنظيم الفريق
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: secondary plugin command entry point
- `skills/auto-pilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates
- `install.sh`: canonical installer
- `uninstall.sh`: canonical uninstaller

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Usage

يمكنك طلب ما يلي:

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`
- `Build a diary app my friend Dohyeon would love ap`

في المشاريع الجديدة يتبع intake هذا النمط:

- عرض سؤال واحد فقط في كل مرة
- استخدام تنسيق `1. Question`
- عرض `Questions remaining: N` في السطر التالي
- بعد الإجابة الأخيرة يتم تلخيص العقد ثم يبدأ spec lock والتنفيذ

تبقى السكربتات منخفضة المستوى متاحة أيضاً:

- `init_intake.py`
- `record_answer.py`
- `status.py`

## Current Status

جذر هذا المستودع هو جذر الإضافة وجذر الوثائق والمكان المرجعي لسكربتات التثبيت.

بالنسبة للمستخدم العادي، المسار الموصى به هو التثبيت عبر one-line installer ثم إعادة تشغيل Codex مرة واحدة وبعدها استخدام `$auto-pilot` داخل Codex.
إذا أردت شرحًا أكمل للاستخدام، ابدأ بقراءة `docs/06-usage-guide.md`.
