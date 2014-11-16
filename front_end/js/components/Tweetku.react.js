var React = require('react');
var TweetkuActions = require('../actions/TweetkuActions');

var Tweetku = React.createClass({
    render: function () {
        return (
            <div className="tweetku">
                <div className="haiku">
                    <span className="line">
                        {this.props.tweetku.haiku[0]}
                    </span>
                    <span className="line">
                        {this.props.tweetku.haiku[1]}
                    </span>
                    <span className="line">
                        {this.props.tweetku.haiku[2]}
                    </span>
                </div>
                <div className="author">
                    <span className="handle">
                        {this.props.tweetku.author}
                    </span>
                </div>
            </div>
        );
    }
});

module.exports = Tweetku;
