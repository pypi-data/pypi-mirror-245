# Punjabi Stopwords Library

The `punjabi_stopwords` library is a Python package providing a collection of stopwords in the Punjabi language. Stopwords are words which are filtered out before processing natural language data. They are typically words that are very common in the language and do not contribute much to the meaning of a sentence, especially when performing tasks like text analysis or natural language processing.

## Main Features

The punjabi_stopwords package offers several functionalities, including:
1. Identifying Punjabi stopwords in text.
2. Removing Punjabi stopwords from text.
3. Adding custom stopwords to the existing list.

### Install the Package

You can install punjabi_stopwords directly from PyPI

## Installation

Install `punjabi_stopwords` using pip:

```python
pip install punjabi_stopwords
```
# Usage
Here's how to use the punjabi_stopwords library in your Python projects:

## Check if a word is a stopword

```python
from punjabi_stopwords import is_stopword

word = 'ਇਸ'
print(is_stopword(word))  # Returns: True if the word is a stopword, False otherwise

```
Output
```
True
```
## Remove stopwords from text

```python
from punjabi_stopwords import remove_stopwords

sample_text = 'ਇਹ ਇੱਕ ਉਦਾਹਰਣ ਵਾਕ ਹੈ।'
filtered_text = remove_stopwords(sample_text)
print(filtered_text)
```
Output
```
ਉਦਾਹਰਣ ਵਾਕ
```
## Add additional stopwords

```python
from punjabi_stopwords import add_stopwords

additional_stopwords = ['ਨਵਾਂਸਟਾਪਵਰਡ1', 'ਨਵਾਂਸਟਾਪਵਰਡ2']
add_stopwords(additional_stopwords)
```

## Contributing
Contributions to punjabi_stopwords are welcome! If you have suggestions for additional stopwords, or improvements to the existing list, please feel free to contribute.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
