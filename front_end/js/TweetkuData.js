module.exports = {
    // mock haiku data
    init: function() {
        localStorage.clear();
        localStorage.setItem('tweetkus', JSON.stringify([
            {
                "haiku": [
                    "keep posting pics like",
                    "this and you gon have a new",
                    "father in law bruh"
                ],
                "author": "@Fucklmani"
            },
            {
                "haiku": [
                    "So you lied to me??",
                    "That's why I fucked yo dog and",
                    "boss at the same time!!"
                ],
                "author": "@LESBINAH"
            },
            {
                "haiku": [
                    "here is me and a",
                    "dog. I miss jesse and the",
                    "UK. See you soon"
                ],
                "author": "@blitzedBitchhh"
            },
            {
                "haiku": [
                    "I take a shot of",
                    "I don't care what you're doing",
                    "now. Chase that one bitch"
                ],
                "author": "@The_IrishHammer"
            }
        ]));
    }
}
