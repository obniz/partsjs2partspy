# partsjs2partspy
JS製obnizパーツライブラリをpythonのコードへと変換するプログラム

## usage
1. `js2json.js`を実行する(`node js2json.js`)  
    - `./parts`ディレクトリ以下の`*.js`ファイルを全てJSON形式のAST Treeに変換し，`./partspy`に保存します
    - `./partspy`ディレクトリ以下は`./parts`以下と同じ構成ですが，全てのJSファイルがJSONファイルに置き換えられています
1. `json2py.py`を実行する(`python json2py.py`)
    - 1で生成したJSONファイルを元に，同じ場所に`__init__.py`を生成します
    - `--file`オプションによってファイルパスの一部を指定することでターゲットを絞れます
        - ex) `--file MovementSensor`によって`partspy/MovementSensor`のみを対象とします
        - ex) `--file HC-SR505`によって`partspy/MovementSensor/HC-SR505`のみを対象とします

## note
### 無名関数
無名関数はうまく変換することができません．
```JavaScript
    // JS
    callback = function (position) {
        if (!position)
            return 0;
        return position;
    }
```
同様にアロー関数もうまく変換することができません．
```JavaScript
    // JS
    callback = position => {
        if (!position)
            return 0;
        return position;
    }
```
これらに関しては，事前に関数を定義することで対応可能です．
```python
    # python
    def retpos(position):
        if not position:
            return 0
        return position
    callback = retpos
```

### Promise
Promiseによるブロックはうまく変換することができません．  
asyncioのFutureを使用することで同値の変換を行えます．

## prestring
asyncioに対応するため多少改変した[podhmo/prestring](https://github.com/podhmo/prestring)を用いてpythonへのコード変換を行なっています．  