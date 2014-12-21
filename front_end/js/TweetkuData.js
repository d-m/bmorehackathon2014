module.exports = {
    // mock haiku data
    init: function() {
        localStorage.clear();
        localStorage.setItem('tweetkus', JSON.stringify([
            {
                "haiku": [
                    "The moon so pure",
                    "a wandering monk carries it",
                    "across the sand."
                ],
                "author": "@The_IrishHammer"
            }
        ]));
    }
}
