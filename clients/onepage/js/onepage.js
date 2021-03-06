/** The main onepage application handler. */
onepage.Application = function(config) {
    /** Accumulate attackres or blockers. */
    this.attackersOrBlockers_ = [];
    /** The socket that we use to communicate with the server. */
    this.socket_ = new onepage.Socket(config.url);

    /** A lookup cache for game ids. */
    this.gameIdLookup_ = new onepage.GameIdLookup();

    /** A renderer for the game state. */
    this.renderer_ = new onepage.Renderer(this.gameIdLookup);

    /** External callbacks for message handling. */
    this.messageCallbacks_ = {};

    // Set up the socket callbacks
    this.socket_.installCallbacks(this.openCallback_.bind(this),
                                  this.messageCallback_.bind(this));
};


/** Create a new game. */
onepage.Application.prototype.createGame = function() {
    this.socket_.sendMessage({message_type: 0});
};


/** Join an already created game. */
onepage.Application.prototype.joinGame = function(gameId, deck) {
    if (!gameId) {
        console.log("gameId is invalid");
        return;
    }
    this.socket_.sendMessage({message_type: 1,
                              join_message: {game_id: gameId,
                                             client_type: 0,
                                             player_config: {
                                                 deck: deck
                                             }}});
};


/**
 * Start the game that we're connected to.
 */
onepage.Application.prototype.startGame = function() {
    this.socket_.sendMessage({message_type: 2,
                              action_message: {
                                  action_type: 0
                              }});
};


/** Attempt to play a card. */
onepage.Application.prototype.playCard = function(gameId) {
    this.socket_.sendMessage({message_type: 2,
                              action_message: {
                                  action_type: 1,
                                  play: {
                                      card: gameId
                                  }
                              }});
};


/** Pass priority. */
onepage.Application.prototype.passPriority = function() {
    this.socket_.sendMessage({message_type: 2,
                              action_message: {
                                  action_type: 5
                              }});
};


/** Activate a card ability. Right now, will only activate the first ability. */
onepage.Application.prototype.activateAbility = function(gameId) {
    this.socket_.sendMessage({message_type: 2,
                              action_message: {
                                  action_type: 2,
                                  activate_ability: {
                                      card: gameId,
                                      index: 0
                                  }
                              }});
};


/** Populate an attackers or blockers message */
onepage.Application.prototype.addAttackerOrBlocker = function(gameId, target) {
    this.attackersOrBlockers_.push([gameId, target]);
};


/** Send an blockers message. This should already be populated. */
onepage.Application.prototype.declareBlockers = function() {
    // Convert to a proper list.
    var blockers = [];
    for (var i = 0; i < this.attackersOrBlockers_.length; i++) {
        blockers.push({
            blocker: this.attackersOrBlockers_[i][0],
            blocking: this.attackersOrBlockers_[i][1]
        });
    }
    this.socket_.sendMessage({
        message_type: 2,
        action_message: {
            action_type: 4,
            declare_blockers: {
                blockers: blockers
            }
        }
    });
    this.attackersOrBlockers_ = [];
};


/** Send an attackers message. This should already be populated. */
onepage.Application.prototype.declareAttackers = function() {
    // Convert to a proper list.
    var attackers = [];
    for (var i = 0; i < this.attackersOrBlockers_.length; i++) {
        attackers.push({
            attacker: this.attackersOrBlockers_[i][0],
            target: this.attackersOrBlockers_[i][1]
        });
    }
    this.socket_.sendMessage({
        message_type: 2,
        action_message: {
            action_type: 3,
            declare_attackers: {
                attackers: attackers
            }
        }
    });
    this.attackersOrBlockers_ = [];
};

/** Create a deck list out of a string. */
onepage.Application.prototype.stringToDeck = function(string) {
    deck = [];
    for (var i = 0; i < 60; i++) {
        deck.push("Forest");
    }
    deck.push("Norwood Ranger");
    return deck;
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
    switch (message.response_type) {
        case 3: // Error
            this.processError_(message.error_response.message);
            break;
        case 4: // GameStateResponse
            this.proccessGameStateResponse_(message.game_state_response.game_state);
            break;
        default:
            console.log("Encountered unhandled message. Ignoring.");
    }
    // Call any other callbacks
    if (this.messageCallbacks_[message.response_type]) {
        var callbacks = this.messageCallbacks_[message.response_type];
        for (var i = 0; i < callbacks.length; i++) {
            callbacks[i](message);
        }
    }
};


/** Process a game state. This should update the UI accordingly. */
onepage.Application.prototype.proccessGameStateResponse_ = function(gameState) {
    this.gameIdLookup_.setGameObjects(gameState);
    this.renderer_.render(gameState);
};


/** Process an error. Log it to the console and to the actual screen. */
onepage.Application.prototype.processError_ = function(errorMessage) {
    this.renderer_.renderError(errorMessage);
    console.error(errorMessage);
};


// Kick everything off
var app; // Make the app externally accesiable for easy debugging.
$(document).ready(function() {
    app = new onepage.Application({
        url: "http://localhost:8080/",
        renderTo: "game"
    });
    // Hook up the app to the UI
    $("#create-game").click(function() {
        app.createGame();
    });

    $("#start-game").click(function() {
        app.startGame();
    });

    $("#pass-priority").click(function() {
        app.passPriority();
    });

    $("#play-card").click(function() {
        app.playCard(+$("#card-id").val());
    });

    $("#activate-ability").click(function() {
        app.activateAbility(+$("#card-id").val());
    });

    $("#add").click(function() {
        app.addAttackerOrBlocker(+$("#card-id").val(), +$("#card-id2").val());
    });

    $("#block").click(function() {
        app.declareBlockers();
    });

    $("#attack").click(function() {
        app.declareAttackers();
    });

    $("#join-game").click(function() {
        app.joinGame(+$("#join-id").val(),
                     app.stringToDeck($("join-deck").val()));
    });

    // Install callbacks for the app
    app.addMessageCallback(0 /** Create */, function(message) {
        $("#join-id").val(message.create_response.game_id);
    });
});
