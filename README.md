# peal

A small toolkit for change ringing (English full-circle bell ringing).

Bells are written `1234567890ETABCD...`, rows are permutations of them, and
methods are described in place notation the way the Central Council
method library writes them (`x16x16x16,12`, `&5.1.5.1.5,+125`).

```
python -m peal methods
python -m peal course "Cambridge Surprise Minor"
python -m peal music "Plain Bob Major" --run 4
```

What's there:

- `rows.py` – the `Row` type, composition of permutations, inverse
- `notation.py` – place notation parsing, implied external places, palindromic shorthand
- `methods.py` – leads, lead heads, plain courses and a small built-in library
- `proof.py` – checks a block of rows for repetition
- `music.py` – named rows (queens, tittums...) and runs at front and back

Not done yet: calls (bobs and singles), touches, and proving anything other
than a plain course.

Run the tests with `python -m pytest`.
