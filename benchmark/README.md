# Benchmark ディレクトリ

## 概要

本ディレクトリには、TexasSolverとPioSolverの性能比較ベンチマークファイルが格納されています。

## ファイル

### benchmark_piosolver.txt
PioSolver用のベンチマーク設定ファイルです。

**設定内容:**
- SPR（Stack-to-Pot Ratio）: 10
- フロップゲーム
- スレッド数: 6
- 目標精度: 0.29%
- 収束時間: 242秒

### benchmark_texassolver.txt
TexasSolver用のベンチマーク設定ファイルです。

**設定内容:**
- SPR（Stack-to-Pot Ratio）: 10
- フロップゲーム
- スレッド数: 6
- 目標精度: 0.275%
- 収束時間: 172秒

## サブディレクトリ

### benchmark_outputs/
ベンチマーク実行結果の出力ファイルが格納されています:
- `piosolver_log.txt`: PioSolverの実行ログ
- `texassolver_log.txt`: TexasSolverの実行ログ
- `result_compair.png`: 両ソルバーの結果比較画像

## ベンチマーク結果

### 性能比較

| ソルバー | メモリ使用量 | 精度 | 収束時間 | スレッド数 |
|---------|------------|------|---------|---------|
| PioSolver 1.0 | 492MB | 0.29% | 242秒 | 6 |
| TexasSolver 0.1.0 | 1600MB | 0.275% | 172秒 | 6 |

### 分析

**TexasSolverの利点:**
- 収束時間が約29%短縮（242秒 → 172秒）
- わずかに高い精度（0.275% vs 0.29%）

**トレードオフ:**
- メモリ使用量が約3.25倍（492MB → 1600MB）

両ソルバーの戦略結果は非常に近似しており、実用上同等の精度を持つことが確認されています。
