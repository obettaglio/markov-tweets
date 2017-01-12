from random import choice
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and returns
    the file's contents as one string of text.
    """

    open_file = open(file_path)
    text_string = open_file.read()
    open_file.close()

    return text_string


def make_chains(text_string, input_n):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}
    words = text_string.split()
    for i in range(len(words) - (input_n - 1)):
        n_gram = tuple(words[i:i+input_n])
        try:
            if n_gram in chains:
                chains[n_gram].append(words[i+input_n])
            else:
                chains[n_gram] = [words[i+input_n]]
        except:
            pass

    return chains


def check_punctuation(rand_key_tuple):
    """Checks for sentence ending punctuation in a tuple of words"""

    end_punctuations = set(['.', '!', '?'])

    tuple_punctuation = rand_key_tuple[-1][-1]
    if tuple_punctuation == '"':
        tuple_punctuation = rand_key_tuple[-1][-2]

    if tuple_punctuation in end_punctuations:
        return False
    else:
        return True


def make_text_tweetable(text, text_list):
    """Makes tweetable text from current text string and new text list

    Takes current text string and new text_list
    Returns list of:
        new text string, and
        boolean of whether tweet is complete
    """

    TWEET_NOT_DONE = True

    if text:                            # If text already has characters
        text_list = [""] + text_list    # Add extra space to start of text list

    text_addition = " ".join(text_list)

    # Keep adding sentences until character limit reached
    if len(text + text_addition) <= 140:
        text += text_addition
        text_list = []

    # Else if first sentence longer than character limit
    elif len(text + text_addition) > 140 and text == "":

        #Keep adding words until character limit reached
        for word in text_list:

            if len(text + word) <= 139:     # 139 to account for extra punctuation
                text += word + " "
            else:
                text = text[:-1] + '.'      # Remove final space and add punctuation
                TWEET_NOT_DONE = False      # Set global variable to end sentence creation
                # return [text, TWEET_NOT_DONE]
                break

    # Else tweet has sentence and reaches character limit
    else:
        TWEET_NOT_DONE = False              # Set global variable to end sentence creation

    return [text, TWEET_NOT_DONE]


def make_text(chains):
    """Takes dictionary of markov chains; returns random text of tweet length."""

    # Set global variable for tweet completion
    TWEET_NOT_DONE = True

    text = ""
    text_list = []

    capital_keys = [key for key in chains.keys() if (key[0][0].isupper()
                                                  or key[0][0] == '"')]
    rand_key_tuple = choice(capital_keys)
    text_list.extend(rand_key_tuple)

    # while rand_key_tuple in chains:           # Stop at end of file (hopefully)
    # while check_punctuation(rand_key_tuple):  # Stop at punctuation
    # while len(text_list) < 70:                # Stop at number of words
    while TWEET_NOT_DONE:                       # Stop at tweetable parameters

        rand_value = choice(chains[rand_key_tuple])
        text_list.append(rand_value)

        # Listify key, remove first value, add new value, retuplefy key
        rand_key_list = list(rand_key_tuple)
        del rand_key_list[0]
        rand_key_list.append(rand_value)
        rand_key_tuple = tuple(rand_key_list)

        # If punctuation is found for end of sentence
        if check_punctuation(rand_key_tuple) is False:

            # Make tweetable text and determine if tweet is finished, reset text list
            text, TWEET_NOT_DONE = make_text_tweetable(text, text_list)
            text_list = []

    # text = " ".join(text_list)

    return text


input_path = sys.argv[1]
input_n = int(sys.argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, input_n)

# Produce random text
random_text = make_text(chains)

print random_text
# print len(random_text)
