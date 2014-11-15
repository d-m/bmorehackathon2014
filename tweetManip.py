from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
h_en = Hyphenator('en_US')

class checkTweet():
    def __init__(self, text = 'Defualt Tweet', repeats = False):
        self.text = text
        self.repeats = repeats
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
            
        	
		        

	        
        

