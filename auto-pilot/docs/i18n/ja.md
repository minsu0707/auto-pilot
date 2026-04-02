# Auto Pilot Docs

> 一度だけ聞いて、ブリーフを固定し、そのまま作り続ける。

[English](../../README.md) | [한국어](./ko.md) | 日本語 | [中文](./zh.md) | [العربية](./ar.md)

このフォルダには `Auto Pilot` Codex プラグインの初期ドキュメントパッケージが含まれています。このプラグインは短いプロジェクト依頼を intake-driven の長時間自律実行ワークフローに変換します。

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

このフォルダは plugin root です。repo-local marketplace は [marketplace.json](../../../.agents/plugins/marketplace.json) で接続されています。

## Usage

次のように依頼できます。

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`

新しいプロジェクトでは intake は次の UX に従います。

- 一度に一つの質問だけ表示
- `1. Question` 形式を使用
- 次の行に `Questions remaining: N` を表示
- 最後の回答後に契約を要約し、spec lock と実行を開始

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

最後の回答後、次のファイルが生成されます。

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

下位スクリプトもそのまま使えます。

- `init_intake.py`
- `record_answer.py`
- `status.py`

現在のセッションではプラグイン一覧がすぐには更新されないことがあります。新しいセッションで workspace を再度開くのが plugin discovery を反映する最も安全な方法です。
