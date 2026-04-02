# auto-pilot

[English](./README.md) | [한국어](./README.ko.md) | 日本語 | [中文](./README.zh.md) | [العربية](./README.ar.md)

`Auto Pilot` のローカル Codex プラグインリポジトリです。

## 内容

- [Auto Pilot プラグインルート](./auto-pilot)
- [リポジトリローカル marketplace 設定](./.agents/plugins/marketplace.json)
- intake、状態生成、再開フロー用スクリプト

## 主な機能

- 短いプロジェクト依頼を intake セッションに変換
- 質問を 1 回に 1 つずつ表示
- `1. Question` / `Questions remaining: N` UX を使用
- 最後の回答後に `docs/spec.md`、`docs/progress.md`、`docs/next.md`、`autopilot/state.json`、`autopilot/blockers.json` を自動生成
- 後続の Codex セッションで再開できる状態構造を保持
