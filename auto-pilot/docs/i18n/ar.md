# Auto Pilot Docs

> اسأل مرة واحدة، ثبّت الملخص، واستمر في البناء.

[English](../../README.md) | [한국어](./ko.md) | [日本語](./ja.md) | [中文](./zh.md) | العربية

## ابدأ مباشرة داخل Codex

```bash
/auto-pilot:autopilot Build a budgeting app for freelancers
```

استخدم `/auto-pilot:autopilot` كنقطة الدخول العامة الوحيدة.
إذا كان المشروع جديدًا فسيبدأ intake تلقائيًا، وإذا كان موجودًا فسيتم الاستئناف تلقائيًا.

يحتوي هذا المجلد على الحزمة الأولية من مستندات إضافة Codex المسماة `Auto Pilot`. تقوم الإضافة بتحويل طلب مشروع قصير إلى سير تنفيذ طويل المدى يعتمد على intake-driven.

## Files

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `skills/autopilot/SKILL.md`: main orchestration skill
- `skills/autopilot-intake/SKILL.md`: one-question-at-a-time intake skill
- `skills/autopilot-resume/SKILL.md`: resume skill
- `scripts/autopilot.py`: recommended CLI entry point
- `scripts/*.py`: intake, answer recording, and status scripts
- `templates/*.json`: state templates

## Current Identity

- Product name: `Auto Pilot`
- Plugin slug: `auto-pilot`

## Current Status

هذا المجلد هو plugin root. يتم ربط repo-local marketplace عبر [marketplace.json](../../../.agents/plugins/marketplace.json).

## Usage

يمكنك طلب ما يلي:

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`

في المشاريع الجديدة يتبع intake هذا النمط:

- عرض سؤال واحد فقط في كل مرة
- استخدام تنسيق `1. Question`
- عرض `Questions remaining: N` في السطر التالي
- بعد الإجابة الأخيرة يتم تلخيص العقد ثم يبدأ spec lock والتنفيذ

## Script Example

```bash
python3 scripts/autopilot.py start \
  --workspace /path/to/project \
  --prompt "Build a budgeting app for freelancers"

python3 scripts/autopilot.py answer \
  --workspace /path/to/project \
  --text "Freelancers and solo business owners"

python3 scripts/autopilot.py status \
  --workspace /path/to/project
```

بعد الإجابة الأخيرة، يقوم Auto Pilot بإنشاء الملفات التالية:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

تبقى السكربتات منخفضة المستوى متاحة أيضاً:

- `init_intake.py`
- `record_answer.py`
- `status.py`

قد لا تقوم الجلسة الحالية بتحديث قائمة الإضافات فوراً. أكثر طريقة أماناً لفرض plugin discovery هي إعادة فتح الـ workspace في جلسة جديدة.
