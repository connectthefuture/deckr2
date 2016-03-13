/**
 * This file contains a simple renderer for the onepage client.
 */

onepage.Renderer = function(gameIdLookup) {
    this.gameIdLookup_ = gameIdLookup;
};

/**
 * The main entry point to the renderer. Takes in a gameState that is a json
 * representation of a GameState proto and renders it to the screen.
 */
onepage.Renderer.prototype.render = function(gameState) {
    // Clear everything
    $("#players").html('');
    
    this.renderTurnState_(gameState);
    for(var i = 0; i < gameState.players.length; i++) {
        this.renderPlayer_(gameState.players[i]);
    }
};

/** Render the state of the turn (who's turn it is, current step, phase, etc.) */
onepage.Renderer.prototype.renderTurnState_ = function(gameState) {
    $("#current-phase").text(gameState.current_phase);
    $("#current-step").text(gameState.current_step);
    $("#active-player").text(this.getPlayerName_(gameState.active_player, gameState));
    $("#priority-player").text(this.getPlayerName_(gameState.priority_player, gameState));

};


/** Render a player and their zones. */
onepage.Renderer.prototype.renderPlayer_ = function(player) {
    var playerDiv = $("<div/>");
    this.renderZone_(player.hand, "Hand", playerDiv);
    this.renderZone_(player.graveyard, "Graveyard", playerDiv);
    this.renderZone_(player.library, "Library", playerDiv);
    $("#players").append(playerDiv);
};


/** Render a zone and all of the cards in it. */
onepage.Renderer.prototype.renderZone_ = function(zone, name, parentDiv) {
    var zoneDiv = $("<div/>");
    zoneDiv.text(name + ": ");
    if (zone.cards) {
        for (var i = 0; i < zone.cards.length; i++) {
            this.renderCard_(zone.cards[i], zoneDiv);
        }
    }
    parentDiv.append(zoneDiv);
};


/** Render a single card. */
onepage.Renderer.prototype.renderCard_ = function(card, parentDiv) {
    var cardSpan = $("<span/>");
    cardSpan.text(card.name+" ("+card.game_id+") ");
    parentDiv.append(cardSpan);
};


/** Get a human readable name for a player by game id. */
onepage.Renderer.prototype.getPlayerName_ = function(game_id, gameState) {
    for (var i = 0; i < gameState.players.length; i++) {
        if (gameState.players[i].game_id == game_id) {
            return "Player " + (i+1);
        }
    }
    return "Unknown player";
};
