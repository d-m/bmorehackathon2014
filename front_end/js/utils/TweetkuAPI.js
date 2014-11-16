var TweetkuActions = require('../actions/TweetkuActions');

module.exports = {
    // load canned tweetku
    getTweetku: function() {
        var tweetku = JSON.parse(localStorage.getItem('tweetku'));
        TweetkuActions.receiveTweetku(tweetku);
    }
};
