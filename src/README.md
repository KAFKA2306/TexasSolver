# Src ディレクトリ

## 概要

本ディレクトリには、TexasSolverプロジェクトの全てのC++実装ファイル（.cpp）が格納されています。`include/`ディレクトリのヘッダーファイルに対応する実装が含まれています。

## 主要ファイル

### Card.cpp
`Card`クラスの実装です。

**実装される主要機能:**
- カード文字列（例: "As", "Kh"）から整数への変換
- 整数からカード文字列への逆変換
- ボードカードのビットボード表現（64ビット整数）への変換
- スート（♠♥♦♣）とランク（A-2）の解析と文字列化
- HTML形式でのカード表示（色付き）

### Deck.cpp
`Deck`クラスの実装です。

**実装される主要機能:**
- テキサスホールデム用52枚デッキの初期化
- ショートデッキ用36枚デッキの初期化（2-5を除く）
- デッキからのカード取得とシャッフル

### GameTree.cpp
ゲームツリーの構築と管理を実装します。

**実装される主要機能:**
- ゲームツリーの再帰的構築
- アクションノード（ベット、レイズ、チェック、フォールド）の生成
- チャンスノード（カード配布）の処理
- ベットサイズの計算と設定からの読み込み
- ツリーのJSONシリアライゼーション
- メモリ使用量の推定

### api.cpp
FFI（Foreign Function Interface）APIの実装です。

**実装される主要機能:**
- C言語互換APIの提供
- 他の言語（Python、Rust等）からのソルバー呼び出しインターフェース

### console.cpp
コンソール版ソルバーのエントリーポイントです。

**実装される主要機能:**
- コマンドライン引数の解析
- 設定ファイルの読み込み
- ソルバーの初期化と実行

### library.cpp
`library.h`で宣言された汎用関数の実装です。

**実装される主要機能:**
- 文字列分割処理
- 時刻取得
- 乱数生成
- tanh正規化

## サブディレクトリ

### nodes/
ゲームツリーノードの実装:
- `ActionNode.cpp`: プレイヤーアクションの処理
- `ChanceNode.cpp`: チャンスイベント（カード配布）の処理
- `ShowdownNode.cpp`: ショーダウン時の勝者判定
- `TerminalNode.cpp`: 終端ノードの処理
- `GameTreeNode.cpp`: 基底ノードクラスの実装

### solver/
求解アルゴリズムの実装:
- `Solver.cpp`: ソルバー基底クラス
- `PCfrSolver.cpp`: Public Chance Sampling CFRアルゴリズムの実装
  - 並列処理対応
  - 同型性（isomorphism）の活用
  - 半精度浮動小数点による最適化
- `CfrSolver.cpp`: 標準CFRアルゴリズム
- `BestResponse.cpp`: ベストレスポンス計算

### ranges/
レンジ管理の実装:
- `PrivateCards.cpp`: プライベートカード表現
- `PrivateCardsManager.cpp`: カード組み合わせの管理
- `RiverRangeManager.cpp`: リバーラウンドでのレンジ管理
- `RiverCombs.cpp`: リバーでの可能な組み合わせ計算

### trainable/
CFRトレーニング実装:
- `Trainable.cpp`: 基底トレーニング可能クラス
- `CfrPlusTrainable.cpp`: CFR+アルゴリズム（リグレットマッチングの改良版）
- `DiscountedCfrTrainable.cpp`: ディスカウントCFR（線形ディスカウント）
- `DiscountedCfrTrainableHF.cpp`: 半精度浮動小数点版（メモリ効率化）
- `DiscountedCfrTrainableSF.cpp`: 単精度浮動小数点版

### tools/
ユーティリティツールの実装:
- `CommandLineTool.cpp`: コマンドライン処理
- `GameTreeBuildingSettings.cpp`: ツリー構築パラメータ
- `Rule.cpp`: ゲームルールの適用
- `PrivateRangeConverter.cpp`: レンジ文字列のパース
- `utils.cpp`: 各種ユーティリティ関数

### compairer/
ハンド評価の実装:
- ポーカーハンドの強度計算
- ハンド同士の比較

### runtime/
ランタイムシステムの実装

### ui/
ユーザーインターフェース関連の実装（Qt GUI）

### pybind/
Python バインディングの実装:
- Pybind11を使用したPythonインターフェース

### experimental/
実験的機能の実装
