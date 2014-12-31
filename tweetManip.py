from nltk.corpus import wordnet as wn
from random import randint
from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
import sys
import re
import copy

class buildHaiku():
    def __init__(self):
        self.finalHaiku = list()
        self.seasonWordPath = 'winterWords.txt'
        self.keyWord = relatedWords()
        self.listLength = 100
        self.syns = []
        self.ants = []
        self.seasons = []
        self.line1 = []
        self.line2 = []
        self.line3 = []
        self.synsFound = False
        self.antsFound = False
        self.seasonsFound = False

    def setWord(self, wordText):
        self.keyWord = relatedWords(wordText)
        syns = self.keyWord.buildWordList(True, self.listLength)
        self.syns = [w.replace('_', ' ') for w in syns]
        ants = self.keyWord.buildWordList(False, self.listLength)
        self.ants = [w.replace('_', ' ') for w in ants]        
        self.seasons = open(self.seasonWordPath).read().splitlines()
        return self.syns + self.ants + self.seasons

    def newTweet(self, tweetText):
        tweetObj = checkTweet(tweetText)
        print "----checking tweet: ", tweetText.encode('utf-8').strip()
        if not tweetObj.qualityControl():
            print "the tweet did not pass QC"
            return list()
        if not self.classifyTweet(tweetObj.checkSylbls(7), 7):
            self.classifyTweet(tweetObj.checkSylbls(5), 5)
        if self.line1 and self.line2 and self.line3:
            haikuLines = [" ".join(self.line1), " ".join(self.line2), " ".join(self.line3)]
            return "\n".join(haikuLines)
        else:
            return list()    

    def classifyTweet(self, tweetWordList, Nsyls):
        if not tweetWordList:
            return False
        # chech if it is a synonym
        if list(set(self.syns) & set(tweetWordList)) and not self.synsFound:
            if Nsyls == 7 and not self.line2:
                self.line2 = tweetWordList
                self.synsFound = True
            elif Nsyls == 5 and not self.line1:
                self.line1 = tweetWordList
                self.synsFound = True
            elif Nsyls == 5 and not self.line3:
                self.line3 = tweetWordList
                self.synsFound = True
            if self.synsFound:
                print 'this tweet will be the synonym'
                return True
        # chech if it is an antonym
        if list(set(self.ants) & set(tweetWordList)) and not self.antsFound:
            if Nsyls == 7 and not self.line2:
                self.line2 = tweetWordList
                self.antsFound = True
            elif Nsyls == 5 and not self.line3:
                self.line3 = tweetWordList
                self.antsFound = True
            elif Nsyls == 5 and not self.line1:
                self.line1 = tweetWordList
                self.antsFound = True
            if self.antsFound:
                print 'this tweet will be the antonym'
                return True
        # chech if it is an season
        if list(set(self.seasons) & set(tweetWordList)) and not self.seasonsFound:
            if Nsyls == 7 and not self.line2:
                self.line2 = tweetWordList
                self.seasonsFound = True
            elif Nsyls == 5 and not self.line1:
                self.line1 = tweetWordList
                self.seasonsFound = True
            elif Nsyls == 5 and not self.line3:
                self.line3 = tweetWordList
                self.seasonsFound = True
            if self.seasonsFound:
                print 'this tweet will be the season'
                return True
        return False        

