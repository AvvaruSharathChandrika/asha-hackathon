import base64
import nltk
import pandas as pd
from nltk.corpus import stopwords
from string import punctuation

def remove_stopwords(text):
    """Removes stop words from a given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with stop words removed.
    """

    # Download stopwords if not already downloaded
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))-set(["not"])

    # Remove stop words
    words = [word.lower() for word in text.split() if word.lower() not in stop_words]

    return ' '.join(words)


def remove_punctuation(text):
    """Removes punctuation from a given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with punctuation removed.
    """

    # Remove punctuation
    words = [word for word in text.split() if word not in punctuation]

    return ' '.join(words)


def process_query(query):
    """Processes a query by removing stop words and punctuation.

    Args:
        query (str): The input query.

    Returns:
        str: The processed query.
    """

    query = remove_stopwords(query)
    query = remove_punctuation(query)

    query = query.replace("?", "")

    return query

