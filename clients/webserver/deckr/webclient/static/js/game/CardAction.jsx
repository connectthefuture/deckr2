var React = require('react');

function sendPlayMessage (card_id) {
  var play_card_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'PLAY',
      'play': new PlayAction({
        'card': card_id
      })
    })
  });

  sendMessage(play_card_msg);
}

module.exports = React.createClass({
  displayName: 'CardAction',
  _handleClick: function () {
    if (this.props.action === "Play") {
      sendPlayMessage(this.props.cardId);
    }
  },
  render: function () {
    return (
      <li onClick={this._handleClick}>{this.props.action}</li>
    );
  }
});
