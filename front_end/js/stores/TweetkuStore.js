var AppDispatcher = require('../dispatcher/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var TweetkuConstants = require('../constants/TweetkuConstants');
var merge = require('react/lib/merge');

_tweetku = {}

// load canned data
function loadTweetku(data) {
    console.log(data);
    _tweetku = data[0];
}

var TweetkuStore = merge(EventEmitter.prototype, {
    getTweetku: function() {
        return _tweetku;
    },
    // Emit Change event
    emitChange: function() {
        this.emit('change');
    },

    // Add change listener
    addChangeListener: function(callback) {
        this.on('change', callback);
    },

    // Remove change listener
    removeChangeListener: function(callback) {
        this.removeListener('change', callback);
    }
});

// Register callback with AppDispatcher
AppDispatcher.register(function(payload) {
    var action = payload.action;
    var text;

    switch(action.actionType) {

        // Respond to RECEIVE_DATA action
        case TweetkuConstants.RECEIVE_DATA:
            loadTweetku(action.data);
        break;

      default:
        return true;
    }

    // If action was responded to, emit change event
    TweetkuStore.emitChange();

    return true;
});

module.exports = TweetkuStore;
