# auto-pilot

`Auto Pilot` のローカル Codex プラグインリポジトリです。

## 言語

- English: [`README.md`](/Users/minsu/Documents/Codex/README.md)
- 한국어: [`README.ko.md`](/Users/minsu/Documents/Codex/README.ko.md)
- 日本語: `README.ja.md`
- 中文: [`README.zh.md`](/Users/minsu/Documents/Codex/README.zh.md)
- العربية: [`README.ar.md`](/Users/minsu/Documents/Codex/README.ar.md)

## 内容

- [Auto Pilot プラグインルート](/Users/minsu/Documents/Codex/auto-pilot)
- [リポジトリローカル marketplace 設定](/Users/minsu/Documents/Codex/.agents/plugins/marketplace.json)
- intake、状態生成、再開フロー用スクリプト

## 主な機能

- 短いプロジェクト依頼を intake セッションに変換
- 質問を 1 回に 1 つずつ表示
- `1. Question` / `Questions remaining: N` UX を使用
- 最後の回答後に `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json` を自動生成
- 後続の Codex セッションで再開できる状態構造を保持
