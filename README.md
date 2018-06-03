# remo-tools
シェルスクリプトで書かれた Nature remo のためのユーティリティ群
![sample_images](https://github.com/mixsoda/remo-tools/blob/master/images/sample_figure.png?raw=true "sample")

以下の機能を提供します。
1. Self-hostedなサーバ上でのセンサーデータのロギング
2. ロギングしたセンサーデータの可視化
3. 温度センサーと連動したエアコン自動コントローラ

# 動機
## スマートなエアコン制御
Nature Remoでやりたいことは、「家に帰ってきたときに部屋を適温にしておきたい」なんだけど、
Nature Remo+標準アプリやNature Remo+IFTTTだと、トリガー条件が貧弱でこれがなかなか難しい。

「平日で室温が28度以上なら、17:45にエアコンをつける。ただし、祝日は除く。」

みたいに、2018年6月現在、センサーとの連携やきめ細やかなスケジュール設定をすることができない。

Nature Remoの公式APIを使えば、Remo内蔵のセンサーの値の取得やエアコン制御が可能なので、
人手を介さずエアコンを自動制御したい。

## センサーデータの可視化
せっかく、Remoには温湿度計、照度計、人感センサーがついているので、ロギングしてグラフ化したい。

# 特徴

# インストール方法
準備中

# Links
- [Nature remo](https://nature.global/)
- [Nature remo API documents](https://developer.nature.global/)

# 謝辞
以下のライブラリを使用しました
- parsrj.sh :: JSONをパースするためのシェルスクリプト