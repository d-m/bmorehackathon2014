from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
import sys
import re
h_en = Hyphenator('en_US')

class buildHaiku():
    def __init__(self):
        self.finalHaiku = list()
        self.nLines = 0
    def newTweet(self, tweetText):
        tweetObj = checkTweet(tweetText)
        if not tweetObj.qualityControl():
            return list()
        Nsyls = 5 + 2*(self.nLines%2)
        line = tweetObj.checkSylbls(Nsyls)
        if line:
            self.finalHaiku.append(line)
            self.nLines += 1
        if self.nLines == 3:
            return self.finalHaiku
        else:
            return list()


class checkTweet():
    def __init__(self, text = 'Defualt Tweet'):
        self.text = text
        self.textWords = list()
        self.nWords = 0
        self.baseText = self.text

    def qualityControl(self):
        self.replaceHashtag()
        self.remove_at_symbol_first()
        self.remove_urls()
        self.remove_ampersand_words()
        if self.words_no_vowels():
            return False
        return True
    
    def replaceHashtag(self):
        self.text = self.text.replace('#', 'hashtag ')

    def remove_at_symbol_first(self):
        string_split = self.text.split()
        if re.search('@',string_split[0]):
            del string_split[0]
            self.text = ' '.join(string_split)

    def remove_urls(self):
        self.text = self.search_delete('http:', self.text)

    def remove_ampersand_words(self):
        self.text = self.search_delete('&',self.text)

    def words_no_vowels(self):
        string_split = self.text.split()
        for i in range(len(string_split)):
            if re.search("([aeiouy]+)",string_split[i]):
                string_split[i] = True
            else:
                string_split[i] = False
        if False in string_split:
            return True
        else:
            return False

    def search_delete(self, search_term, string_input):
        string = string_input
        while re.search(search_term, string):
            string_split = string.split()
            for i in range(len(string_split)):
                if re.search(search_term,string_split[i]):
                    string_split[i] = 'delete1'
            string = ' '.join(string_split)
        string_split_2 = string.split()
        while 'delete1' in string_split_2:
            string_split_2.remove('delete1')
        return ' '.join(string_split_2)

    def checkSylbls(self, Nsyls):
        self.textWords=self.text.split()
        self.nWords = len(self.textWords)
        return self.confirmSylsCounts(Nsyls)
    
    def confirmSylsCounts(self, Nsyls):
        i = 0
        sylsCount = 0;
        tooHard = False;
        # loop until the end of the word list, we count Nsyls or can't figure out a word
        while i < self.nWords and sylsCount < Nsyls and not tooHard:
            libreSyls = len(h_en.syllables(self.textWords[i]))
            libreSyls = max(libreSyls, 1)
            simplSyls = self.count_syllables(self.textWords[i])
            if libreSyls == simplSyls[0] or libreSyls == simplSyls[1]:
                sylsCount = sylsCount + libreSyls
            elif simplSyls[0] == simplSyls[1]:
                sylsCount = sylsCount + simplSyls[1]
            else: # this tweet is too hard
                tooHard = True
            i += 1
        if (sylsCount == Nsyls) and not tooHard:
            return ' '.join(self.textWords[:i])
        else:
            return list()
            
            
    def count_syllables(self, word):
        vowels = ['a', 'e', 'i', 'o', 'u']

        on_vowel = False
        in_diphthong = False
        minsyl = 0
        maxsyl = 0
        lastchar = None

        word = word.lower()
        for c in word:
            is_vowel = c in vowels

            if on_vowel == None:
                on_vowel = is_vowel

            # y is a special case
            if c == 'y':
                is_vowel = not on_vowel

            if is_vowel:
                if not on_vowel:
                    # We weren't on a vowel before.
                    # Seeing a new vowel bumps the syllable count.
                    minsyl += 1
                    maxsyl += 1
                elif on_vowel and not in_diphthong and c != lastchar:
                    # We were already in a vowel.
                    # Don't increment anything except the max count,
                    # and only do that once per diphthong.
                    in_diphthong = True
                    maxsyl += 1

            on_vowel = is_vowel
            lastchar = c

        # Some special cases:
        if word[-1] == 'e':
            minsyl -= 1
        # if it ended with a consonant followed by y, count that as a syllable.
        if word[-1] == 'y' and not on_vowel:
            maxsyl += 1

        return minsyl, maxsyl