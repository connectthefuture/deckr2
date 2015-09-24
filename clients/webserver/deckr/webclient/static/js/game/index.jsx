// MESSAGES
function sendJoinGameMessage (game_id, client_type, deck) {
  var join_msg = new ClientMessage({
    'message_type': 'JOIN',
    'join_message': new JoinMessage({
      'game_id': game_id,
      'client_type': client_type
    })
  });
  if (client_type === 'PLAYER') {
    join_msg.join_message.set('player_config', new PlayerConfig({ 'deck': deck }));
  }

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

// MAIN
$(document).ready(function () {
  var React = require('react');
  var Room = require('./Room');
  var vars = PassVars.getVars();

  $(document).on('click', ".start-game", sendStartGameMessage);

  sendJoinGameMessage(vars.game_id, vars.client_type, vars.deck);

  React.render(
    <Room gameId={vars.game_id} gameName={vars.game_name} nick={vars.nick} />,
    document.getElementById('room')
  );
});
