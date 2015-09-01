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

$(document).ready(function () {
  $('.create-game-button').on("click", sendCreateGameMessage);
});
