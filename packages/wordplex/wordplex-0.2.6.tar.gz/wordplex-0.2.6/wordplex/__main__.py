import argparse

from .wordplex import WordPlex

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--suffix", dest="suffix", default="", help="Suffix")
parser.add_argument("-p", "--prefix", dest="prefix", default="", help="Prefix")
parser.add_argument("-f", "--format", dest="format", default=None, help="Format to use")
parser.add_argument(
    "-w", "--word", dest="word", default=None, help="Generate similar to provided word"
)

config = parser.parse_args()

wp = WordPlex()
wp.set_prefix(config.prefix)
wp.set_suffix(config.suffix)

if config.format is not None:
    wp.set_format(config.format)

if config.word:
    wp.set_format_by_word(config.word)

wp.go(print)
