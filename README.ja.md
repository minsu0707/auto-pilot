# Auto Pilot

> 一度だけ聞いて、ブリーフを固定し、そのまま作り続ける。

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](./README.md) | [한국어](./README.ko.md) | 日本語 | [中文](./README.zh.md) | [العربية](./README.ar.md)

## 1行でインストール

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/main/install.sh | bash
```

## Codex で実行

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

公開エントリーポイントは `/auto-pilot:autopilot` ひとつで十分です。
インストール後は slash command を読み込むために Codex を一度再起動してください。
一度インストールすれば、新規プロジェクトなら intake に進み、既存プロジェクトなら自動で resume します。

Auto Pilot は、`Build me a budgeting app` のような短い依頼を intake-first の実行フローへ変換するローカル Codex プラグインです。

途中で何度も止まって不足情報を聞き直す代わりに、Auto Pilot は:

- 必要な入力を一度だけ集め
- 再利用できるプロジェクト契約を保存し
- spec、progress、next-step、runtime state ファイルを生成し
- Codex が長時間実行を再開できる構造を提供します

## Why It Exists

短いプロンプトは便利ですが、長時間の自律実行には情報が足りないことが多いです。

Auto Pilot は次の仕組みでそのギャップを埋めます。

- 一問ずつ進む intake
- 明示的な definition of done
- blocker policy
- 再開可能な project state

目的は単純です。babysitting を減らし、前進を増やすことです。

## What It Does

- 短いプロジェクト依頼を構造化された intake セッションに変換します
- `1. Question` / `Questions remaining: N` UX を使います
- `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json` を生成します
- 次の Codex セッションが止まった地点から再開できるだけの state を残します
- プラグインマニフェストと repo-local marketplace wiring を含みます

## Quick Start

新しい intake セッションを開始します。

```bash
python3 auto-pilot/scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a budgeting app for freelancers"
```

現在の質問に答えます。

```bash
python3 auto-pilot/scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "Freelancers and solo business owners"
```

現在のモードと状態を確認します。

```bash
python3 auto-pilot/scripts/autopilot.py status \
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
2. Auto Pilot が一問ずつ質問します。
3. 回答を project contract として正規化します。
4. 以後の実行と再開のために runtime state を作成します。
5. Codex はコンテキストを再発見せず、保存されたファイルから続行できます。

## Repository Layout

- [auto-pilot](./auto-pilot): plugin root
- [auto-pilot/.codex-plugin/plugin.json](./auto-pilot/.codex-plugin/plugin.json): plugin manifest
- [auto-pilot/scripts](./auto-pilot/scripts): CLI and helper scripts
- [auto-pilot/skills](./auto-pilot/skills): orchestration, intake, and resume skills
- [.agents/plugins/marketplace.json](./.agents/plugins/marketplace.json): repo-local marketplace config

## Current Status

現在このリポジトリは次のものを提供しています。

- home-level プラグイン導入用の one-line installer
- intake UX
- spec と state の bootstrapping
- resume-friendly file structure
- multilingual README entry points
