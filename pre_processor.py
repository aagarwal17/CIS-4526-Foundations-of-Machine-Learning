import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
import numpy as np
from utils.wordnet import GetWordnetPos
import string


class Preprocess(object):
    """ preprocess  """
    def __init__(self, sentence):
        self.sentence = sentence

    def get_tokens(self):
        """ return list of tokens"""
        import re
        # Format words and remove unwanted characters
        self.sentence = re.sub(r'https?:\/\/.*[\r\n]*', '', self.sentence, flags=re.MULTILINE)
        self.sentence = re.sub(r'\<a href', ' ', self.sentence)
        self.sentence = re.sub(r'&amp;', '', self.sentence) 
        self.sentence = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', self.sentence)
        self.sentence = re.sub(r'<br />', ' ', self.sentence)
        self.sentence = re.sub(r'\'', ' ', self.sentence)
        
        tokens = word_tokenize(str(self.sentence))
        return tokens
    
    def get_pos_tag(self, tokens):
        """ get pos tag for each word in a sentence"""
        pos1 = pos_tag(tokens)
        #  Lower case the words after POS
        pos1 = [(element[0].lower(),element[1]) for element in pos1]
        return pos1

    def remove_stop_words(self,**kwargs):
        """ remove stopwords"""
        stop_words = stopwords.words('english') + list(string.punctuation)
        final_sentence = []
        pos = kwargs.get("pos")
        tokens = kwargs.get("tokens")
        if pos is None:
            for item in tokens:
                if item not in stop_words:
                    final_sentence.append(item)
        else:
            for item in pos:
                if item[0] not in stop_words:
                    final_sentence.append(item)

        return final_sentence

    def get_lemmaization(self, final_sentence):
        # lemmaization
        lemmatizer = WordNetLemmatizer()
        lemma = []
        for item in final_sentence:
            (word, pos_tag_name) = item
            lemmaizer = GetWordnetPos(pos_tag_name)
            wordnet_tag = lemmaizer.get_wordnet_pos()
            if wordnet_tag is None:
                lemma.append(lemmatizer.lemmatize(word))
            else:
                lemma.append(lemmatizer.lemmatize(word, pos=wordnet_tag))
        return lemma

    def replace_contractions(self, tokens):
        new_tokens = []
        contractions = { "ain't": "am not","aren't": "are not","can't": "cannot","can't've": "cannot have","'cause": "because","could've": "could have","couldn't": "could not","couldn't've": "could not have","didn't": "did not","doesn't": "does not","don't": "do not","hadn't": "had not","hadn't've": "had not have","hasn't": "has not","haven't": "have not","he'd": "he would","he'd've": "he would have","he'll": "he will","he's": "he is","how'd": "how did","how'll": "how will","how's": "how is","i'd": "i would","i'll": "i will","i'm": "i am","i've": "i have","isn't": "is not","it'd": "it would","it'll": "it will","it's": "it is","let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have","mightn't": "might not","must've": "must have","mustn't": "must not","needn't": "need not","oughtn't": "ought not","shan't": "shall not","sha'n't": "shall not","she'd": "she would","she'll": "she will","she's": "she is","should've": "should have","shouldn't": "should not","that'd": "that would","that's": "that is","there'd": "there had","there's": "there is","they'd": "they would","they'll": "they will","they're": "they are","they've": "they have","wasn't": "was not","we'd": "we would","we'll": "we will","we're": "we are","we've": "we have","weren't": "were not","what'll": "what will","what're": "what are","what's": "what is","what've": "what have","where'd": "where did","where's": "where is","who'll": "who will","who's": "who is","won't": "will not","wouldn't": "would not","you'd": "you would","you'll": "you will","you're": "you are"}
        for word in tokens:
            if word in contractions:
                new_tokens.append(contractions[word])
            else:
                new_tokens.append(word)
        return new_tokens
    
    def preprocess_without_lemma(self):
        # tokenization
        tokens = self.get_tokens()

        # remove_stop_words
        tokens = dict(tokens=tokens)
        final_sentence = self.remove_stop_words(**tokens)
        final_sentence2 = self.replace_contractions(final_sentence)
        return final_sentence2

    def preprocess_with_lemma(self):
        # tokenization
        tokens = self.get_tokens()
        # pos tags
        pos1 = self.get_pos_tag(tokens)
        # remove_stop_words
        pos = dict(pos=pos1)
        final_sentence = self.remove_stop_words(**pos)
        final_sentence2 = self.replace_contractions(final_sentence)

        res_lemma = self.get_lemmaization(final_sentence2)

        return res_lemma