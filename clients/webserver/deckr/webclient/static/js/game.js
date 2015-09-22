// GLOBALS
var player_id;
var active_player;
var priority_player;
var started = false;

function _60Forests () {
  var deck = [];
  for (var i = 0; i < 60; i++) { deck.push("Forest"); }
  return deck;
}

// MESSAGES
function sendJoinGameMessage () {
  var client_type = is_player ? 'PLAYER' : 'SPECTATOR';
  var join_msg = new ClientMessage({
    'message_type': 'JOIN',
    'join_message': new JoinMessage({
      'game_id': game_id, // This variable is set in template: staging.html
      'client_type': client_type,
      'player_config': new PlayerConfig({
        'deck': _60Forests()
      })
    })
  });

  sendMessageOnceSocketOpens(join_msg);
}

function sendStartGameMessage () {
  var start_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'START'
    })
  });

  sendMessage(start_msg);
}

$(document).ready(function () {
  sendJoinGameMessage();
  $(document).on('click', ".start-game", sendStartGameMessage);
  // $(document).on('click', ".pass-priority", sendPassPriorityMessage);
});
