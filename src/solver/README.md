# Solver ディレクトリ（実装）

## 概要

本ディレクトリには、`include/solver/`で定義されたソルバークラスの実装が格納されています。

## ファイル

### Solver.cpp
基底ソルバークラスの実装です。

**実装される機能:**
- 共通のソルバーインターフェース
- 統計情報の収集
- ログ出力

### PCfrSolver.cpp
Public Chance Sampling CFRソルバーの実装です。

**実装される主要機能:**

#### CFRアルゴリズムの実装
```cpp
vector<float> PCfrSolver::cfr(int player, shared_ptr<GameTreeNode> node, 
                               const vector<float>& reach_probs, int iter, 
                               uint64_t current_board, int deal)
```
- 再帰的なCFR計算
- リーチ確率の伝播
- リグレットの更新

#### チャンスノード処理
```cpp
vector<float> chanceUtility(...)
```
- ボードカードのサンプリング
- 各カードパターンでの期待値計算
- 加重平均の算出

#### アクションノード処理
```cpp
vector<float> actionUtility(...)
```
- 各アクションの期待値計算
- リグレットの計算
- 戦略の更新

#### ショーダウン処理
```cpp
vector<float> showdownUtility(...)
```
- ハンド強度の比較
- エクイティの計算
- ポット分配

#### 並列処理
- OpenMPによるマルチスレッド処理
- リバーラウンドでの並列化
- スレッド間の同期

#### 同型性の活用
```cpp
void findGameSpecificIsomorphisms()
```
- カードスートの同型性検出
- 同型ハンドのマッピング
- 計算量の削減

### CfrSolver.cpp
標準CFRソルバーの実装です。

**実装される機能:**
- 全探索版CFR
- サンプリングなしの正確な計算

### BestResponse.cpp
ベストレスポンス計算の実装です。

**実装される機能:**
- 固定戦略に対する最適反応の計算
- 搾取可能性（Exploitability）の測定
- ナッシュ距離の計算

## パフォーマンス最適化

### メモリアクセスパターン
- キャッシュフレンドリーなデータ配置
- メモリアライメントの最適化

### 計算の最適化
- 不要な計算のスキップ
- インライン関数の使用
- SIMD命令の活用（将来的な拡張）

### 並列処理の最適化
- 粒度の調整
- ロック競合の最小化
- ワークスチーリング
