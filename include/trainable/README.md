# Trainable ディレクトリ

## 概要

本ディレクトリには、CFR（Counterfactual Regret Minimization）アルゴリズムでトレーニング可能なノードの実装が格納されています。各アクションノードに付随し、リグレットと戦略を管理します。

## ファイル

### Trainable.h
全てのトレーニング可能クラスの基底クラスです。

**主要機能:**
- トレーニング可能オブジェクトの共通インターフェース定義
- 仮想関数による多態性の提供

**主要仮想関数:**
- `updateRegret()`: リグレットの更新
- `getStrategy()`: 現在の戦略の取得
- `getAverageStrategy()`: 平均戦略の取得

### CfrPlusTrainable.h
CFR+アルゴリズムの実装です。

**主要機能:**
- リグレットマッチング+（Regret Matching+）
- 負のリグレットをゼロにリセット
- より高速な収束

**アルゴリズムの特徴:**
- 標準CFRの改良版
- 負のリグレットを蓄積しない
- 実用的な性能と収束速度のバランス

**データ構造:**
- `cumulative_regret`: 累積リグレット（正値のみ）
- `strategy_sum`: 戦略の累積和
- `num_actions`: アクション数

**主要メソッド:**
- `update()`: リグレットと戦略の更新
- `getCurrentStrategy()`: 現在の戦略計算
- `getAverageStrategy()`: 平均戦略計算

### DiscountedCfrTrainable.h
ディスカウントCFRアルゴリズムの実装（全精度版）です。

**主要機能:**
- 線形ディスカウント方式
- 過去のイテレーションの影響を徐々に減衰
- 安定した収束特性

**ディスカウント計算:**
```
discount_factor = (iteration / (iteration + 1))^α
```
ここで、αはディスカウント指数（通常1.5-2.0）

**特徴:**
- 初期イテレーションのノイズを軽減
- 後期イテレーションの精度を向上
- 大規模ゲームに適している

**データ構造:**
- `cumulative_regret`: 累積リグレット（ディスカウント適用）
- `strategy_sum`: 戦略の累積和（ディスカウント適用）
- `iteration`: 現在のイテレーション数
- `discount_alpha`: ディスカウント指数

### DiscountedCfrTrainableHF.h
ディスカウントCFRの半精度浮動小数点版です。

**主要機能:**
- 16ビット浮動小数点（FP16）を使用
- メモリ使用量を約50%削減
- わずかな精度低下とのトレードオフ

**メモリ効率:**
```
通常版: 4 bytes × num_actions × 2 (regret + strategy)
半精度版: 2 bytes × num_actions × 2 → 50%削減
```

**適用シーン:**
- 大規模ゲームツリー
- メモリ制約がある環境
- 実用精度で十分な場合

### DiscountedCfrTrainableSF.h
ディスカウントCFRの単精度浮動小数点版です。

**主要機能:**
- 32ビット浮動小数点（FP32）を使用
- 標準的な精度とメモリ使用量のバランス

**特徴:**
- 最も一般的に使用される実装
- 十分な精度を維持
- ほとんどのケースで推奨

## アルゴリズムの比較

### CFR+

**利点:**
- シンプルな実装
- 高速な収束
- 小中規模のゲームに最適

**欠点:**
- 大規模ゲームでは収束が遅い場合がある
- 初期ノイズの影響を受けやすい

### ディスカウントCFR

**利点:**
- 大規模ゲームでも安定した収束
- 初期ノイズの影響を軽減
- 最終精度が高い

**欠点:**
- わずかに複雑な実装
- ディスカウント係数の調整が必要

## リグレットマッチング

### 基本原理

各アクションのリグレットを計算:
```
Regret[action] = EV[action] - EV[chosen_action]
```

リグレットに基づいて戦略を更新:
```
Strategy[action] = max(0, Regret[action]) / sum(max(0, Regret[a]) for a in Actions)
```

### CFR+の改良点

負のリグレットを即座にゼロにリセット:
```
Regret[action] = max(0, Regret[action] + new_regret)
```

これにより、過去の悪い選択の影響を排除し、より高速に収束します。

### ディスカウントの効果

古いイテレーションのリグレットを減衰:
```
Discounted_Regret = Regret × discount_factor^(total_iter - current_iter)
```

これにより、最近のサンプルを重視し、初期のノイズを除去します。

## 精度とメモリのトレードオフ

### 倍精度（FP64）
- メモリ: 8 bytes/値
- 精度: 約15桁
- 用途: デバッグ、高精度検証

### 単精度（FP32）
- メモリ: 4 bytes/値
- 精度: 約7桁
- 用途: 標準的な使用（推奨）

### 半精度（FP16）
- メモリ: 2 bytes/値
- 精度: 約3桁
- 用途: 大規模ゲーム、メモリ制約

## 使用例

```cpp
// CFR+の使用
auto trainable = make_shared<CfrPlusTrainable>(num_actions);
trainable->update(regrets, current_strategy, iteration);
auto avg_strategy = trainable->getAverageStrategy();

// ディスカウントCFRの使用（半精度）
auto trainable_hf = make_shared<DiscountedCfrTrainableHF>(num_actions, discount_alpha);
trainable_hf->update(regrets, current_strategy, iteration);
auto avg_strategy_hf = trainable_hf->getAverageStrategy();
```

## パフォーマンスへの影響

### メモリ使用量

大規模ゲームツリー（100万ノード、平均3アクション）の場合:
- FP64: 48 MB
- FP32: 24 MB（推奨）
- FP16: 12 MB（メモリ制約時）

### 収束速度

- CFR+: 小規模で最速
- ディスカウントCFR: 大規模で安定
- 半精度: わずかに遅いが実用的

## 推奨設定

### 小規模ゲーム（ノード数 < 100K）
- アルゴリズム: CFR+
- 精度: FP32

### 中規模ゲーム（100K < ノード数 < 1M）
- アルゴリズム: ディスカウントCFR
- 精度: FP32

### 大規模ゲーム（ノード数 > 1M）
- アルゴリズム: ディスカウントCFR
- 精度: FP16
- ディスカウント指数: 1.5-2.0
