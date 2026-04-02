# Auto Pilot

> اسأل مرة واحدة، ثبّت الملخص، واستمر في البناء.

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](./README.md) | [한국어](./README.ko.md) | [日本語](./README.ja.md) | [中文](./README.zh.md) | العربية

## ابدأ مباشرة داخل Codex

```bash
/auto-pilot:autopilot Build a budgeting app for freelancers
/auto-pilot:autopilot-intake Build a budgeting app for freelancers
/auto-pilot:autopilot-resume Continue this project with Auto Pilot
```

Auto Pilot هو إضافة Codex محلية تحول طلباً قصيراً مثل `Build me a budgeting app` إلى سير تنفيذ يعتمد على intake-first.

بدلاً من التوقف كل بضع خطوات لطلب سياق إضافي، يقوم Auto Pilot بما يلي:

- يجمع الحد الأدنى من المدخلات المطلوبة مرة واحدة
- يحفظ عقد مشروع قابل لإعادة الاستخدام
- ينشئ ملفات spec و progress و next-step و runtime state
- يمنح Codex بنية قابلة للاستئناف للتنفيذ طويل المدى

## Why It Exists

الطلبات القصيرة مريحة، لكنها غالباً أضعف من أن تدعم عملاً ذاتياً طويل المدى.

يقوم Auto Pilot بسد هذه الفجوة عبر:

- intake بسؤال واحد في كل مرة
- definition of done صريحة
- blocker policy
- project state قابلة للاستئناف

الهدف بسيط: babysitting أقل، وتقدّم أكثر.

## What It Does

- يحول طلب المشروع القصير إلى جلسة intake منظمة
- يستخدم نمط `1. Question` / `Questions remaining: N`
- يكتب `docs/spec.md` و `docs/progress.md` و `docs/next.md` و `autopilot/state.json` و `autopilot/blockers.json`
- يحتفظ بحالة كافية لكي تستأنف جلسة Codex التالية من النقطة التي توقفت عندها
- يأتي مع plugin manifest و repo-local marketplace wiring

## Quick Start

ابدأ جلسة intake جديدة:

```bash
python3 auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

أجب عن السؤال الحالي:

```bash
python3 auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

تحقق من الوضع الحالي والحالة:

```bash
python3 auto-pilot/scripts/autopilot.py status \
  --workspace /tmp/my-project
```

بعد الإجابة الأخيرة، يقوم Auto Pilot بإنشاء:

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. يبدأ intake من خلال prompt قصير.
2. يطرح Auto Pilot سؤالاً واحداً في كل مرة.
3. يتم تحويل الإجابات إلى project contract.
4. يتم إنشاء runtime state للتنفيذ والاستئناف لاحقاً.
5. يستطيع Codex المتابعة من الملفات المحفوظة بدلاً من إعادة اكتشاف السياق.

## Repository Layout

- [auto-pilot](./auto-pilot): plugin root
- [auto-pilot/.codex-plugin/plugin.json](./auto-pilot/.codex-plugin/plugin.json): plugin manifest
- [auto-pilot/scripts](./auto-pilot/scripts): CLI and helper scripts
- [auto-pilot/skills](./auto-pilot/skills): orchestration, intake, and resume skills
- [.agents/plugins/marketplace.json](./.agents/plugins/marketplace.json): repo-local marketplace config

## Current Status

يركّز هذا المستودع حالياً على:

- intake UX
- bootstrapping لملفات spec و state
- resume-friendly file structure
- multilingual README entry points

الخطوة المنطقية التالية هي توفير one-command installer يقوم بتسجيل الإضافة تلقائياً في home-level marketplace.
