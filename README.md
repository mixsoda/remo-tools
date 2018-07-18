# remo-tools
 Nature remo のためのPythonとシェルスクリプトで書かれたマルチプラットフォームなユーティリティ

![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/sample_figure.png?raw=true "sample")


以下の機能を提供します。
1. Self-hostedなサーバ上でのセンサーデータのロギング
2. ロギングしたセンサーデータの可視化
3. 複雑なルールが設定できるエアコン自動コントローラ

## 動機
### センサーデータのロギング
Nature remoに搭載されている各種センサーデータを定期的にロギングしたい。

### センサーデータの可視化
せっかく、Remoには温湿度計、照度計、人感センサーがついているので、ロギングしてグラフ化したい。

### スマートなエアコン制御
Nature Remoの標準アプリでは複雑なルール設定ができない。
「平日で室温が28度以上なら、17:45にエアコンをつける。ただし、祝日は除く。」
みたいな、きめ細やかなスケジュール設定を行いたい。

## 特徴
ロギングツールはシェルスクリプトで書かれているので（bashさえ動けば）どこででも動く。
例えば、NAS上でも動作可能。

ロギングしたデータをもとにセンサーデータをコマンド一発で可視化できる
Python+Pandas+matplotlibで書かれているので改変も簡単

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

### 可視化ツール
（準備中）

### 制御ツール
（準備中）

## Gallery
可視化結果例
(準備中)

## Links
- [Nature remo](https://nature.global/)
- [Nature remo API documents](https://developer.nature.global/)

## Licence

## 謝辞
以下のライブラリを使用しました
- [parsrj.sh](https://github.com/ShellShoccar-jpn/Parsrs) :: JSONをパースするためのシェルスクリプト
- [holidays-jp](https://github.com/holidays-jp) :: 日本の国民の祝日をJSON形式で返すAPI