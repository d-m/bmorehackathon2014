from twython import TwythonStreamer
from nltk.corpus import wordnet as wn


class HaikuStreamer(TwythonStreamer):

    def on_success(self, data):
        if data.has_key('text'):
            print data['text']

    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()

    def _related_words(self, word):
        synlist = []
        for synset in wn.synsets(word):
            synlist.append(len(synset.lemma_names()))
        first_max = synlist.index(max(synlist))
        return wn.synsets(word)[first_max].lemma_names()
