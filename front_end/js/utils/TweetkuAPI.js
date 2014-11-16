var TweetkuActions = require('../actions/TweetkuActions');

module.exports = {
    // load canned tweetku
    getTweetku: function() {
        var tweetkus = JSON.parse(localStorage.getItem('tweetkus'));
        var randomIndex = Math.floor(Math.random()*tweetkus.length);
        TweetkuActions.receiveTweetku(tweetkus[randomIndex]);
    }
};
