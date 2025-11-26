# VRChat Poker GTO Assistant

VRChat内のポーカーゲームでGTO戦略をアドバイスするシンプルなツール。

## Phase 0: 最小動作プロトタイプ （実装済み）

TexasSolverをPythonから実行し、結果を表示します。

### セットアップ

```bash
cd vrchat-poker-gto
pip install -r requirements.txt
```

### 使い方

1. TexasSolverのパスを確認:
```bash
# Linux/Mac
which texassolver

# または、プロジェクトディレクトリ内にTexasSolverがある場合
ls -la ~/projects/TexasSolver/TexasSolver
```

2. スクリプトを実行:
```bash
python solver_wrapper.py
```

3. 結果を確認:
- コンソールに推奨アクションが表示されます
- `last_result.json`に詳細が保存されます

### カスタマイズ

`solver_wrapper.py`の`main()`関数を編集:
```python
result = solve_poker_situation(
    hand="AsKh",      # あなたのハンド
    board="Qs Jh 2h", # ボードカード
    pot=50,           # ポットサイズ
    stack=200,        # スタックサイズ
    iterations=20     # イテレーション数（増やすと精度↑、時間↑）
)
```

## Phase 1以降（今後実装予定）

- Phase 1: 画面キャプチャ + OCR
- Phase 2: VRChat OSC統合
- Phase 3: pamiq-core統合（オプション）

## トラブルシューティング

### TexasSolverが見つからない
```bash
# solver_wrapper.pyで絶対パスを指定
solver_path="/path/to/your/TexasSolver"
```

### タイムアウトエラー
```python
# iterations を減らす（デフォルト20→10）
iterations=10
```

### 出力フォーマットが違う
- `last_result.json`の内容を確認
- TexasSolver のバージョンにより出力形式が異なる場合があります
