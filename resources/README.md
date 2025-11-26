# Resources ディレクトリ

## 概要

本ディレクトリには、TexasSolverプロジェクトで使用される各種リソースファイルが格納されています。設定ファイル、スクリプト、サンプルデータ、Python/FFIバインディング等が含まれます。

## サブディレクトリ

### bash/
Bashスクリプトが格納されています:
- ビルドスクリプト
- デプロイメントスクリプト

### compairer/
ハンド比較関連のリソースファイル:
- ハンド強度評価用のデータファイル
- ルックアップテーブル

### desktop/
デスクトップアプリケーション用のリソース:
- アプリケーションアイコン
- `.desktop`ファイル（Linux用）

### ffi_api/
FFI（Foreign Function Interface）API関連:
- C言語互換APIのドキュメント（`README.MD`）
- サンプルコード
- 他言語（Python、Rust等）からの呼び出し例

**主要機能:**
- DLL/SO/DYLIBを通じたライブラリ呼び出し
- 設定ファイルベースのソルバー実行
- JSON形式での結果出力

### gametree/
ゲームツリーのサンプルファイル:
- 事前構築されたゲームツリーのJSON
- ツリー構造のテンプレート

### outputs/
ソルバーの出力ファイル格納場所:
- 求解結果のJSON
- 戦略ダンプファイル

### python/
Python バインディングとサンプルコード:
- Pybind11ベースのPythonインターフェース
- Pythonからのソルバー使用例
- サンプルスクリプト

**主要機能:**
- Pythonからの直接ソルバー呼び出し
- NumPy配列との統合
- 結果の解析とビジュアライゼーション

### text/
テキスト形式の設定ファイル:
- `commandline_sample_input.txt`: コマンドライン版のサンプル入力
- ゲームツリー構築パラメータ
- ベットサイズ設定
- レンジ定義

**設定例:**
```
set_pot 50
set_effective_stack 200
set_board Qs,Jh,2h
set_range_ip [レンジ定義]
set_range_oop [レンジ定義]
set_bet_sizes [ベットサイズ設定]
build_tree
start_solve
dump_result output_result.json
```

### yamls/
YAML形式の設定ファイル:
- より構造化された設定ファイル
- 複数のゲームシナリオ定義
- デフォルト設定

## 使用方法

### FFI API経由での使用

Python例:
```python
from ctypes import *
api_library = CDLL('api.dll')  # Windows
api_library.api(b"resources/text/commandline_sample_input.txt", b"./resources", b"holdem")
```

### Python バインディング経由での使用

```python
import texassolver
solver = texassolver.create_solver(config)
solver.train()
result = solver.get_results()
```

### コマンドライン経由での使用

```bash
./TexasSolverConsole --config resources/text/commandline_sample_input.txt
```

## 設定ファイル形式

### ゲーム基本設定
- `set_pot`: ポットサイズ
- `set_effective_stack`: 有効スタックサイズ
- `set_board`: ボードカード

### レンジ設定
- `set_range_ip`: インポジションのレンジ
- `set_range_oop`: アウトオブポジションのレンジ

### ベットサイズ設定
- `set_bet_sizes [position],[round],[action],[sizes]`
- 例: `set_bet_sizes oop,flop,bet,50`

### ソルバー設定
- `set_thread_num`: スレッド数
- `set_accuracy`: 目標精度
- `set_max_iteration`: 最大イテレーション数
- `set_use_isomorphism`: 同型性の使用（0/1）
