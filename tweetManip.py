from hyphen import Hyphenator, dict_info 
from hyphen.dictools import *
import re
h_en = Hyphenator('en_US')

class checkTweet():
    def __init__(self, text = 'Defualt Tweet', repeats = False):
        self.text = text
        self.repeats = repeats
    def replaceHashtag(self):
        self.text = self.text.replace('#', 'hashtag ')
        print(self.text)
    def findWords(self):
        self.textWords=self.text.split()
        print(a)
    def checkSylbls(self, Nsyls):
        print('syllables are')
        a = [h_en.syllables() for x in self.words]
        print(a)
        self.sybs = h_en.syllables(self.text)
        print(self.sybs)
        print(len(self.sybs))
        
        	
		        

	        
        

