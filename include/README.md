# Include ディレクトリ

## 概要

本ディレクトリには、TexasSolverプロジェクトの全てのC++ヘッダーファイルが格納されています。テキサスホールデムおよびショートデッキの求解に必要なコアアルゴリズム、データ構造、およびユーティリティ関数の宣言が含まれています。

## 主要ファイル

### Card.h
トランプカードを表現するクラスです。

**主要な機能:**
- カードの文字列表現と整数表現の相互変換
- ボードカードの64ビット整数表現への変換
- カードの重複チェック
- スートとランクの変換ユーティリティ

### Deck.h
デッキを表現するクラスです。テキサスホールデム（52枚）とショートデッキ（36枚）の両方に対応しています。

### GameTree.h
ゲームツリーを構築および管理するクラスです。

**主要な機能:**
- JSONファイルからのゲームツリーの読み込み
- 動的なゲームツリーの構築
- ベットサイズの計算と丸め処理
- ツリーのメモリ使用量の推定

### library.h
汎用的なユーティリティ関数とテンプレートクラスを提供します。

**主要な機能:**
- `Combinations<T>`: 組み合わせを生成するテンプレートクラス
- `string_split`: 文字列分割関数
- `timeSinceEpochMillisec`: エポックからのミリ秒取得
- `normalization_tanh`: tanh正規化関数

## サブディレクトリ

### nodes/
ゲームツリーノードの各種実装が含まれています:
- `ActionNode.h`: アクションノード（ベット、チェック、フォールド等）
- `ChanceNode.h`: チャンスノード（カード配布）
- `ShowdownNode.h`: ショーダウンノード
- `TerminalNode.h`: 終端ノード
- `GameTreeNode.h`: 全ノードの基底クラス

### solver/
求解アルゴリズムの実装が含まれています:
- `Solver.h`: ソルバーの基底クラス
- `PCfrSolver.h`: Public Chance Sampling CFR実装
- `CfrSolver.h`: 標準CFR実装
- `BestResponse.h`: ベストレスポンス計算

### ranges/
プレイヤーのハンドレンジ管理:
- `PrivateCards.h`: プライベートカードの表現
- `PrivateCardsManager.h`: プライベートカード管理
- `RiverRangeManager.h`: リバーでのレンジ管理
- `RiverCombs.h`: リバーでの組み合わせ

### trainable/
CFRトレーニング可能なノードの実装:
- `Trainable.h`: トレーニング可能オブジェクトの基底クラス
- `CfrPlusTrainable.h`: CFR+アルゴリズム実装
- `DiscountedCfrTrainable.h`: ディスカウントCFR実装
- `DiscountedCfrTrainableHF.h`: 半精度浮動小数点版
- `DiscountedCfrTrainableSF.h`: 単精度浮動小数点版

### tools/
各種ユーティリティツール:
- `CommandLineTool.h`: コマンドライン解析
- `GameTreeBuildingSettings.h`: ツリー構築設定
- `Rule.h`: ゲームルール定義
- `StreetSetting.h`: ストリート別設定
- `utils.h`: 汎用ユーティリティ関数
- `progressbar.h`: 進捗バー表示
- `argparse.hpp`: 引数解析ライブラリ
- `half-1-12-0.h`: 半精度浮動小数点ライブラリ

### compairer/
ハンド強度比較:
- ポーカーハンドの強度評価と比較機能

### runtime/
ランタイム関連の機能

### ui/
ユーザーインターフェース関連のヘッダー

### experimental/
実験的な機能の実装
