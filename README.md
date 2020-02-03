# FT-Compress
The following module demonstrates how to compress and store fastText vectors in order to reduce RAM consumption.

Currently supported two types of compression:
* simple compression (see [DumbCompressor](./ft_compress/compressors/dumb.py), which saves vectors in a special storage
* 8-bit compression (see [Compressor8Bit](./ft_compress/compressors/dumb.py), which saves vectors with 1-byte per component

The module allows not only save the word vectors, but also predict the new one for the unknown words, just like the original fastText.

For the details see [Demo](demo.ipynb) 


# Changelog

* 0.0.1 --- initial commit
* 0.1.0 --- basic compressors
* 0.2.0 --- updated interfaces. Dumb compressor works correctly.
* 0.3.0 --- Compressor8bit was refactored
* 0.4.0 --- Shelve-based storage
* 0.5.0 --- fixed prediction, some refactoring, demo