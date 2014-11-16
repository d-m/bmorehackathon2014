from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
import sys
h_en = Hyphenator('en_US')

class buildHaiku():
    def __init__(self):
        self.finalHaiku = list()
        self.nLines = 0
    def newTweet(self, tweetText):
        tweetObj = checkTweet(tweetText)
        if not tweetObj.qualityControl():
            return list()
        tweetObj.findWords()
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

    def qualityControl(self):
        self.replaceHashtag()
        if not self.retweetCheck():
            return False
#         do some more checks
        return True
    
    def replaceHashtag(self):
        self.text = self.text.replace('#', 'hashtag ')

    def retweetCheck(self):
#         check if retweet 
#           if so return false
        return True

    def findWords(self):
        self.textWords=self.text.split()
        self.nWords = len(self.textWords)

    def checkSylbls(self, Nsyls):
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
            return ''
            
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