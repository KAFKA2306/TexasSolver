# 最小構成機能追加要求ドキュメント (Pamiq × TexasSolver連携)

## 1. 目的 (Purpose)

本機能追加は、VRChat向け自律機械知能フレームワークであるPamiq (P-AMI\<Q\>) の推論パイプラインを活用し、外部の高性能GTOソルバーであるTexasSolverと連携させることで、VRChat内のポーカーワールドにおいて、リアルタイムなGTO (Game Theory Optimal) ベースの戦略アドバイスをユーザーに提供することを目的とする。

## 2. スコープ (Scope)

本機能追加は、pamiq-core統合による完全なVRChatポーカーGTOシステムを構築する。

| 項目 | 定義 |
|---|---|
| 対象ゲーム | VRChat内のテキサスホールデム・ポーカーワールド |
| 対象局面 | 全局面（プリフロップ、フロップ、ターン、リバー） |
| アーキテクチャ | pamiq-core Agent/Environment/Interactionパターン |
| 入力手段 | PC画面キャプチャ（ModularEnvironmentのSensorとして実装） |
| 出力手段 | VRChat OSC経由のアクション実行（Actuatorとして実装） |
| 外部ソルバー | TexasSolver（Modelとして統合） |
| データ収集 | pamiq-core DataBufferによる経験データ収集 |
| 継続学習対応 | Trainer統合の基盤構築（将来拡張） |

## 3. 要求事項 (Requirements)

### 3.1. 機能要求 (Functional Requirements: F-)

本システムが実行すべき機能は以下の通りである。

| ID | 機能詳細 | 備考 |
|---|---|---|
| F-01 | 画像入力 | pamiq-io または同等の機能により、PC画面上のVRChatウィンドウをリアルタイムでキャプチャし、静止画像データとして取得できること。 |
| F-02 | データ抽出 (OCR) | 取得した画像データから、画像認識（OCR）により以下のポーカー状態情報を文字列データとして正確に抽出できること。<br>1. 自分のハンド<br>2. 場札 (Board)<br>3. ポットサイズ<br>4. 有効スタックサイズ |
| F-03 | 推論実行 (Solver呼出) | 抽出した文字列データを引数として、TexasSolver のコンソールモード (CLI) をサブプロセスとして起動し、GTO戦略の計算を要求できること。 |
| F-04 | 結果解析 | TexasSolver の標準出力から返されるテキスト結果をパース（解析）し、「推奨アクション（例: BET / CHECK / FOLD）」と「実行頻度（例: 75%）」のデータを抽出できること。 |
| F-05 | VRChat出力 | 抽出した推奨アクションと実行頻度を、VRChatの OSC (Open Sound Control) 機能を介して、指定のOSCアドレスへリアルタイムで送信できること。 |

### 3.2. 非機能要求 (Non-Functional Requirements: NF-)

本システムが満たすべき品質・性能要件は以下の通りである。

| ID | 要件種別 | 詳細 |
|---|---|---|
| NF-01 | 性能 (リアルタイム性) | 画像キャプチャのトリガー発生から、VRChatへのOSC送信完了までを最大 3.0秒以内で完了させること。 |
| NF-02 | 環境 | Windows 10/11環境において、TexasSolverの実行を含め、安定して動作すること。 |
| NF-03 | 信頼性 (エラー処理) | F-02 (OCR失敗) および F-03 (Solverエラー) 発生時、システムがクラッシュすることなく、エラー状態を示すメッセージ（例: /pamiq/poker/error に "OCR_FAIL"）をVRChat側にフィードバックできること。 |
| NF-04 | セキュリティ | VRChatクライアントのメモリを直接読み取る等の利用規約に反する手法は一切用いないこと。 |

### 3.3. 制約条件 (Constraints: C-)

開発・運用における制約事項は以下の通りである。

