# LuaLaTeX-ja + jlreq

以前は(u)pLaTeXでPDFを作っていたけど、いまはLuaLaTeXというのが流行っているらしい。
日本語対応していて、LuaLaTeX-jaという。

また文書クラスもjsarticleやjsreportを使っていたけれど、カスタマイズ性の高いjlreqというものも出てきたらしい。

jlreqでLuaLaTeX-jaを使うには、プリアンブルに以下のように記述する。

```tex
\documentclass{jlreq}
\usepackage{luatexja}
```

LuaLaTeXはdviファイルを経由せず直接PDFを生成してくれる。
TeX LiveでインストールしていればLuaLaTeXが含まれているので、コマンドはシンプルに以下のようにすればOK。
ファイル名は適当に読み替えること。

```
lualatex main.tex
```

デフォルトだと日本語に原ノ味フォントというのが使われるので、ヒラギノを使いたい場合はプリアンブルに

```tex
\usepackage[hiragino-pron]{luatexja-preset}
```

を追加する。フォントを自由に変えやすいのもLuaLaTeXの利点らしい。

試しに生成してみたPDFは[ここ](../../sample/tex/lualatex-jlreq.pdf)。改行も問題ない。
