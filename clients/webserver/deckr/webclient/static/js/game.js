function sendJoinGameMessage () {
  var join_msg = new ClientMessage({
    'message_type': 'JOIN',
    'join_message': new JoinMessage({
      'game_id': game_id, // This variable is set in template: staging.html
      'client_type': 'PLAYER'
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

$(document).ready(function () {
  if (is_joining) {
    sendJoinGameMessage();
  }
  $(".start-game").on('click', sendStartGameMessage);
  $(".pass-priority").on('click', sendPassPriorityMessage);
});
