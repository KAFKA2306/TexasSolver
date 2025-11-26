# Tools ディレクトリ

## 概要

本ディレクトリには、TexasSolverプロジェクトで使用される各種ユーティリティツールとライブラリが格納されています。ゲームツリー構築、コマンドライン処理、進捗表示等の補助機能を提供します。

## ファイル

### CommandLineTool.h
コマンドライン版ソルバーのツール関数です。

**主要機能:**
- 設定ファイルの読み込みと解析
- コマンドの実行とディスパッチ
- エラーハンドリング

**サポートされるコマンド:**
- `set_pot`: ポットサイズ設定
- `set_board`: ボードカード設定
- `set_range_ip/oop`: レンジ設定
- `set_bet_sizes`: ベットサイズ設定
- `build_tree`: ゲームツリー構築
- `start_solve`: 求解開始
- `dump_result`: 結果出力

### GameTreeBuildingSettings.h
ゲームツリー構築時の設定を管理するクラスです。

**主要機能:**
- ストリート別（フロップ/ターン/リバー）のベットサイズ設定
- プレイヤー別（IP/OOP）の設定管理
- アクション別（ベット/レイズ/ドンク）の設定

**データ構造:**
```cpp
struct StreetSetting {
    vector<double> bet_sizes;
    vector<double> raise_sizes;
    vector<double> donk_sizes;
    bool allow_allin;
};
```

### Rule.h
ゲームルールを定義するクラスです。

**主要機能:**
- ポットサイズの管理
- プレイヤーのコミット額追跡
- ゲームラウンドの管理
- レイズ制限の適用

**データ構造:**
- `pot`: 現在のポットサイズ
- `oop_commit`: OOPのコミット額
- `ip_commit`: IPのコミット額
- `current_round`: 現在のラウンド
- `raise_limit`: レイズ回数制限

### StreetSetting.h
ストリート（ラウンド）別の設定を定義します。

**主要機能:**
- フロップ/ターン/リバー各ラウンドの設定
- ベットサイズのパターン定義
- アクション制限の設定

### PrivateRangeConverter.h
レンジ文字列をパースして内部表現に変換します。

**主要機能:**
- レンジ記法の解析
- ハンド組み合わせの生成
- 重み付きレンジの処理

**サポートされる記法:**
- `AA`: ポケットペア
- `AKs`: スーテッド
- `AKo`: オフスート
- `88+`: 88以上のペア
- `JJ:0.5`: 50%の頻度

### utils.h
汎用ユーティリティ関数のコレクションです。

**主要機能:**
- ビット操作関数
- 数値変換ユーティリティ
- 配列操作ヘルパー
- デバッグ出力関数

### progressbar.h
コンソールでの進捗バー表示を提供します。

**主要機能:**
- イテレーション進捗の視覚化
- 推定残り時間の表示
- パーセンテージ表示

**使用例:**
```cpp
ProgressBar bar(total_iterations);
for (int i = 0; i < total_iterations; i++) {
    // 処理
    bar.update(i);
}
```

### argparse.hpp
コマンドライン引数のパースライブラリです（サードパーティ）。

**主要機能:**
- 引数の定義と解析
- ヘルプメッセージの自動生成
- 型安全な引数取得

### half-1-12-0.h
半精度浮動小数点（FP16）のライブラリです（サードパーティ）。

**主要機能:**
- IEEE 754準拠のFP16実装
- FP32との相互変換
- 算術演算のサポート

**メモリ削減効果:**
- FP32の半分のメモリ使用量
- 大規模ゲームツリーに有効

### tinyformat.h
型安全な文字列フォーマットライブラリです（サードパーティ）。

**主要機能:**
- printfスタイルのフォーマット
- C++型安全性
- ヘッダーオンリーライブラリ

**使用例:**
```cpp
tfm::format("Player %d has %f chips", player_id, stack);
```

### lookup8.h
ハッシュ関数のユーティリティです。

**主要機能:**
- Bob Jenkins のhash関数実装
- 高速なハッシュ計算
- 衝突回避の最適化

### qdebugstream.h
Qtデバッグ出力をストリームにリダイレクトします。

**主要機能:**
- qDebugの出力をキャプチャ
- カスタムログハンドラへの転送
- GUI版デバッグ支援

## ユーティリティの使用例

### ゲームツリー構築設定

```cpp
GameTreeBuildingSettings settings;

// フロップでのOOPベットサイズ
settings.flop.oop.bet_sizes = {0.5, 0.75, 1.0};
settings.flop.oop.raise_sizes = {2.0, 3.0};
settings.flop.oop.allow_allin = true;

// ターンでのIPレイズサイズ
settings.turn.ip.raise_sizes = {2.5};
```

### レンジ変換

```cpp
PrivateRangeConverter converter;
auto range = converter.parse("AA,KK,QQ,JJ:0.5,AKs,AKo:0.75");
// → vector<pair<PrivateCards, float>>
```

### 進捗表示

```cpp
ProgressBar progress(1000);
for (int iter = 0; iter < 1000; iter++) {
    solver.iterate();
    progress.update(iter);
    // 出力例: [=====>    ] 50% (500/1000) ETA: 2m 30s
}
```

### コマンドライン引数解析

```cpp
argparse::ArgumentParser program("TexasSolver");
program.add_argument("--config")
    .required()
    .help("Configuration file path");
program.add_argument("--threads")
    .default_value(4)
    .scan<'i', int>();

auto config_path = program.get<string>("--config");
auto num_threads = program.get<int>("--threads");
```

## サードパーティライブラリ

### argparse.hpp
- ライセンス: MIT
- 用途: コマンドライン引数解析
- バージョン: 最新安定版

### half-1-12-0.h
- ライセンス: MIT
- 用途: 半精度浮動小数点演算
- バージョン: 1.12.0

### tinyformat.h
- ライセンス: Boost Software License
- 用途: 型安全な文字列フォーマット
- バージョン: 最新安定版

## パフォーマンス考慮事項

### 半精度浮動小数点の使用

**メリット:**
- メモリ使用量50%削減
- キャッシュ効率の向上

**デメリット:**
- 精度低下（約3桁）
- FP32との変換オーバーヘッド

**推奨:**
- 大規模ゲームツリー（>1Mノード）で有効
- 最終精度が0.1%程度で十分な場合

### 進捗バーのオーバーヘッド

進捗バーの更新頻度を調整:
```cpp
if (iter % 10 == 0) {  // 10イテレーションごとに更新
    progress.update(iter);
}
```
