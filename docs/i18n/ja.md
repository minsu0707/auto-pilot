# Auto Pilot

---

<p align="center">
  <img src="../../assets/auto-pilot.png" alt="Auto Pilot mascot" width="260" />
</p>

> 一度だけ聞いて、ブリーフを固定し、そのまま作り続ける。

このマスコットは、[oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) の創設者が作ったヒーローアイコンのスタイルに着想を得て制作しました。

![GitHub stars](https://img.shields.io/github/stars/minsu0707/auto-pilot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/minsu0707/auto-pilot?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/minsu0707/auto-pilot?style=flat-square)
![License](https://img.shields.io/github/license/minsu0707/auto-pilot?style=flat-square)

[English](../../README.md) | [한국어](./ko.md) | 日本語

## 1行でインストール

現在の stable `v0.1.1` は `curl`、`tar`、`python3` を前提にしており、公開済みの slash command エントリーポイントを維持します。

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/v0.1.1/install.sh | bash
```

次の stable release ラインを先に試したい場合だけ `develop` を明示してインストールしてください。

```bash
curl -fsSL https://raw.githubusercontent.com/minsu0707/auto-pilot/develop/install.sh | env -u NO_COLOR bash
```

現在公開中のリリースは `v0.1.1` です。unreleased な挙動を検証したいときだけ `develop` を使ってください。次の stable tag を切るときは、stable install URL、実行例、baked-in stable ref をまとめて更新してください。

## Codex で実行

### Stable `v0.1.1`

```text
/auto-pilot:autopilot Build a budgeting app for freelancers
```

stable の公開エントリーポイントは `/auto-pilot:autopilot` です。
インストール後は slash command を読み込むために Codex を一度再起動してください。
一度インストールすれば、新規プロジェクトなら intake に進み、既存プロジェクトなら自動で resume します。
再起動後は `Build a budgeting app for freelancers ap` のような自然言語ショートカットも使えます。

### Preview on `develop`

```text
$auto-pilot Build a diary app my friend Dohyeon would love
```

`$auto-pilot` は `develop` をインストールした場合にのみ使ってください。
再起動後は `Build a diary app my friend Dohyeon would love ap` のような自然言語ショートカットも使えます。

以下のセクションでは、次の stable release に入る `main` 基準の現在のリポジトリワークフローを説明します。

## What It Is

Auto Pilot は短い製品依頼を resumable execution workflow に変える Codex プラグインです。

- 重要な入力だけを一度だけ集める
- 再利用できるプロジェクト契約を保存する
- 本当に human-only blocker が出るまで進み続ける
- 保存された状態から次のセッションで再開できる

## Why It Exists

短いプロンプトは便利ですが、長時間の自律作業には情報が足りないことが多いです。

Auto Pilot は次の要素でそのギャップを埋めます。

- 一問ずつ進む intake
- 明示的な definition of done
- デフォルトの blocker policy
- 再開可能なプロジェクト状態

目標はシンプルです。付き添いを減らし、前進を増やすことです。

## Core Features

- 短いプロジェクト依頼を構造化された intake セッションに変換する
- `1. Question` / `Questions remaining: N` パターンで対話する
- `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json` を生成する
- user-facing プロジェクトでは generic な初期UIではなく具体的なデザインブリーフから始めるために `docs/design.md` も生成する
- 次の Codex セッションが止まった場所から再開できるだけの状態を残す
- デザイン関連の説明は broad web research が完了したという意味ではなく、curated reference stack をもとにした design brief を作るという意味です
- 正式なプラグインコード、ドキュメント、インストーラをすべてリポジトリルートに置く

## Quick Start

新しい intake セッションを開始:

```bash
python3 scripts/autopilot.py start \
  --workspace /tmp/my-project \
  --prompt "Build a diary app my friend Dohyeon would love"
```

現在の質問に回答:

```bash
python3 scripts/autopilot.py answer \
  --workspace /tmp/my-project \
  --text "毎日飾りながら秘密の日記を書きたい10代のユーザー"
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
- user-facing プロジェクトなら `docs/design.md`
- `autopilot/state.json`
- `autopilot/blockers.json`

## How It Works

1. 短いプロンプトが intake を開始します。
2. Auto Pilot は質問を一つずつ行います。
3. 回答はプロジェクト契約として正規化されます。
4. user-facing プロジェクトなら、選んだ theme、vibe、design direction をもとに `docs/design.md` ブリーフも生成されます。
5. 将来の実行と再開のための runtime state が作られます。
6. Codex は保存済みファイルから続行できます。

## Repository Layout

- `docs/01-product-brief.md`: product overview
- `docs/02-prd.md`: functional requirements and operating model
- `docs/03-plugin-spec.md`: plugin structure and state model
- `docs/04-mvp-roadmap.md`: MVP implementation sequence
- `docs/05-how-it-works.md`: intake、state、resume の流れを図でまとめた文書
- `docs/06-usage-guide.md`: インストール、実行、resume、CLI、チーム運用の詳細ガイド
- `docs/i18n/*`: localized README files
- `assets/auto-pilot.png`: mascot image
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

## Current Status

このリポジトリルートがプラグインルート兼ドキュメントルート兼インストーラの基準位置です。

一般ユーザー向けの推奨フローは、one-line installer で導入し、Codex を一度再起動してから `$auto-pilot` を使うことです。
より詳しい使い方は `docs/06-usage-guide.md` を参照してください。