| ID | 制約内容 |
|---|---|
| C-01 | TexasSolverのコンソール版 (CLI) が事前にインストールされ、実行可能であること。 |
| C-02 | VRChatがOSC機能を有効化していること。 |
| C-03 | Python 3.11環境で動作すること。 |
| C-04 | pamiq-ioまたは同等の画面キャプチャライブラリが使用可能であること。 |
| C-05 | OCRライブラリ（例: Tesseract、EasyOCR等）が使用可能であること。 |

## 4. システム構成 (System Architecture)

### 4.1. コンポーネント構成

```
┌─────────────────────────────────────────────────────────────┐
│                         VRChat                              │
│                    (ポーカーワールド)                         │
└──────────────────┬──────────────────────────────────────────┘
                   │ OSC (受信)
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                    Pamiq統合モジュール                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ 画像入力     │  │ OCRモジュール │  │ OSC送信モジュール │  │
│  │ (pamiq-io)  │─▶│              │  │                  │  │
│  └─────────────┘  └──────┬───────┘  └──▲───────────────┘  │
│                           │             │                   │
│                           ▼             │                   │
│                  ┌─────────────────┐    │                   │
│                  │ Solver呼出      │────┘                   │
│                  │ モジュール       │                        │
│                  └────────┬────────┘                        │
└───────────────────────────┼─────────────────────────────────┘
                            │ サブプロセス起動
                            ▼
                  ┌─────────────────┐
                  │  TexasSolver    │
                  │  (コンソール版)  │
                  └─────────────────┘
```

### 4.2. データフロー

```
1. 画像キャプチャ (pamiq-io)
   ↓
2. OCR処理
   - ハンド抽出: "As Kh"
   - ボード抽出: "Qs Jh 2h"
   - ポット抽出: "50"
   - スタック抽出: "200"
   ↓
3. TexasSolver入力ファイル生成
   set_pot 50
   set_effective_stack 200
   set_board Qs,Jh,2h
   set_range_ip [レンジ定義]
   set_range_oop [レンジ定義]
   ...
   ↓
4. TexasSolver実行 (サブプロセス)
   $ texassolver --config input.txt
   ↓
5. JSON結果パース
   {
     "strategy": {
       "bet": 0.6,
       "check": 0.3,
       "fold": 0.1
     }
   }
   ↓
6. OSC送信
   /chatbox/input "推奨: Bet 60%, Check 30%, Fold 10%"
```

## 5. 実装ガイドライン (Implementation Guidelines)

### 5.1. ディレクトリ構造

```
pamiq-poker-gto/
├── src/
│   ├── capture/          # 画像キャプチャモジュール
│   │   └── screen_capture.py
│   ├── ocr/              # OCRモジュール
│   │   ├── card_recognizer.py
│   │   └── text_extractor.py
│   ├── solver/           # Solver呼出モジュール
│   │   ├── texassolver_wrapper.py
│   │   └── config_generator.py
│   ├── osc/              # OSC送信モジュール
│   │   └── vrchat_osc.py
│   └── main.py           # メインエントリーポイント
├── config/
│   ├── ocr_regions.yaml  # OCR領域設定
│   └── solver_defaults.yaml
├── tests/
│   ├── test_ocr.py
│   ├── test_solver.py
│   └── test_osc.py
└── README.md
```

### 5.2. 主要モジュールの仕様

#### 5.2.1. 画像キャプチャモジュール

```python
class ScreenCapture:
    """VRChatウィンドウをキャプチャ"""
    
    def capture_window(self, window_title: str = "VRChat") -> np.ndarray:
        """
        指定されたウィンドウをキャプチャ
        
        Args:
            window_title: キャプチャ対象のウィンドウタイトル
            
        Returns:
            キャプチャされた画像 (numpy配列)
        """
        pass
```

#### 5.2.2. OCRモジュール

```python
class CardRecognizer:
    """カード認識"""
    
    def recognize_hand(self, image: np.ndarray, region: dict) -> str:
        """
        自分のハンドを認識
        
        Args:
            image: キャプチャ画像
            region: 認識領域 {x, y, width, height}
            
        Returns:
            カード文字列 (例: "As Kh")
        """
        pass
    
    def recognize_board(self, image: np.ndarray, region: dict) -> str:
        """
        場札を認識
        
        Returns:
            ボードカード文字列 (例: "Qs Jh 2h")
        """
        pass
```

