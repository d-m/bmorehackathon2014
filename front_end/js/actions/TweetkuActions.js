var AppDispatcher = require('../dispatcher/AppDispatcher');
var TweetkuConstants = require('../constants/TweetkuConstants');

var TweetkuActions = {
    // receive initial tweetku
    receiveTweetku: function(data) {
        console.log(data);
        AppDispatcher.handleAction({
            actionType: TweetkuConstants.RECEIVE_DATA,
            data: data
        });
    }
}

module.exports = TweetkuActions;
