# bilingual-scrabble-pieces

Generate laser cutting templates for cutting scrabble pieces, with the
additional feature, that two languages can be written on the two sides of
pieces.

Add new language files for your own language of choice.

The lines to be cut have a width of 0.001mm, which is required by some Epilog
machines.  Other machines may require different line widths.

There are hardcoded canvas sizes and material sizes which may need to be
changed in other setups.  Material size is the size of the piece of material
(eg wood) used, while the canvas size is the size of the (digital) canvas that
the laser cutter assumes.

To generate pieces in English and Swedish, for instance, say:
```
./scrabble-gen.py --lang1 en --lang2 se
```

Due to the frames drawn on side 1, it may be advantageous to put the language
with more diacritic symbols on side 2.
