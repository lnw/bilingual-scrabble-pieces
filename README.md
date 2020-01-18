# bilingual-scrabble-pieces

Generate laser cutting templates for cutting scrabble pieces, with the
additional feature, that two languages can be written on the two sides of
pieces.

Add new language files for your own language of choice.

The lines to be cut have a width of 0.001mm, which is required by some Epilog
machines.  Other machines may require different line widths.

To generate pieces in English and Swedish, for instance, say:
```
./scrabble-gen.py --lang1 en --lang2 se
```
