[![Build Status](https://travis-ci.org/mkazin/StatementRenamer.svg?branch=master)](https://travis-ci.org/mkazin/StatementRenamer)
[![Code Climate](https://codeclimate.com/github/mkazin/StatementRenamer/badges/gpa.svg)](https://codeclimate.com/github/mkazin/StatementRenamer)
[![Maintainability](https://api.codeclimate.com/v1/badges/6108f9eff61dd586cab2/maintainability)](https://codeclimate.com/github/mkazin/StatementRenamer/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6108f9eff61dd586cab2/test_coverage)](https://codeclimate.com/github/mkazin/StatementRenamer/test_coverage)


# StatementRenamer
Python framework to rename financial statements (or other documents)

# Building
Should be as simple as:
* virtualenv -p \`which python3\` env 
* source env/bin/activate
* pip install -r requirements.txt -r dev-requirements.txt

# Running tests
* pytest

# Contributions welcome
Pull requests for new extractors must include a unit test with stubbed test data (see current extractor unit testing). Use the extract-only flag to pull data out of a couple PDFs, use that to implement the match() and extract() functions then make sure the utility runs on your original PDFs. It should go without saying that you should keep a backup of the original files.

Due to the nature of this project (handling financial documents), I have limited visibility into potential test data and could use help extending the library of extractors.

That said, I will *not* be accepting raw PDF documents.

You can use the *extract-only* mode (see below) to extract text from a PDF document, and then (carefully) remove any sensitive data before submitting it to me via **((TBD secure manner))**. In other words, contact me and will figure out that last part.

## Usage

### Command Line Interface:
```console
(env) mkazin@VirtualBox:~/Work/StatementRenamer$ python statement_renamer -h
usage: statement_renamer [-h] [-E] [-H] [-S] [-v] [-q] location

positional arguments:
  location            File or folder to process

optional arguments:
  -h, --help          show this help message and exit
  -E, --extract-only  Extract-only mode. Returns content of PDF
  -H, --hash-only     Hash-only mode. Returns MD5 hash of input files
  -S, --simulate      Simulation mode. Outputs actions that would be taken
  -v, --verbose       Verbose mode. Outputs detailed information
  -q, --quiet         Quiet mode. Produces no console output
```

### Running in Simulation mode:

Vanguard's download system is really bad. 

```console
(env) mkazin@VirtualBox:~/Work/StatementRenamer$ python statement_renamer -S Input/Vanguard\ Statements/
Processing Files: 55 files [00:13,  3.94 files/s]
Done processing files
SIMULATION Ignore confirmation (13).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (1).pdf (No matching extractor found.)
SIMULATION Ignore confirm (1).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (27).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (12).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (2).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (1)b.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (23).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (6).pdf (No matching extractor found.)
SIMULATION Ignore 2018 Jan Change Plan Fee Disclosure Notice.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (21).pdf (No matching extractor found.)
SIMULATION Ignore statement (4).pdf (No matching extractor found.)
SIMULATION Ignore confirm.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (9).pdf (No matching extractor found.)
SIMULATION Ignore 2017-Q2 Quarterly Statement.pdf (Already named correctly)
SIMULATION Ignore 2017-Q4 Quarterly Statement.pdf (Already named correctly)
SIMULATION Ignore confirmation (10).pdf (No matching extractor found.)
SIMULATION Delete statementB.pdf (Duplicate hash: d87465b7adf08e3cdb26e203c2877173)
SIMULATION Ignore document (1)df.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (26).pdf (No matching extractor found.)
SIMULATION Delete statement (1).pdf (Found duplicate hash (64cd378db60b38a5c9f9d79f937c64d8) shared by [2017-Q3 Quarterly Statement.pdf].)
SIMULATION Ignore document (4)df.pdf (No matching extractor found.)
SIMULATION Ignore document (4).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (3).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (2)b.pdf (No matching extractor found.)
SIMULATION Delete statement (2).pdf (Duplicate hash: 313bbe96f833ae1863f3d95044e10f5c)
SIMULATION Ignore confirmationB.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (3)b.pdf (No matching extractor found.)
SIMULATION Delete statement (3).pdf (Found duplicate hash (25ca43eca67e9230ab684b0da9167157) shared by [2017-Q1 Quarterly Statement.pdf].)
SIMULATION Ignore confirmation (5).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (8).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (7).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (25).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (11).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (20).pdf (No matching extractor found.)
SIMULATION Ignore document (2)df.pdf (No matching extractor found.)
SIMULATION Delete statement.pdf (Duplicate hash: d87465b7adf08e3cdb26e203c2877173)
SIMULATION Ignore confirmation (14).pdf (No matching extractor found.)
SIMULATION Rename statement (5).pdf to 2018-Q1 Quarterly Statement.pdf
SIMULATION Ignore confirmation (24).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (18).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (4).pdf (No matching extractor found.)
SIMULATION Delete 2017-Q1 Quarterly Statement.pdf (Duplicate hash: 25ca43eca67e9230ab684b0da9167157)
SIMULATION Delete 2017-Q3 Quarterly Statement.pdf (Duplicate hash: 64cd378db60b38a5c9f9d79f937c64d8)
SIMULATION Ignore confirmation (17).pdf (No matching extractor found.)
SIMULATION Ignore document (5).pdf (No matching extractor found.)
SIMULATION Ignore confirmation (16).pdf (No matching extractor found.)
SIMULATION Ignore document (3)df.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (19).pdf (No matching extractor found.)
SIMULATION Ignore confirmation.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (4)b.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (15).pdf (No matching extractor found.)
SIMULATION Ignore documentdf.pdf (No matching extractor found.)
SIMULATION Ignore document (5)df.pdf (No matching extractor found.)
SIMULATION Ignore confirmation (22).pdf (No matching extractor found.)
SIMULATED Summary: Ignore: 47, Delete: 7, Rename: 1

(env) mkazin@VirtualBox:~/Work/StatementRenamer$ ls Input/Vanguard\ Statements/ | wc -l
55
```

### Normal renaming (using same input folder as simulation):

```console
(env) mkazin@VirtualBox:~/Work/StatementRenamer$ python statement_renamer Input/Vanguard\ Statements/
Processing Files: 55 files [00:13,  3.95 files/s]
Done processing files
Summary: Rename: 1, Ignore: 47, Delete: 7

(env) mkazin@VirtualBox:~/Work/StatementRenamer$ ls Input/Vanguard\ Statements/ | wc -l
48
```