class checkTweet():
    def __init__(self, text = 'Defualt Tweet'):
        # only keep latin chars:
        text = re.sub(ur'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', text) 
        self.textWords = text.split()
        self.h_en = Hyphenator('en_US')
        self.badSymbols = ['http:', 'https:', '&']
        self.forbiddenThings = ['@'] # random syms
        self.forbiddenWords = ['el', 'la', 'en', 'tu', # spanish
            'Et', 'le', 'aux', 'les', 'de', 'des', 'du', 'il', 'Elle',
            'ses', 'sa', 'ces', 'cela', 'est', 'vous', 'tous', 'nous',
            'allez', 'alons'] # french
        self.forbiddenEnds = ['the', 'and', 'a', 'an', 'for', 'at', 'except', 'or', 'has',
            'my', 'your', 'their', 'his', 'hers', 'her\'s', 'get', 'it\'ll', 'to']        

    def qualityControl(self):
        self.replaceText()
        self.remove_at_symbol_first()
        self.remove_symbolWords()
        if self.check_forbiddenThings():
            return False
        print "post QC tweet: ", " ".join(self.textWords)
        return True
    
    def replaceText(self):
        self.textWords = [w.replace('#', 'hashtag ') for w in self.textWords]

    def remove_at_symbol_first(self):
        if re.search('RT', self.textWords[0]):
            del self.textWords[0]
        if re.search('@', self.textWords[0]):
            del self.textWords[0]

    def remove_symbolWords(self):
        # remove words with badSymbols and unicode chars
        for i, word in enumerate(self.textWords):
                self.textWords[i] = unicode(word.encode('ascii','ignore'))
                for s in self.badSymbols:
                    if re.search(s, word):
                        del self.textWords[i]
                        break
            
    def words_no_vowels(self, wordList):
        for word in wordList:
            if not re.search("([aeiouyAEIOUY]+)", word):
                print word.encode('ascii','ignore'), ' - did not contain any vowels'
                return True
        return False

    def check_forbiddenThings(self):
        for s in self.forbiddenThings:
            if any([re.search(s, word) for word in self.textWords]):
                print 'the forbidden thing: ', s, ' was found'
                return True
        for s in self.forbiddenWords:
            if any([re.search('^'+s+'$', word, re.IGNORECASE) for word in self.textWords]):
                print 'the forbidden word: ', s, ' was found'
                return True
        return False

    def checkSylbls(self, Nsyls):
        finalWords = self.confirmSylsCounts(Nsyls)
        if not finalWords or self.words_no_vowels(finalWords) \
        or any(finalWords[-1] == s for s in self.forbiddenEnds):
            return list()
        print Nsyls, "syls found... final text: ", finalWords  
        return finalWords               
    
    def confirmSylsCounts(self, Nsyls):
        nWords = len(self.textWords)
        i = 0
        sylsCount = 0;
        tooHard = False;
        # loop until the end of the word list, we count Nsyls or can't figure out a word
        while i < nWords and sylsCount < Nsyls and not tooHard:
            if len(self.textWords[i]) >= 100: #hyphenator will break and something is crazy
                return list()
            libreSyls = len(self.h_en.syllables(self.textWords[i]))
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
            return self.textWords[:i]
        else:
            return list()
            
    def count_syllables(self, word):
        if not word:
            return 0, 0
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

        
class relatedWords():
    def __init__(self, centerWord = 'good'):
        self.centerWord = centerWord
        
    def buildWordList(self, synonyms, length):
        if not synonyms:
            finalWord = self._unrelated_word(self.centerWord)
        else:
            finalWord = self.centerWord
        Nlast = 0
        desperation = 0
        Ntries = 0
        thisTry = []
        while length > len(thisTry):
            if Ntries > desperation:
                desperation = desperation + 1
                Ntries = 1
                if desperation > 10:
                    print '10 recursions only yeilded: ', len(thisTry), ' words!'
                    break
            else:
                Ntries = Ntries + 1
            thisTry = self._related_words(finalWord, 0, desperation)
        return thisTry[:length]
        
    def _related_words(self, word, curDepth, targetDepth):
        Nsynsets = len(wn.synsets(word))
        if Nsynsets == 0:
            return word 
        groupInd = randint(0, Nsynsets -1)
        outputList = copy.copy(wn.synsets(word)[groupInd].lemma_names())
        if curDepth == targetDepth:
            return outputList
        else:
            finalList = []
            for curWord in outputList:
                finalList = finalList + self._related_words(curWord, curDepth+1, targetDepth)
            return list(set(finalList))

    def _unrelated_word(self, word):
        synlist_all = []
        for item in self._related_words(word, 0, 0):
            synlist_all = synlist_all + wn.synsets(item)
        unique = list(set(synlist_all))
        synlist_all2 = []
        for item in unique:
            synlist_all2 = synlist_all2 + item.lemmas()
        antonym_list = []
        for item in synlist_all2:
            antonym_list = antonym_list + item.antonyms()
        antonym_list2 = list()
        for item in antonym_list:
            antonym_list2 = antonym_list2 + item.synset().lemma_names()
        if antonym_list2:
            return antonym_list2[0]
        else:
            return word

