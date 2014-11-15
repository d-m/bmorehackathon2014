from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
h_en = Hyphenator('en_US')

class buildHaiku():
    def __init__(self):
        self.finalHaiku = list()
        self.nLines = 0
    def newTweet(self, tweetText):
        tweetObj = checkTweet(tweetText)
        tweetObj.replaceHashtag()
        tweetObj.findWords()
        Nsyls = 5 + 2*(self.nLines%2)
        line = tweetObj.checkSylbls(Nsyls)
        print(line)
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

    def replaceHashtag(self):
        self.text = self.text.replace('#', 'hashtag ')

    def findWords(self):
        self.textWords=self.text.split()
        self.nWords = len(self.textWords)

    def checkSylbls(self, Nsyls):
        i = 0
        sylsCount = 0;
        while i < self.nWords and sylsCount < Nsyls:
            wordSyls = len(h_en.syllables(self.textWords[i]))
            sylsCount = sylsCount + max(wordSyls, 1)
            i += 1
    
        if (sylsCount == Nsyls):
            return ' '.join(self.textWords[:i])
        else:
            return ''