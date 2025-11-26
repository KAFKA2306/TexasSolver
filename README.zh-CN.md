# テキサスホールデム/ショートデッキ ソルバー

[![release](https://img.shields.io/github/v/release/bupticybee/TexasSolver?style=flat-square)](https://github.com/bupticybee/TexasSolver/releases)
[![license](https://img.shields.io/github/license/bupticybee/TexasSolver?style=flat-square)](https://github.com/bupticybee/TexasSolver/blob/master/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bupticybee/TexasSolver/blob/console/TexasSolverTechDemo.ipynb)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/TexasSolver/TexasSolver)

README [日本語](README.md) | [中文](README.zh-CN.md)

## プロジェクト概要

オープンソースで極めて効率的なテキサスホールデムおよびショートデッキのソルバーです。詳細は[紹介動画](https://www.bilibili.com/video/BV1sr4y1C7KE)をご覧ください。Windows、MacOS、Linuxに対応しています。

![](imgs/solver_example.gif)

特徴:
- 1～2ベット+オールインのゲームツリーに対する求解速度がpiosolverを上回ります
- Mac、Linux、Windowsプラットフォームに対応
- テキサスホールデムとショートデッキに対応
- 言語間呼び出しに対応し、コンソール呼び出しにも対応
- piosolverと一致した結果
- 最適戦略をJSONファイルとして保存する機能に対応
- [TexasHoldemSolverJava](https://github.com/bupticybee/TexasHoldemSolverJava)のC++版であり、速度は前者の5倍以上、メモリ使用量は前者の1/3未満です

[Google Colabデモ](https://colab.research.google.com/github/bupticybee/TexasSolver/blob/console/TexasSolverTechDemo.ipynb)でこのソルバーを体験できます。

## インストール

お使いのOSに応じて[リリースパッケージ](https://github.com/bupticybee/TexasSolver/releases)から該当するパッケージをダウンロードし、解凍すればインストール完了です。とても簡単です。

## グラフィカルインターフェース版の使用方法

ソルバーをインストールした後、アプリケーションのアイコンをダブルクリック（Windowsでは`TexasSolverGui.exe`、Macでは`TexasSolverGui.app`）して、TexasSolverを実行してください。

## コマンドライン版の使用方法

詳細は[コマンドライン版ドキュメント](https://github.com/bupticybee/TexasSolver/tree/console#usage)をご確認ください。

## piosolverとの速度比較

両者ともspr=10のフロップ局面で計算を行い、結果が一致しています。

|                   | 入力設定                                            | 実行ログ                                                       | スレッド数 | メモリ | 終了精度 | 実行時間 |
| ----------------- | ------------------------------------------------------- | ------------------------------------------------------------------ | ------ | ------ | -------- | -------- |
| piosolver 1.0     | [config_piosolver](benchmark/benchmark_piosolver.txt)   | [log_piosolver](benchmark/benchmark_outputs/piosolver_log.txt)     | 6      | 492Mb  | 0.29%    | 242s     |
| TexasSolver 0.1.0（本ソルバー） | [config_texassolver](benchmark/benchmark_texassolver.txt) | [log_texassolver](benchmark/benchmark_outputs/texassolver_log.txt) | 6      | 1600Mb | 0.275%   | 175s     |

結果の一致を示す画像は[result_compair](benchmark/benchmark_outputs/result_compair.png)をご覧ください。ご覧の通り、両者の結果は非常に近いものとなっています。

# ライセンス

[GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.en.html)

# メール

icybee@yeah.net

# よくある質問

1. 質問: このソルバーは本当に完全無料ですか？
   - 回答: はい、個人ユーザーに対しては、このソルバーは完全にオープンソースで無料です。

2. 質問: このソルバーを他のウェブサイト/WeChatやQQグループにアップロードしたり、友人と共有したりできますか？
   - 回答: いいえ、プロジェクトのアドレスのみを共有できます。プロジェクトのバイナリファイルを直接共有することはできません。本プロジェクトのライセンスはAGPL-V3であり、ソフトウェアのバイナリファイルを直接共有/アップロードすることはオープンソースライセンスに直接違反します。

3. 質問: このソルバーを自分の商用ソフトウェアに統合できますか？
   - 回答: ソフトウェアのバイナリファイルのみを統合する場合は可能ですが、TexasSolverのバイナリファイルを配布することはできません。TexasSolverのソースコードを商用ソフトウェアに統合したい場合、またはソフトウェアがインターネットベースのサービスを提供する場合は、私に連絡して有料の商用ライセンスを取得する必要があります。これは本プロジェクトの主な収益化方法でもあります。

4. 質問: TexasSolverの作成にどのフレームワークを使用しましたか？
   - 回答: グラフィカルインターフェース版の構築にはQT 5.1.0（オープンソース版）を使用しました。コマンドライン版にはMingw + CMakeを使用しました。
