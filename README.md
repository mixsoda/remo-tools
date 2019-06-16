# remo-tools
 グラフマニアかつ自動化マニアでNature remoユーザな人のためのユーティリティ

![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/visualize_sensor_data_all.png?raw=true "sample")


以下の機能を提供します。
1. 各種センサーデータ（温度、湿度、照度）のロギング
2. ロギングしたセンサーデータのグラフ化
3. 複雑なルールが設定できるエアコン自動コントローラ

## 動機
### センサーデータのロギングとグラフ化
Nature remoに搭載されている各種センサーデータを定期的にロギングしてグラフ化したい。

### スマートなエアコン制御
Nature Remoの標準アプリでは複雑なルール設定ができない。
「平日で室温が28度以上なら、17:45にエアコンをつける。ただし、祝日は除く。」
みたいな、きめ細やかなスケジュール設定を行いたい。

### 花粉の飛散量が多い日は空気清浄機を起動
花粉の飛散量が多い日に自動で空気清浄機を起動したい

## 特徴
### マルチプラットフォーム
ロギングツールはシェルスクリプトで書かれているので（bashさえ動けば）どこででも動く。
例えば、NAS上でも動作可能。(QNAPのNASで動作検証済み)

### Python製グラフ化ツール
ロギングしたデータをもとにセンサーデータをコマンド一発で可視化できる
Python+Pandas+matplotlibで書かれているので改変も簡単

### 日本の祝日に対応したルールベースのエアコン制御ツール
テキストファイルにルールを記載するだけで、Remo標準アプリより柔軟なエアコン制御が可能

## インストール方法 / 使用方法
### 前提
別途APIキーを取得しておいてください。

### ロギングツールのインストール
1. サーバ上にインストール用のディレクトリ（例えば/path/to/remo-tools/)を作成する。
2. ダウンロードしたファイルの中のlogging, lib, utilsディレクトリをコピー
3. logging/*.sh, lib/*.shに実行権限付与
4. logging/ディレクトリの直下にlogs/ディレクトリを作成
5. logging/getRemoSensorData.shをcronに登録
（例：*/15 * * * * /path/to/remo-tool/logging/getRemoSensorData.sh）

/path/to/remo-tool/logging/logs以下にNatureRemoのセンサーから取得したデータが記録される。

### 可視化ツール
ツールは全部visualizeディレクトリに入っている。まず、
/path/to/remo-tool/logging/logs/ディレクトリにある
- temp.txt
- hu.txt
- il.txt
- aircon_state.txt

をvisualizeディレクトリにコピーする。

Remoのセンサーで取得されたデータを可視化するには、
```sh
python remo_graph.py
```
もしくは
```sh
python remo_graph_simple.py
```

を実行する。

エアコンの使用時間をグラフ化するには、
```sh
python aircon_usage_graph.py
```
を実行する。具体的にどんなグラフが作成されるかは、下の「Gallery」を参照。


### 制御ツール
#### エアコン
（準備中）

#### 空気清浄機
環境省の花粉飛散量予測システムの情報を定期的に自動取得し、花粉の飛散量が多い日は自動的に空気清浄機を起動する。
以下のブログエントリに仕組みと使用方法を書いた。

[Nature Remoで花粉が多い日に空気清浄機が自動起動するようにする](https://zlog.hateblo.jp/entry/2019/03/19/nature-remo-aircleaner)

## Gallery
可視化結果例
記録された温度、湿度、照度計のすべてのデータをグラフ化した結果。

![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/visualize_sensor_data_all.png?raw=true "sample")

実線は平均値で、最低値と最大値の間を半透明の帯で表示している。

直近一週間分だけ拡大してグラフ化した結果。

![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/visualize_sensor_data_week.png?raw=true "sample")

エアコン使用時間の変化（一週間の積算使用時間）。下のグラフが気温。

![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/air-con_optime.png?raw=true "sample")

全期間分表示しているグラフは、一週間分のデータを平均しスムージングしているので、センサーデータが最低数カ月分無いとよくわからないグラフになるかもしれない。

## Links
- [Nature remo](https://nature.global/)
- [Nature remo API documents](https://developer.nature.global/)
- [Nature Remoのセンサーデータをひたすら１年間記録した結果をグラフ化してみる](https://zlog.hateblo.jp/entry/2018/11/08/200000)
- [Nature Remoで花粉が多い日に空気清浄機が自動起動するようにする](https://zlog.hateblo.jp/entry/2019/03/19/nature-remo-aircleaner)

## License
These codes are licensed under CC0.
[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

## 謝辞
以下のライブラリを使用しました
- [parsrj.sh](https://github.com/ShellShoccar-jpn/Parsrs) :: JSONをパースするためのシェルスクリプト
- [holidays-jp](https://github.com/holidays-jp) :: 日本の国民の祝日をJSON形式で返すAPI