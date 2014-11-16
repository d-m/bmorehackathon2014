from twython import TwythonStreamer
from nltk.corpus import wordnet as wn
from tweetManip import buildHaiku

class HaikuStreamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super( HaikuStreamer, self ).__init__(*args, **kwargs)
        self.newHaiku = buildHaiku()

    def on_success(self, data):
        if data.has_key('text'):
            result = self.newHaiku.newTweet(data['text'])
            if result:
                print(result)
                self.disconnect()
                
            
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()

    def _related_words(self, word):
        synlist = []
        for synset in wn.synsets(word):
            synlist.append(len(synset.lemma_names()))
        first_max = synlist.index(max(synlist))
        return wn.synsets(word)[first_max].lemma_names()

    def get_tweets(self, word):
        wordlist = self._related_words(word)
        wordstring = ', '.join(wordlist)
        self.statuses.filter(track=wordstring)
