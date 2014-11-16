var React = require('react');
var TweetkuStore = require('../stores/TweetkuStore');
var Tweetku = require('./Tweetku.react');

var getTweetkuState = function() {
    return {
        tweetku: TweetkuStore.getTweetku()
    }
}

// main controller view
var TweetkuApp = React.createClass({
    // get initial state
    getInitialState: function() {
        return getTweetkuState();
    },
    // Add change listeners to stores
    componentDidMount: function() {
        TweetkuStore.addChangeListener(this._onChange);
    },
    // Remove change listers from stores
    componentWillUnmount: function() {
        TweetkuStore.removeChangeListener(this._onChange);
    },
    // render child components passing state via props
    render: function() {
        return (
            <div className="tweetku-app">
                <Tweetku tweetku={this.state.tweetku} />
            </div>
        );
    },
    // method to set state based on store changes
    _onChange: function() {
        this.setState(getTweetkuState());
    }
});

module.exports = TweetkuApp;
