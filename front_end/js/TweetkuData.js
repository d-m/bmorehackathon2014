module.exports = {
    // mock haiku data
    init: function() {
        localStorage.clear();
        localStorage.setItem('tweetku', JSON.stringify([
            {
                "haiku": [
                    "keep posting pics like",
                    "this and you gon have a new",
                    "father in law bruh"
                ],
                "author": "@Fucklmani"
             }
        ]));
    }
}
