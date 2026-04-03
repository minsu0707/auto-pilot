# Auto Pilot

> 一度だけ聞いて、ブリーフを固定し、そのまま作り続ける。

[English](../../README.md) | [한국어](./ko.md) | 日本語

## 1行でインストール

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## Codex で実行

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

公開の基本エントリーポイントは `/auto-pilot:autopilot` です。
インストール後は slash command を読み込むために Codex を一度再起動してください。
一度インストールすれば、新規プロジェクトなら intake に進み、既存プロジェクトなら自動で resume します。
再起動後は `Build a budgeting app for freelancers ap` のような自然言語ショートカットも使えます。

このフォルダは `Auto Pilot` Codex プラグインの正式なルートです。このプラグインは `Build me a budgeting app` のような短い依頼を intake-first の実行ワークフローに変換します。

Auto Pilot は数ステップごとに止まって文脈を聞き直す代わりに、次のことを行います。

- 必要最小限の入力を一度だけ集める
- 再利用できるプロジェクト契約を保存する
- spec、progress、next-step、runtime state ファイルを生成する
- 次の Codex セッションでも続きから進められるようにする

## Why It Exists

短いプロンプトは便利ですが、長時間の自律作業には情報が足りないことが多いです。

Auto Pilot は次の要素でそのギャップを埋めます。

- 一問ずつ進む intake
- 明示的な definition of done
- blocker policy
- 再開可能なプロジェクト状態

目標はシンプルです。付き添いを減らし、前進を増やすことです。

## What It Does

- 短いプロジェクト依頼を構造化された intake セッションに変換する
- `1. Question` / `Questions remaining: N` UX パターンを使う
- `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json` を書き出す
- 次の Codex セッションが止まった場所から再開できるだけの状態を残す
- 正式なプラグインコード、ドキュメント、インストーラをすべて `auto-pilot/` 配下に置く

## Quick Start

新しい intake セッションを開始:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

現在の質問に回答:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

現在のモードと状態を確認:

```bash
python3 scripts/autopilot.py status \
  --workspace /tmp/my-project
```

最後の回答後、Auto Pilot は次のファイルを生成します。

- `docs/spec.md`
- `docs/progress.md`
- `docs/next.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 短いプロンプトが intake を開始します。
2. Auto Pilot は質問を一つずつ行います。
3. 回答はプロジェクト契約として正規化されます。
4. 将来の実行と再開のための runtime state が作られます。
5. Codex は文脈を再探索せず、保存済みファイルから続行できます。

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/i18n/*`: localized README files
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `commands/autopilot.md`: public slash command entry point
- `skills/autopilot/SKILL.md`: main orchestration skill
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

次のように依頼できます。

- `Start this project with Auto Pilot`
- `Use autopilot to kick off a SaaS MVP`
- `Continue this project with Auto Pilot`
- `Build a budgeting app for freelancers ap`

新しいプロジェクトでは intake は次の UX に従います。

- 一度に一つの質問だけ表示
- `1. Question` 形式を使用
- 次の行に `Questions remaining: N` を表示
- 最後の回答後に契約を要約し、spec lock と実行を開始

下位スクリプトもそのまま使えます。

- `init_intake.py`
- `record_answer.py`
- `status.py`

## Current Status

このフォルダがプラグインルート兼ドキュメントルート兼インストーラの基準位置です。

一般ユーザー向けの推奨フローは、one-line installer で導入し、Codex を一度再起動してから `/auto-pilot:autopilot` を使うことです。
