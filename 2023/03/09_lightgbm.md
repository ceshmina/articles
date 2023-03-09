# LightGBM覚書

たまにLightGBMでサクッと機械学習モデルを作りたいとき、文法を忘れることがあるので使い方のメモ。

先に以下のサンプルで用いるデータを用意しておく。
ボストン住宅価格のデータはいろいろ問題があって使いにくいので、カリフォルニアのを使う。

```python
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

data = fetch_california_housing()

feature_cols = data.feature_names
target_col = data.target_names[0]

df = pd.DataFrame(data.data, columns=data.feature_names) \
    .assign(**{target_col: data.target})

x_train, x_test, y_train, y_test = train_test_split(
    df, data.target, test_size=0.2, random_state=0
)
x_train, x_valid, y_train, y_valid = train_test_split(
    x_train, y_train, test_size=0.2, random_state=0
)
```

今回は簡易的に、適当にtrain・valid・testの3つにデータセットを分割している。

LightGBMには大きくTraining APIとscikit-learn APIの2つの使い方がある。
基本的にはTraining APIの方を使えばよさそう。
ただし、scikit-learnと組み合わせて使いたいときは、インターフェースが揃っているscikit-learn APIを使う必要がある。

以下でそれぞれのシンプルな使い方を紹介する。

## Training API

先にデータセットをLightGBMのオブジェクトにする必要がある。

```python
import lightgbm as lgb

train = lgb.Dataset(x_train, y_train)
valid = lgb.Dataset(x_valid, y_valid, reference=train)
```

Pandasのデータフレームを渡した場合、変数名は自動で入力されるので指定する必要はない。

学習に使うパラメータの大部分は辞書で指定する。
ここで指定したパラメータはあとのtrainメソッドの引数で指定したものより優先されるので、どちらでも設定できるパラメータに関しては注意が必要。

パラメータの説明は[ここ](https://lightgbm.readthedocs.io/en/latest/Parameters.html)にある。
たとえばこんな感じで指定する。ネットの記事だといろいろ指定しているものもあるが、基本的にデフォルトでいい感じになっているのであまり指定しなくてもそれなりに動く。

`num_iterations` はデフォルトの100だと少ないので、増やしておいた方がいい場面が多そう。
`seed` は今回の環境だと指定しても特に結果が変わらなかったが、入れておいた方が無難だと思われる。

```python
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'num_iterations': 1000,  # trainの引数でも指定できる
    'seed': 0
}
```

学習はtrainメソッドで行う。リファレンスは[こちら](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.train.html)。

パラメータで指定している記事もあるが、現在の方法では、early_stoppingの指定は `callbacks` で行う。
`callbacks` があるとデフォルトのverbosityでは指標 (今回はrmse) の経過が表示されなくなるので、見たい場合は別途 `log_evaluation` で指定を行う。今回だと10ステップ単位で出力するようになっている。

```python
model = lgb.train(
    params, train, valid_sets=[valid], valid_names=['valid'],
    callbacks=[lgb.log_evaluation(10), lgb.early_stopping(50)]
)
```

以下は出力イメージ (一部)

```
...
[LightGBM] [Info] Start training from score 2.065707
Training until validation scores don't improve for 50 rounds
[10]	valid's rmse: 0.719651
[20]	valid's rmse: 0.592514
[30]	valid's rmse: 0.534944
...
[310]	valid's rmse: 0.461524
Early stopping, best iteration is:
[260]	valid's rmse: 0.460951
```

モデルが返るので、predictメソッドで予測が行える。

```python
from sklearn.metrics import mean_squared_error

y_pred = model.predict(x_test)
np.sqrt(mean_squared_error(y_test, y_pred))  # 0.441
```

## scikit-learn API

scikit-learn APIでは分類用のクラスや回帰用のクラスが分かれている。
今回使う回帰用クラスの説明は[ここ](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html#lightgbm.LGBMRegressor)。

Training APIのparamsの代わりにコンストラクタのパラメータを、trainの代わりにfitメソッドを使う。

上記と同じ内容で学習するとたとえば以下のようになる。

```python
model2 = lgb.LGBMRegressor(
    n_estimators=1000, random_state=0
).fit(
    x_train, y_train, eval_set=[(x_valid, y_valid)], eval_names=['valid'],
    eval_metric='rmse',
    callbacks=[lgb.log_evaluation(10), lgb.early_stopping(50)]
)
```

一部のパラメータ名が違うので注意 (いろいろエイリアスがあるので、同じにできる部分もある)。
また、callbacksの指定方法は同じになっている。

上記だけでは変数が用意されておらず、指定できないパラメータがある。
その場合は `set_params` メソッドを使うとできそう。

学習の様子は少し違う。デフォルト指標のl2が併記されている。

```
Training until validation scores don't improve for 50 rounds
[10]	valid's rmse: 0.719651	valid's l2: 0.517897
[20]	valid's rmse: 0.592514	valid's l2: 0.351073
[30]	valid's rmse: 0.534944	valid's l2: 0.286165
...
[310]	valid's rmse: 0.461524	valid's l2: 0.213005
Early stopping, best iteration is:
[260]	valid's rmse: 0.460951	valid's l2: 0.212475
```

予測の仕方は同じ。パラメータを揃えているので、結果も同じになった。

```python
y_pred = model2.predict(x_test)
np.sqrt(mean_squared_error(y_test, y_pred))  # 0.441
```
