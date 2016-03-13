/** A simple module to look up game objects by their game ID and vice versa. */
onepage.GameIdLookup = function() {
    this.map_ = null;
};


/** Set the game objects. */
onepage.GameIdLookup.prototype.setGameObjects = function(gameState) {
    this.map_ = {};
    // Start with the players
    for (var i = 0; i < gameState.players.length; i++) {
        this.map_[gameState.players[i].game_id] = gameState.players[i];
    }
};


/** Lookup a game object. Returns the game object if avaliable. */
onepage.GameIdLookup.prototype.lookup = function(gameId) {
    return this.map_[gameId];
};
