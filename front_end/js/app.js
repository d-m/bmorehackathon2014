var React = require('React');
var TweetkuData = require('./TweetkuData');
var TweetkuAPI = require('./utils/TweetkuAPI');
var TweetkuApp = require('./components/TweetkuApp.react');

// load mock data
TweetkuData.init();

// make mock api call
TweetkuAPI.getTweetku();
setInterval(TweetkuAPI.getTweetku, 5000);

// render controller view
React.render(
    <TweetkuApp />,
    document.getElementById('tweetku')
);
