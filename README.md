# CPP Texas Solver

[![release](https://img.shields.io/github/v/release/bupticybee/TexasSolver?style=flat-square)](https://github.com/bupticybee/TexasSolver/releases)
[![license](https://img.shields.io/github/license/bupticybee/TexasSolver?style=flat-square)](https://github.com/bupticybee/TexasSolver/blob/master/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bupticybee/TexasSolver/blob/console/TexasSolverTechDemo.ipynb)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/TexasSolver/TexasSolver)

README [日本語](README.md) | [中文](README.zh-CN.md)

## はじめに

オープンソースで極めて効率的なテキサスホールデムおよびショートデッキソルバーです。詳細は[紹介動画](https://youtu.be/IsSJNz7sRmQ)をご覧ください。Windows、MacOS、Linuxに対応しています。

![](imgs/solver_example.gif)

特徴:

- 1～2ベット+オールインのツリーにおいて、フロップでの速度がpiosolverを上回ります
- Mac、Linux、Windowsに対応
- テキサスホールデムとショートデッキに対応
- 言語間呼び出しに対応
- piosolverと一致した結果
- 戦略をJSONファイルにダンプする機能に対応
- [TexasHoldemSolverJava](https://github.com/bupticybee/TexasHoldemSolverJava)のC++版であり、大量の最適化により、Javaバージョンの5倍の速度と1/3未満のメモリ使用量を実現しています。

[Google Colab](https://colab.research.google.com/github/bupticybee/TexasSolver/blob/console/TexasSolverTechDemo.ipynb)でソルバーのデモをお試しいただけます。


## インストール

[リリースパッケージ](https://github.com/bupticybee/TexasSolver/releases)からお使いのOSに応じたパッケージをダウンロードし、解凍すればインストール完了です。とても簡単です。

## GUI版の使用方法

ソルバーをインストールした後、アプリケーションバイナリ（Windowsでは`TexasSolverGui.exe`、MacOSでは`TexasSolverGui.app`）をダブルクリックして、TexasSolverを実行してください。

## コンソール版の使用方法

詳細は[コンソール版ドキュメント](https://github.com/bupticybee/TexasSolver/tree/console#usage)をご確認ください。

## piosolverとの速度ベンチマーク

Piosolverと本TexasSolver（コンソール版）を同じ設定（spr=10、フロップゲーム）で実行し、結果が一致しています。

|                                | 入力設定                                              | ログ                                                          | スレッド数 | メモリ使用量 | 精度 | 収束時間 |
| ------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------ | ------------- | ------------ | -------- | ------------- |
| piosolver 1.0                  | [config_piosolver](benchmark/benchmark_piosolver.txt)     | [log_piosolver](benchmark/benchmark_outputs/piosolver_log.txt) | 6             | 492Mb        | 0.29%    | 242s          |
| TexasSolver 0.1.0（本ソルバー） | [config_texassolver](benchmark/benchmark_texassolver.txt) | [log_texassolver](benchmark/benchmark_outputs/texassolver_log.txt) | 6             | 1600Mb       | 0.275%   | 172s          |

両者の結果の比較画像は[こちら](benchmark/benchmark_outputs/result_compair.png)です。ご覧の通り、結果は非常に近いものとなっています。

# ライセンス

[GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.en.html)

本ソフトウェアは以下の個人/企業にライセンスされています: 
[licensed_list](licensed_list.txt)

# メール

icybee@yeah.net

# よくある質問

1. 質問: このソルバーは本当に無料ですか？
   - 回答: はい、個人ユーザーに対しては、このソルバーは完全にオープンソースで無料です。

2. 質問: 他のウェブサイトやフォーラムにアップロードできますか？友人と共有できますか？
   - 回答: いいえ、このプロジェクトへのリンクのみを他のウェブサイトに掲載できます。バイナリファイルの直接共有は禁止されています。本プロジェクトはAGPL-V3ライセンスの下にあり、これらの行為はライセンスに違反します。

3. 質問: 自分のソフトウェアに統合できますか？
   - 回答: リリースパッケージ（バイナリ）を統合する場合は、可能です。ソルバーのコードを統合したい、またはインターネット経由でサービスを提供したい場合は、商用ライセンスについて私に連絡する必要があります。これは本プロジェクトの主な収益化方法でもあります。

4. 質問: UIの作成にどのフレームワークを使用していますか？
   - 回答: GUI版の構築にはQT 5.1.0（オープンソース版）を使用しています。コンソール版にはMingw + CMakeを使用しています。

