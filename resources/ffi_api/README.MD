## 使用方法

### C FFI API

Rust、Python、Dartなどのc FFI互換言語を使用してこのライブラリを簡単に呼び出すことができます。

例えば、Windows上でPythonを使用している場合、ライブラリをロードしてAPI関数を呼び出す簡単な方法は以下の通りです:

```python
from ctypes import *
api_library = CDLL('api.dll') # pythonスクリプトをライブラリと同じディレクトリに配置

api_library.api(b"resources/text/commandline_sample_input.txt", b"./resources", b"holdem") # これで動作します
# ソリューションファイルが生成されることを確認してください
```

Linuxユーザーは以下のコマンドを使用してください:

```python
api_library = CDLL('api.so') 
```

MacOSの場合:

```python
api_library = CDLL('api.dylib') 
```

注意: これは単なる例です。より多くの機能と柔軟性を持つTexas Solverが提供するPythonバインディングを使用してください。

求解プロセスが完了すると、`output_result.json`ファイルが生成されます。これには計算された最適戦略が含まれています。

上記で言及した入力ファイル`resources/text/commandline_sample_input.txt`には、ツリー構築と求解プロセスを制御するパラメータが含まれています。典型的なファイルは以下のようになります:

```text
set_pot 50
set_effective_stack 200
set_board Qs,Jh,2h
set_range_ip AA,KK,QQ,JJ,TT,99:0.75,88:0.75,77:0.5,66:0.25,55:0.25,AK,AQs,AQo:0.75,AJs,AJo:0.5,ATs:0.75,A6s:0.25,A5s:0.75,A4s:0.75,A3s:0.5,A2s:0.5,KQs,KQo:0.5,KJs,KTs:0.75,K5s:0.25,K4s:0.25,QJs:0.75,QTs:0.75,Q9s:0.5,JTs:0.75,J9s:0.75,J8s:0.75,T9s:0.75,T8s:0.75,T7s:0.75,98s:0.75,97s:0.75,96s:0.5,87s:0.75,86s:0.5,85s:0.5,76s:0.75,75s:0.5,65s:0.75,64s:0.5,54s:0.75,53s:0.5,43s:0.5
set_range_oop QQ:0.5,JJ:0.75,TT,99,88,77,66,55,44,33,22,AKo:0.25,AQs,AQo:0.75,AJs,AJo:0.75,ATs,ATo:0.75,A9s,A8s,A7s,A6s,A5s,A4s,A3s,A2s,KQ,KJ,KTs,KTo:0.5,K9s,K8s,K7s,K6s,K5s,K4s:0.5,K3s:0.5,K2s:0.5,QJ,QTs,Q9s,Q8s,Q7s,JTs,JTo:0.5,J9s,J8s,T9s,T8s,T7s,98s,97s,96s,87s,86s,76s,75s,65s,64s,54s,53s,43s
set_bet_sizes oop,flop,bet,50
set_bet_sizes oop,flop,raise,60
set_bet_sizes oop,flop,allin
set_bet_sizes ip,flop,bet,50
set_bet_sizes ip,flop,raise,60
set_bet_sizes ip,flop,allin
set_bet_sizes oop,turn,bet,50
set_bet_sizes oop,turn,raise,60
set_bet_sizes oop,turn,allin
set_bet_sizes ip,turn,bet,50
set_bet_sizes ip,turn,raise,60
set_bet_sizes ip,turn,allin
set_bet_sizes oop,river,bet,50
set_bet_sizes oop,river,donk,50
set_bet_sizes oop,river,raise,60,100
set_bet_sizes oop,river,allin
set_bet_sizes ip,river,bet,50
set_bet_sizes ip,river,raise,60,100
set_bet_sizes ip,river,allin
set_allin_threshold 0.67
build_tree
set_thread_num 8
set_accuracy 0.5
set_max_iteration 200
set_print_interval 10
set_use_isomorphism 1
start_solve
set_dump_rounds 2
dump_result output_result.json
```

ファイルを修正して、ゲームツリーの詳細や並列処理などを制御してください。デフォルトでは、入力ファイルにはフロップとターンで1ベット/レイズ+オールイン、リバーで2ベット/レイズ+オールインを使用してゲームツリーを構築するフロップ状況が含まれています。

より詳細な説明については、'resources/ffi_api'フォルダ内の完全なPython実装をご確認ください。

他の言語の実装をご希望の場合は...（GitHubのissueを作成してください？）