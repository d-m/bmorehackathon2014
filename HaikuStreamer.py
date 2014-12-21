from twython import TwythonStreamer
from nltk.corpus import wordnet as wn
from tweetManip import buildHaiku
import copy

class HaikuStreamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super( HaikuStreamer, self ).__init__(*args, **kwargs)
        self.newHaiku = buildHaiku()
        self.keyWord = ''
                
    def setWord_GO(self, word):
        self.keyWord = word
        self.get_tweets()   

    def get_tweets(self):
        wordlist = self._related_words(self.keyWord)
        wordlist.append(u'fall')
        wordlist.extend(self._unrelated_words(self.keyWord))
        wordstring = ', '.join(wordlist)
        wordstring = wordstring.replace('_', ' ')
        print('search terms:')
        print(wordstring)
        self.statuses.filter(track=wordstring)

    def on_success(self, data):
        if data.has_key('text'):
            result = self.newHaiku.newTweet(data['text'])
            if result:
                self.disconnect()
                print(result)
                    
    def on_error(self, status_code, data):
        print 'ERROR', status_code, data
        self.disconnect()

    def _related_words(self, word):
        synlist = []
        for synset in wn.synsets(word):
            synlist.append(len(synset.lemma_names()))     
        first_max = synlist.index(max(synlist)) # the  group with the most synonyms
        outputList = copy.copy(wn.synsets(word)[first_max].lemma_names())
        return outputList

    def _unrelated_words(self, word):
        synlist_all = []
        for item in self._related_words(word):
            synlist_all = synlist_all + wn.synsets(item)
        unique = list(set(synlist_all))
        synlist_all2 = []
        for item in unique:
            synlist_all2 = synlist_all2 + item.lemmas()
        antonym_list = []
        for item in synlist_all2:
            antonym_list = antonym_list + item.antonyms()
        antonym_list2 = []
        for item in antonym_list:
            antonym_list2 = antonym_list2 + item.synset().lemma_names()
        if antonym_list2:
            return antonym_list2
        else:
            return self._related_words(word)










