/**
 * This file contains a simple renderer for the onepage client.
 */

onepage.Renderer = function(gameIdLookup) {
    this.gameIdLookup_ = gameIdLookup;
};


/** Render an error message. */
onepage.Renderer.prototype.renderError = function(errorMessage) {
    $("#error-message").text(errorMessage);
};


/**
 * The main entry point to the renderer. Takes in a gameState that is a json
 * representation of a GameState proto and renders it to the screen.
 */
onepage.Renderer.prototype.render = function(gameState) {
    // Clear everything
    this.clear_();

    // Render the battle field
    this.renderTurnState_(gameState);
    for(var i = 0; i < gameState.players.length; i++) {
        var player = gameState.players[i];
        // Get all the cards on the battlefield that belong to that player and stick them
        // here. I'm not sure why the battlefield isn't a per player zone (I get that it's
        // actually shared, but I don't think it needs to be.)
        if (gameState.battlefield.cards) {
            player.battlefield = {'cards': gameState.battlefield.cards.filter(function (card) {
                return card.controller == gameState.players[i].game_id;
            })};
        } else {
            player.battlefield = {};
        }

        this.renderPlayer_(player, this.getPlayerName_(player.game_id, gameState));
    }

    this.renderZone_(gameState.stack, "Stack", $("#shared-zones"));
};

/** Render the state of the turn (who's turn it is, current step, phase, etc.) */
onepage.Renderer.prototype.renderTurnState_ = function(gameState) {
    $("#current-phase").text(gameState.current_phase);
    $("#current-step").text(gameState.current_step);
    $("#active-player").text(this.getPlayerName_(gameState.active_player, gameState));
    $("#priority-player").text(this.getPlayerName_(gameState.priority_player, gameState));
};


/** Render a player and their zones. */
onepage.Renderer.prototype.renderPlayer_ = function(player, playerName) {
    var playerDiv = $("<div/>");
    playerDiv.text(playerName + "("+player.game_id+")" + " Life: " + player.life);
    this.renderZone_(player.hand, "Hand", playerDiv);
    this.renderZone_(player.graveyard, "Graveyard", playerDiv);
    this.renderZone_(player.library, "Library", playerDiv);
    this.renderZone_(player.battlefield, "Battlefield", playerDiv);
    this.renderManaPool_(player.mana_pool, playerDiv);
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
    cardSpan.text(card.name+" ("+card.game_id+") " + (card.tapped ? "{T}" : ""));
    parentDiv.append(cardSpan);
};


/** Render a mana pool. */
onepage.Renderer.prototype.renderManaPool_ = function(manaPool, parentDiv) {
    var manaPoolSpan = $("<span/>");
    var text = (
        "W:" + manaPool.white + "," +
        "U:" + manaPool.blue + "," +
        "R:" + manaPool.red + "," +
        "B:" + manaPool.black + "," +
        "G:" + manaPool.green// + "," +
        //"C:" + manaPool.colorless
    );
    manaPoolSpan.text(text);
    parentDiv.append(manaPoolSpan);
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


/** Clear everything that needs to be cleared. */
onepage.Renderer.prototype.clear_ = function() {
    $("#players").html('');
    $("#error-message").html('');
    $("#shared-zones").html('');
};
