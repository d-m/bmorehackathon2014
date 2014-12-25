from twython import TwythonStreamer
from tweetManip import buildHaiku, relatedWords

class HaikuStreamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super(HaikuStreamer, self ).__init__(*args, **kwargs)
        self.seasonWordPath = 'testList.txt'
        self.newHaiku = buildHaiku()
        self.keyWord = relatedWords()
        self.listLength = 30
                
    def setWord_GO(self, word):
        self.keyWord = relatedWords(word)
        self.get_tweets()   

    def get_tweets(self):
        syns = self.keyWord.buildWordList(True, self.listLength)
        seasons = open(self.seasonWordPath).read().splitlines()
        ants = self.keyWord.buildWordList(False, self.listLength)
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



