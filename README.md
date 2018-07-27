# glitch-tool

glitch-tool is a simple Python script for messing with files in a few different ways. This tool was created for making glitch art, more specifically doing databending. You can read more about my results in [this blog post](https://tobloef.com/fun/glitch-art). This tool was mostly created for this one-time use and therefore the code quality isn't great. 

## Usage
```
usage: glitch_tool.py [-h] [-i INFILE] [-m MODE] [-o OUTDIR] [-s SEED]
                      [-a AMOUNT] [-c CHANGES] [-b BYTES] [-r REPEAT_WIDTH]
                      [-q] [--output-iterations OUTPUT_ITERATIONS]

Required arguments:
  -i, --infile         Input file
  -m, --mode           File change mode
  -o, --outdir         Output folder
Optional arguments:
  -s, --seed           Seed to use for random
  -a, --amount         Amount of new files to create
  -c, --changes        Amount of random changes. Can be in a range, like 1-10.
  -b, --bytes          Amount of bytes to change each change. Can be in a range, like 1-10.
  -r, --repeat-width   Amount of bytes to repeat. Can be in a range, like 1-10.
  -q, --quiet          Surpress logging
  --output-iterations  How many changes between outputs
```

### Modes
The valid modes are:

* `change` - Change bytes in chunk to random values.
* `reverse` - Reverse order of bytes in chunk.
* `repeat` - Repeat first X bytes (specfied with `--repeat-width`) of chunk throughout the chunk.
* `remove` - Remove the chunk entirely.
* `zero` - Make the chunk all zeroes.
* `insert` - Insert random chunk of data at a random point.
* `replace` - Replace chunk with a chunk of random data.
* `move` - Remove a chunk from one position to another.
