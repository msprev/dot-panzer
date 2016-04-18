My personal `.panzer` files.

Install to `$HOME/.panzer/` to use them.

Note this useful experience from [fredcallaway](https://github.com/fredcallaway) described here: https://github.com/msprev/dot-panzer/issues/6

> I struggled for a long time trying to generate a pdf with panzer foo.md -o foo.pdf before realizing that the command should be panzer foo.md -o foo.tex. It might be worth including that information somewhere for other wandering souls :)

There are 2 ways to generate a pdf in pandoc/panzer:

1. Quick-and-dirty by passing .pdf as the output extension to pandoc/panzer
2. Writing .tex and using a postflight script to compile to pdf

My .panzer files use (2).


