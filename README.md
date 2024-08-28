# minesweeper-solver-14
[14 Minesweeper Variants](https://store.steampowered.com/app/1865060/14/) の攻略 solver の作成を目標にしています。

現在対応しているルールはまだ少ないです。 (V, Q, M, C, L)

## 環境準備
[rye](https://rye.astral.sh/guide/installation/) の install をしてください。`rye --version` が動作すれば問題ありません。

その後、

```sh
rye sync --no-dev
```

をしてください。

## 入力データの準備
`src/minesweeper_solver_14/input/case.json` が入力データになります。初期盤面やルールを入力してください。

### 注意点
1. `grid_array` の値は、本プロジェクトでは以下の意味を持ちます。

- `-1`: 未確定の盤面
- `-2`: `?` で確定している盤面
- `正の整数`: 確定している盤面

1. `coffences` は、 `M` ルールの際にかける係数です。白マスの場所に 2 を、黒マスの場所に 1 を入れてください。

1. `all_mines_count` は、地雷の総数を入力してください。

## 用法
`rye run solve` で `src/minesweeper_solver_14/input/case.json` を元に確定した一部の情報が出てきます。

`( r, c ): flag` の形式で出力され、 `r` が行番号、 `c` が列番号、 `flag` が地雷のフラグを意味します。(`1` なら地雷、 `0` なら安全)

`flag` が 0 の場合 `Val: ` という形で入力が求められます。新たにわかったマスの値を入力してください。なお `?` の場合は、`-2` を入力してください。

`Huu...` という文字列が出力された場合は、 solver が確定することができない or 解なしと判断しています。入力データが間違っていないか確認してください。(正しい場合は issue を立ててください)
