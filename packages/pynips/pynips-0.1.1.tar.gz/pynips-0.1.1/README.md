# PyNIPS

PyNIPS is a [Python](https://python.org/) library for reading data from *NIPS 360 FFS* data files.

The **N**ational Military Command System **I**nformation **P**rocessing **S**ystem **360** **F**ormatted **F**ile **S**ystem (NIPS 360 FFS) was a database management system used by the United States of America Military, primarily during the Vietnam War. NIPS 360 FFS runs on the IBM System/360 mainframe computers and is based on the IBM **F**ormatted **F**ile **S**ystem (FFS).

## Installation

```
pip install pynips
```

See also the [Getting and Installing PyNIPS in the online documentation](https://ctrlall.codeberg.page/pynips/install.html).

## Usage

See also the [online documentation](https://ctrlall.codeberg.page/pynips/).

### As Python library

```
import nips


# load the NIPS file
data_set = nips.DataSet('HES.HAMLA.67.NIPS')

for record in data_set.fixed_set:
	print(record)
	
for record in data_set.periodic_sets[0]:
	print(record)
```


### The NIPSEXT command-line utility

A stand-alone command-line utility is provided for:

```
$ nipsext -h

usage: nipsext [-h] [-d] [-v] {info,rec,logical,sqlite,repl} ...

NIPS EXtraction Tool

options:
  -h, --help            show this help message and exit
  -d, --debug           Print debugging statements
  -v, --verbose         Print verbose information

commands:
  {info,rec,logical,sqlite,repl}
    info                Output information about the NIPS file.
    rec                 Output records in the recfiles file format. This is a format usable by the GNU Recutils tools.
    logical             Read and display logical records in a NIPS data file. Useful for debugging physical format.
    sqlite              Export records from NIPS file to an SQLite database.
    repl                Load the NIPS file and start an interactive REPL.

Danger's over, Banana Breakfast is saved.
```

## Development

### Building Documentation

Documentation for PyNIPS is built using [Sphinx](https://www.sphinx-doc.org).

Install Sphinx (`pip install sphinx`) and run:

```
make -C docs/ html
```

to build a HTML rendering of the documentation in `docs/_build_html`.

### Publishing to PyPi

Make sure version is set propertly in [`pyproject.toml`](./pyproject.toml) and [`nips/__init__.py`](./nips/__init__.py).

```
pip install hatch
hatch build
hatch publish
```

## TODOs

- [ ] Handle _continuation records_
- [ ] Handle GeoCoordinate data mode

## License

[AGPL-3.0-or-later](./LICENSES/AGPL-3.0-or-later.txt)
