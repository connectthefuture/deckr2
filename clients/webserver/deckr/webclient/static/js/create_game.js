function sendCreateGameMessage () {
  var variant = $('input[name="variant"]').val();
  var max_players = parseInt($('input[name="max_players"]').val());
  var create_msg = new ClientMessage({
    'message_type': 'CREATE',
    'create_message': new CreateMessage({
      'variant': variant,
      'max_players': max_players
    })
  });

  sendMessage(create_msg);
}

function handleCreate (message) {
  $("input[name='game_id']").val(message.game_id);
  $('#create-game-room').submit();
}

$(document).ready(function () {
  $('.btn.create-game').on("click", sendCreateGameMessage);
  $('#create-game-room input').on('keypress', function () {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') sendCreateGameMessage();
  });
});
