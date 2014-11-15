from twython import TwythonStreamer


class HaikuStreamer(TwythonStreamer):
    
    def on_success(self, data):
        if data.has_key('text'):
            print data['text']

    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()
