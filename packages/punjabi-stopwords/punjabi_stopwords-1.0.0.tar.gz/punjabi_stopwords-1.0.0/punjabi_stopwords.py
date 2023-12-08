# punjabi_stopwords.py

# List of Punjabi stopwords
STOPWORDS = set([ 'ਇਸ', 'ਵਿਚ', 'ਤਕ', 'ਵੀ', 'ਉੱਤੋਂ', 'ਨਹੀਂ', 'ਭੀ', 'ਵਲੋਂ', 'ਇਹ', 'ਏ', 'ਜਦੋਂ', 'ਕਈ', 'ਤੱਦ', 'ਅੰਦਰ', 'ਉੱਤੇ', 'ਸਾਬੁਤ', 'ਕਦੀ', 'ਨੇਂ', 'ਜੀ', 'ਕਿਸੇ',
                 'ਪੂਰਾ', 'ਨੇ', 'ਹੋਵੇ', 'ਜੇਕਰ', 'ਦੇ', 'ਜੇਹੜਾ', 'ਬਾਅਦ', 'ਸਾਰਾ', 'ਚੋ', 'ਕਦੀ', 'ਸਭ', 'ਤਾਂ', 'ਕੀ', 'ਲਾ', 'ਪੂਰਾ', 'ਨਾਲੇ', 'ਤੋਂ', 'ਹੋਣਾ', 'ਪਾਸੋ', 'ਜਿਹਾ',
                 'ਏਸ', 'ਜਿਨਾ', 'ਕੁਝ', 'ਦੁਆਰਾ', 'ਸਦਾ', 'ਏਥੇ', 'ਬਾਰੇ', 'ਕਦ', 'ਕਦੇ', 'ਹੋਏ', 'ਰਹੇ', 'ਬਣੋ', 'ਦੇਣੀ', 'ਪਿਆ', 'ਹੋਇਆ', 'ਗਈ', 'ਲਗ', 'ਹੁੰਦਾ', 'ਜਾਂਦਾ',
                 'ਵੇਖ', 'ਸੁਣ', 'ਆਈ', 'ਸਕਦੇ', 'ਜਾਵੇ', 'ਕਰਣ', 'ਲਗਾਉਦਾ', 'ਆਵੇ', 'ਕਰੀ', 'ਲਾਇਆ', 'ਰਿਹ', 'ਉਹ', 'ਸਾਂ', 'ਸਭ', 'ਹਨ', 'ਤੂੰ', 'ਸੀ', 'ਹੋ', 'ਤੇਨੂੰ',
                 'ਤੁਸਾ', 'ਹੈਂ', 'ਹੈ', 'ਹੈ।', 'ਆਪਣਾ', 'ਜੇ', 'ਅਤੇ', 'ਜਾਂ', 'ਕੁਲ', 'ਵਗ਼ੈਰਾ', 'ਰੱਖ', 'ਲੱਗ', 'ਗੱਲ', 'ਪੀ', 'ਜਿਸ', 'ਨਾ', 'ਹਣੁ', 'ਜਿਨਾਂ', 'ਨਾਲ', 'ਚਾਹੇ', 'ਕਿਸ',
                 'ਪਿਛੋਂ', 'ਏਧਰ', 'ਨੂੰ', 'ਅਿਜਹੇ', 'ਹੀ', 'ਕੇ', 'ਹੈਂ', 'ਬਹਤੁ', 'ਕਾਫ਼ੀ', 'ਹਣੇ', 'ਲਈ', 'ਕਿ', 'ਮਗਰ', 'ਦਾ', 'ਤਰ੍ਹਾਂ', 'ਫੇਰ', 'ਵੇਲੇ', 'ਓਥੇ', 'ਕਿਤੇ', 'ਇੱਥੇ',
                 'ਜਿਨ੍ਹਾਂਨੂੰ', 'ਜਿਨੂ', 'ਜਦ', 'ਵਾਂਗ', 'ਦੌਰਾਨ', 'ਵਰਗਾ', 'ਕਰਕੇ', 'ਬਿਲਕੁਲ', 'ਐਹੋ', 'ਕੌਣ', 'ਫਿਰ', 'ਤਦ', 'ਕੋਲੋਂ', 'ਕਿੰਨਾ', 'ਜਿਵੇਂ', 'ਹੇਠਾਂ', 'ਸਾਰੇ', 'ਜਿੱਥੇ',
                 'ਕੋਈ', 'ਕੀ', 'ਜੀ', 'ਦੀਆਂ', 'ਚਲਾ', 'ਲੈ', 'ਆਖ', 'ਬਣ', 'ਬਣਾ', 'ਕਰ', 'ਪੈਣ', 'ਕਿਹ', 'ਚਕੇ', 'ਕਿਹਾ', 'ਕਰਵਾਈ', 'ਬਣਾਏ', 'ਕੀਤਾ', 'ਜਾਵਣ', 'ਦੇਖ',
                 'ਆਦੀ', 'ਲਿਆ', 'ਆ', 'ਰਿਹਾ', 'ਗਿਆ', 'ਉਠ', 'ਰਹੀ', 'ਉਸਨੇ', 'ਤੁਸੀ', 'ਮੇਰਾ', 'ਉਸਦੀ', 'ਤੇਰਾ', 'ਉਸ', 'ਉਏ', 'ਆਪ', 'ਸਨ', 'ਮੈਂ', 'ਤੁਸੀ', 'ਅੱਸੀ',
                 'ਪਰ', 'ਤੇ', 'ਤਾਂ', 'ਭਾਵੇਂ', 'ਅਗਲੀ', 'ਵਰਗ', 'ਆਮ', 'ਲਾ', 'ਹਾਲ', 'ਇੱਕ' ])

def is_stopword(word):
    """
    Check if a word is a Punjabi stopword.
    
    Args:
        word (str): A word to check.
    
    Returns:
        bool: True if the word is a stopword, False otherwise.
    """
    return word in STOPWORDS

def add_stopwords(words):
    """
    Add additional stopwords to the existing list.
    
    Args:
        words (list): A list of words to add to the stopword list.
    """
    global STOPWORDS
    if isinstance(words, list):
        STOPWORDS.update(words)
    else:
        raise ValueError("Words to add must be in a list.")

def remove_stopwords(text):
    """
    Remove stopwords from a given text.
    
    Args:
        text (str): The text to process.
    
    Returns:
        str: The text with stopwords removed.
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    
    words = text.split()
    filtered_words = [word for word in words if not is_stopword(word)]
    return ' '.join(filtered_words)
