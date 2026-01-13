# 🎯 Dynamic Visual Acuity Training & Testing App

動的視力トレーニング＆テストのためのStreamlitアプリケーションです。

## 概要

このアプリケーションは、動的視力（動いている物体に対する反応能力）を測定・トレーニングするためのWebアプリです。

### 主な機能

- **反応時間テスト**: ランダムなタイミングで表示されるターゲットに素早く反応する5回のトライアル
- **移動ターゲットテスト**: ランダムな位置に表示されるターゲットをクリックする8回のトライアル
- **結果の可視化**: 反応時間のグラフ表示と統計情報
- **パフォーマンス比較**: 平均的な人やアスリートとの比較

## ローカルでの実行方法

### 必要な環境

- Python 3.8以上

### インストール

```bash
pip install -r requirements.txt
```

### 起動

```bash
streamlit run dynamic_visual_acuity_app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます。

## Streamlit Cloudでの実行

このアプリはStreamlit Cloudでも動作します。

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## 使い方

1. 「Start Test」ボタンをクリックしてテストを開始
2. 反応時間テスト：ターゲットが表示されたら素早くクリック
3. 移動ターゲットテスト：ランダムな位置に表示されるターゲットをクリック
4. 結果を確認し、ベースライン値と比較
5. 「Retry Test」ボタンで再テスト可能

## 技術スタック

- Python 3.x
- Streamlit
- Pandas

## ライセンス

MIT License
