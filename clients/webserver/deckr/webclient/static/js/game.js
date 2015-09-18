function sendJoinGameMessage () {
  var client_type = is_player ? 'PLAYER' : 'SPECTATOR';
  var join_msg = new ClientMessage({
    'message_type': 'JOIN',
    'join_message': new JoinMessage({
      'game_id': game_id, // This variable is set in template: staging.html
      'client_type': client_type
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

function sendPassPriorityMessage () {
  var pass_priority_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'PASS_PRIORITY'
    })
  });

  sendMessage(pass_priority_msg);
}

function handleGameState (message) {
  $('.start-game').hide(); // TODO: Broadcast this to all players
}

$(document).ready(function () {
  sendJoinGameMessage();
  $(".start-game").on('click', sendStartGameMessage);
  $(".pass-priority").on('click', sendPassPriorityMessage);
});
