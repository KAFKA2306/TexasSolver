# Runtime ディレクトリ

## 概要

本ディレクトリには、TexasSolverのランタイムシステムに関連する機能が格納されています。

## 主要機能

### スレッド管理
CFR計算の並列実行を管理します。

**機能:**
- スレッドプールの管理
- タスクのディスパッチ
- 同期とロック管理

### メモリ管理
効率的なメモリ使用を実現します。

**機能:**
- メモリプールの管理
- オブジェクトの再利用
- ガベージコレクション

### パフォーマンス監視
実行時のパフォーマンスメトリクスを収集します。

**収集される情報:**
- CPU使用率
- メモリ使用量
- イテレーション速度
- 収束状況

## 使用例

```cpp
Runtime runtime;
runtime.setThreadCount(8);
runtime.setMemoryLimit(4096); // MB
runtime.enableProfiling(true);

solver.setRuntime(runtime);
solver.train();

auto stats = runtime.getStatistics();
```
