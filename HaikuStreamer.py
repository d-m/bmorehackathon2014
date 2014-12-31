from twython import TwythonStreamer
from tweetManip import buildHaiku

class HaikuStreamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super(HaikuStreamer, self ).__init__(*args, **kwargs)
        self.newHaiku = buildHaiku()
        self.haikuFile = 'haikuStore.txt'

    def get_tweets(self, word):
        wordlist = self.newHaiku.setWord(word)
        wordstring = ', '.join(wordlist)
        print('search terms:')
        print(wordstring)
        self.statuses.filter(track=wordstring)

    def on_success(self, data):
        if data.has_key('text'):
            result = self.newHaiku.newTweet(data['text'])
            if result:
                self.disconnect()
                textFile = open(self.haikuFile, "w")
                textFile.write(result)
                textFile.close()
                    
    def on_error(self, status_code, data):
        print 'ERROR', status_code, data
        self.disconnect()



