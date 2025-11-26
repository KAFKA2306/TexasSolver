# Pybind ディレクトリ

## 概要

本ディレクトリには、Pybind11を使用したPythonバインディングの実装が格納されています。PythonからTexasSolverの機能を直接呼び出すことができます。

## 主要機能

### Pythonインターフェース
C++のクラスと関数をPythonから使用可能にします。

**バインドされるクラス:**
- `Card`: カードクラス
- `Deck`: デッキクラス
- `GameTree`: ゲームツリークラス
- `PCfrSolver`: ソルバークラス
- `PrivateCards`: プライベートカードクラス

### 型変換
PythonとC++の型を自動変換します。

**サポートされる型:**
- `list` ↔ `vector`
- `dict` ↔ `map`
- `str` ↔ `string`
- `float` ↔ `double`
- NumPy配列 ↔ `vector`

### エラーハンドリング
C++例外をPython例外に変換します。

## 使用例

### ソルバーの実行

```python
import texassolver

# ゲームツリーの構築
tree = texassolver.GameTree(
    deck=texassolver.Deck.HOLDEM,
    oop_commit=1.0,
    ip_commit=2.0,
    current_round=texassolver.GameRound.FLOP,
    raise_limit=3,
    small_blind=0.5,
    big_blind=1.0,
    stack=100.0,
    settings=settings,
    allin_threshold=0.67
)

# レンジの定義
range1 = texassolver.parse_range("AA,KK,QQ,AKs")
range2 = texassolver.parse_range("88+,A9s+")

# ボードの設定
board = texassolver.parse_board("Qs,Jh,2h")

# ソルバーの作成と実行
solver = texassolver.PCfrSolver(
    tree=tree,
    range1=range1,
    range2=range2,
    initial_board=board,
    iteration_number=1000,
    num_threads=8
)

solver.train()
result = solver.dumps(with_status=True, depth=2)

# 結果の取得
import json
strategy = json.loads(result)
print(strategy)
```

### カード操作

```python
import texassolver

# カードの作成
card1 = texassolver.Card("As")
card2 = texassolver.Card("Kh")

# カードの情報取得
print(card1.get_card())  # "As"
print(card1.get_card_int())  # 整数表現

# ボードカードの変換
board = ["Qs", "Jh", "2h"]
board_long = texassolver.Card.board_cards_to_long(board)
```

## ビルド方法

### 要件
- Python 3.7以上
- Pybind11 2.6以上
- C++17対応コンパイラ

### コンパイル

```bash
# CMakeを使用
mkdir build && cd build
cmake .. -DBUILD_PYTHON_BINDINGS=ON
make

# または setup.py を使用
python setup.py build_ext --inplace
```

### インストール

```bash
pip install .
```

## パフォーマンス

### GIL（Global Interpreter Lock）の解放
長時間実行される計算ではGILを解放:
```cpp
py::gil_scoped_release release;
solver->train();
```

### NumPy統合
効率的なデータ転送のためNumPy配列を直接サポート:
```python
import numpy as np
reach_probs = np.array([0.5, 0.3, 0.2], dtype=np.float32)
```
