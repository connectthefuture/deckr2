var React = require('react');

function sendPassPriorityMessage () {
  var pass_priority_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'PASS_PRIORITY'
    })
  });

  sendMessage(pass_priority_msg);
}

module.exports = React.createClass({
  displayName: 'PlayerGameActions',
  _handlePassPriorityClick: function () {
    if (this.props.hasPriority)
      sendPassPriorityMessage();
  },
  _renderPassPriority: function () {
    if (this.props.hasPriority) {
      return (
        <button onClick={this._handlePassPriorityClick} className="pass-priority">
          Pass Priority
        </button>
      );
    }
  },
  render: function () {
    return (
      <div className="game-actions">
        {this._renderPassPriority()}
      </div>
    );
  }
});
