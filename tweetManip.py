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
        self.seasonWordPath = 'testList.txt'
        self.keyWord = relatedWords()
        self.listLength = 30
        self.Nseven = 0
        self.Nfive = 0
        
    def setWord(self, wordText):
        self.keyWord = relatedWords(wordText)
        syns = self.keyWord.buildWordList(True, self.listLength)
        syns = [w.replace('_', ' ') for w in syns]
        ants = self.keyWord.buildWordList(False, self.listLength)
        ants = [w.replace('_', ' ') for w in ants]        
        seasons = open(self.seasonWordPath).read().splitlines()
        seasons = [w.replace('_', ' ') for w in seasons]
        return syns + ants + seasons
        
    def newTweet(self, tweetText):
        tweetObj = checkTweet(tweetText)
        if not tweetObj.qualityControl()
            return list()
        sevenSyl = tweetObj.checkSylbls(7);
        if sevenSyl # it can have 7 syls
            self.classifyTweet(tweetObj, 7)
            if sevenSylRslt # it is valid, we use it as zeven
                return sevenSylRslt
        fiveSyl = tweetObj.checkSylbls(5);
        if fiveSyl: # check if it works as a five syl line
            return self.classifyTweet(tweetObj, 5)

    def classifyTweet(self, tweetObj, Nsyls):
    #returns empty if tweet catorgy is already filled, otherwise retruns the tweet

            
            

class checkTweet():
    def __init__(self, text = 'Defualt Tweet'):
        self.text = text
        self.h_en = Hyphenator('en_US')

    def qualityControl(self):
        self.replaceText()
        self.remove_at_symbol_first()
        self.remove_symbolWords()
        if self.words_no_vowels():
            return False
        if self.check_forbiddenThings():
            return False
        return True
    
    def replaceText(self):
        self.text = self.text.replace('#', 'hashtag ')

    def remove_at_symbol_first(self):
        string_split = self.text.split()
        if re.search('@',string_split[0]):
            del string_split[0]
            self.text = ' '.join(string_split)

    def remove_symbolWords(self):
        # remove words with badSymbols below
        badSymbols = ['http:', 'https:', '&']
        for s in badSymbols:
            self.text = self.search_delete(s, self.text)
            
        # remove crazy unicode characters   
        self.text = unicode(self.text.encode('ascii','ignore'))
            
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

    def check_forbiddenThings(self):
        forbiddenThings = ['@', # random syms
            ' el ', ' la ', ' en ', ' tu ', # spanish
            ' Et ', ' le ', ' aux ', ' les ', ' de ', ' des ', ' du ', ' il ', ' Elle ',
            ' ses ', ' sa ', ' ces ', ' cela ', ' est ', ' vous ', ' tous ', ' nous ',
            ' allez ', ' alons '] # french
        for s in forbiddenThings:
            if re.search(s, self.text, re.IGNORECASE):
                return True
        return False

    def search_delete(self, search_term, string_input):
        string = string_input
        string_split = string.split()
        while re.search(search_term, string):
            for i in range(len(string_split)):
                if re.search(search_term,string_split[i]):
                    string_split[i] = 'delete1'
            string = ' '.join(string_split)
        string_split_2 = string.split()
        while 'delete1' in string_split_2:
            string_split_2.remove('delete1')
        return ' '.join(string_split_2)

    def checkSylbls(self, Nsyls):
        forbiddenEnds = ['the', 'and', 'a', 'an', 'for', 'at', 'except', 'or']
        finalWords = self.confirmSylsCounts(Nsyls)
        if not finalWords or any(finalWords[-1] == s for s in forbiddenEnds):
            return list()
        return ' '.join(finalWords)               
    
    def confirmSylsCounts(self, Nsyls):
        textWords = self.text.split()
        nWords = len(textWords)
        i = 0
        sylsCount = 0;
        tooHard = False;
        # loop until the end of the word list, we count Nsyls or can't figure out a word
        while i < nWords and sylsCount < Nsyls and not tooHard:
            if len(textWords[i]) >= 100: #hyphenator will break and something is crazy
                return list()
            libreSyls = len(self.h_en.syllables(textWords[i]))
            libreSyls = max(libreSyls, 1)
            simplSyls = self.count_syllables(textWords[i])
            if libreSyls == simplSyls[0] or libreSyls == simplSyls[1]:
                sylsCount = sylsCount + libreSyls
            elif simplSyls[0] == simplSyls[1]:
                sylsCount = sylsCount + simplSyls[1]
            else: # this tweet is too hard
                tooHard = True
            i += 1
        if (sylsCount == Nsyls) and not tooHard:
            return textWords[:i]
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
                if desperation > 5:
                    print '5 recursions only yeilded: ', len(thisTry), ' words!'
                    break
            else:
                Ntries = Ntries + 1
            thisTry = self.related_words(finalWord, 0, desperation)
        return thisTry
        
    def related_words(self, word, curDepth, targetDepth):
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
                finalList = finalList + self.related_words(curWord, curDepth+1, targetDepth)
            return list(set(finalList))

    def _unrelated_word(self, word):
        synlist_all = []
        for item in self.related_words(word, 0, 0):
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

