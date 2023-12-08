# WordPlex

The `WordPlex` class is a Python utility designed to generate and manipulate words. It provides methods 
for handling consonants, vowels, numbers and alphabet.

## Example

```python
    python -m wordplex -f "Porsche-99#"

    Porsche-990
    Porsche-991
    Porsche-992
    Porsche-993
    Porsche-994
    Porsche-995
    Porsche-996
    Porsche-997
    Porsche-998
    Porsche-999
```


## Requirements

- Python `^3.8`

## Installation

```python
pip install wordplex
```

## Usage

```python
from wordplex import WordPlex

# Initialize the class
wordplex = WordPlex()

# Example method usage (adjust according to actual methods)
result = wordplex.generate('CV')
print(result)
```

## Features

- **Consonants and Vowels Handling**: Provides lists of consonants and vowels for various processing needs.

## Contributing

Contributions to the `WordPlex` class are welcome. Please fork the repository, make your changes, and submit a 
pull request for review.

## License

MIT
