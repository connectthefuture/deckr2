/** The main onepage application handler. */
onepage.Application = function(config) {
    this.socket_ = new onepage.Socket(config.url);

    // Set up the socket callbacks
    this.socket_.installCallbacks(this.openCallback_.bind(this),
                                  this.messageCallback_.bind(this));

    this.messageCallbacks_ = {}
};


/** Create a new game. */
onepage.Application.prototype.createGame = function() {
    this.socket_.sendMessage({message_type: 0});
};


/** Join an already created game. */
onepage.Application.prototype.joinGame = function(gameId) {
    if (!gameId) {
        console.log("gameId is invalid");
        return;
    }
    this.socket_.sendMessage({message_type: 1, join_message: {game_id: gameId, client_type: 0}});
};


/** Add a callback for external functions when messages are processed. */
onepage.Application.prototype.addMessageCallback = function(messageType, callback) {
    if (!this.messageCallbacks_[messageType]) {
        this.messageCallbacks_[messageType] = [];
    }
    this.messageCallbacks_[messageType].push(callback);
};


/** Called when the socket is fully open. */
onepage.Application.prototype.openCallback_ = function(event) {
    console.log("Socket is open, let's go.");
};


/** Process a message from the server. */
onepage.Application.prototype.messageCallback_ = function(message) {
    // Delegate to various other handlers
    // Call any other callbacks
    if (this.messageCallbacks_[message.response_type]) {
        var callbacks = this.messageCallbacks_[message.response_type];
        for (var i = 0; i < callbacks.length; i++) {
            callbacks[i](message);
        }
    }
};

// Kick everything off
var app; // Make the app externally accesiable for easy debugging.
$(document).ready(function() {
    app = new onepage.Application({
        url: "http://localhost:8080/"
    });
    // Hook up the app to the UI
    $("#create-game").click(function() {
        app.createGame();
    });
    $("#join-game").click(function() {
        app.joinGame(+$("#join-id").val());
    });

    // Install callbacks for the app
    app.addMessageCallback(0 /** Create */, function(message) {
        console.log("In here");
        $("#join-id").val(message.create_response.game_id);
    });
});