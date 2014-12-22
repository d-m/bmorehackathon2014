from twython import TwythonStreamer
from nltk.corpus import wordnet as wn
from tweetManip import buildHaiku
import copy

class HaikuStreamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super(HaikuStreamer, self ).__init__(*args, **kwargs)
        self.seasonWordPath = 'testList.txt'
        self.newHaiku = buildHaiku()
        self.keyWord = ''
        
                
    def setWord_GO(self, word):
        self.keyWord = word
        self.get_tweets()   

    def get_tweets(self):
        syns = self._related_words(self.keyWord)
        seasons = open(self.seasonWordPath).read().splitlines()
        ants = self._unrelated_words(self.keyWord)
        wordlist = syns + seasons + ants
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

    def buildManyWords(self, word, synonyms, length):
        if not synonyms:
            finalWords = list(self._unrelated_words(word))
        else:
            finalWords = [word]
        Nlast = 0
        desperation = 0
        while length > Nlast
            tempWords = []
            for currentWord in finalWords:
                tempWords = tempWords + self._related_words(currentWord, desperation)
            if tempWords == list():
                print 'only could find ', len(finalWords), 'words'
                return finalWords        
            print'****TEMP WORDS WERE:', tempWords
            finalWords.extend(tempWords)
            finalWords = list(set(finalWords))
            if Nlast == len(finalWords):
                desperation = desperation + 1
            else:
                Nlast = len(finalWords)


    def _related_words(self, word, groupInd):
        if len(wn.synsets(word)) == 0:
            return word
        synlist = []
        for synset in wn.synsets(word):
            synlist.append(len(synset.lemma_names()))         
        sortInd = [i[0] for i in sorted(enumerate(synlist), key=lambda x:x[1])]
        sortIndIndex = len(sortInd) - groupInd
        if sortIndIndex < 0:
            return list()
        groupInd = sortInd[sortIndIndex]
        outputList = copy.copy(wn.synsets(word)[groupInd].lemma_names())
        return outputList

    def _unrelated_words(self, word):
        synlist_all = []
        for item in self._related_words(word, 0):
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