#### 5.2.3. Solver呼出モジュール

```python
class TexasSolverWrapper:
    """TexasSolver CLI ラッパー"""
    
    def __init__(self, solver_path: str):
        """
        Args:
            solver_path: TexasSolverの実行ファイルパス
        """
        self.solver_path = solver_path
    
    def solve(self, 
              hand: str,
              board: str,
              pot: float,
              stack: float) -> dict:
        """
        GTO戦略を計算
        
        Args:
            hand: 自分のハンド
            board: ボードカード
            pot: ポットサイズ
            stack: 有効スタック
            
        Returns:
            戦略辞書 {"bet": 0.6, "check": 0.3, ...}
        """
        # 1. 設定ファイル生成
        config = self._generate_config(hand, board, pot, stack)
        
        # 2. サブプロセス実行
        result = subprocess.run(
            [self.solver_path, "--config", config],
            capture_output=True,
            timeout=10
        )
        
        # 3. JSON解析
        return json.loads(result.stdout)
```

#### 5.2.4. OSC送信モジュール

```python
class VRChatOSC:
    """VRChat OSC通信"""
    
    def __init__(self, ip: str = "127.0.0.1", port: int = 9000):
        self.client = SimpleUDPClient(ip, port)
    
    def send_advice(self, strategy: dict):
        """
        推奨アクションを送信
        
        Args:
            strategy: 戦略辞書
        """
        # 最も確率の高いアクションを取得
        best_action = max(strategy.items(), key=lambda x: x[1])
        
        # チャットボックスに送信
        message = f"推奨: {best_action[0]} {best_action[1]*100:.0f}%"
        self.client.send_message("/chatbox/input", message)
```

### 5.3. メインループ

```python
def main():
    """メインループ"""
    capture = ScreenCapture()
    recognizer = CardRecognizer()
    solver = TexasSolverWrapper("path/to/texassolver")
    osc = VRChatOSC()
    
    while True:
        try:
            # 1. 画像キャプチャ
            image = capture.capture_window()
            
            # 2. OCR
            hand = recognizer.recognize_hand(image, region_hand)
            board = recognizer.recognize_board(image, region_board)
            pot = recognizer.recognize_pot(image, region_pot)
            stack = recognizer.recognize_stack(image, region_stack)
            
            # 3. Solver実行
            strategy = solver.solve(hand, board, pot, stack)
            
            # 4. OSC送信
            osc.send_advice(strategy)
            
            # 5. 待機
            time.sleep(5)
            
        except Exception as e:
            logging.error(f"エラー: {e}")
            continue
```

## 6. テスト計画 (Test Plan)

### 6.1. 単体テスト

| モジュール | テストケース |
|---|---|
| OCR | 各種カード組み合わせの認識精度テスト |
| Solver呼出 | 正常系・異常系の動作確認 |
| OSC送信 | メッセージ送信の確認 |

### 6.2. 統合テスト

- End-to-Endでの動作確認
- 画像キャプチャからOSC送信までの一連の流れ

### 6.3. 性能テスト

- 応答時間の測定（目標: 10秒以内）
- OCR精度の測定（目標: 95%以上）

## 7. 今後の拡張 (Future Enhancements)

以下の機能は、MVP完成後の拡張として検討する。

1. **プリフロップ対応**: プリフロップの戦略アドバイス
2. **マルチプレイヤー対応**: 3人以上のゲームに対応
3. **リアルタイム学習**: ユーザーの戦略から学習
4. **GUI**: 設定・監視用のGUI追加
5. **統計分析**: プレイ履歴の分析とレポート生成

## 8. 参考資料 (References)

- [TexasSolver GitHub](https://github.com/bupticybee/TexasSolver)
- [VRChat OSC仕様](https://docs.vrchat.com/docs/osc-overview)
- [Pamiq Documentation](※要リンク追加)
