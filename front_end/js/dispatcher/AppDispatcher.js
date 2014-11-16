var Dispatcher = require('flux').Dispatcher;

var AppDispatcher = new Dispatcher();

// handle dispatch requests
AppDispatcher.handleAction = function(action) {
    this.dispatch({
        source: 'VIEW_ACTION',
        action: action
    });
}

module.exports = AppDispatcher;
