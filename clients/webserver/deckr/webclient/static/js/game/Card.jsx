var React = require('react');
var CardActionList = require('./CardActionList');

module.exports = React.createClass({
  displayName: 'Card',
  _cardActions: function () {
    if (this.props.zone == "hand") {
      return this._handActions();
    } else {
      return this._battlefieldActions();
    }
  },
  _handActions: function () {
    return ["Play"];
  },
  _battlefieldActions: function () {
    return this.props.cardData.abilities;
  },
  _contextMenu: function (e) {
    e.preventDefault();
    this._toggleActions();
  },
  _toggleActions: function () {
    this.setState({show_actions: !this.state.show_actions})
  },
  getInitialState: function () {
    return {show_actions: false};
  },
  render: function () {
    var class_name = "card"
    class_name += this.state.show_actions ? " show-actions" : "";
    return (
      <div className={class_name} onClick={this._toggleActions} onContextMenu={this._contextMenu}>
        <CardActionList actions={this._cardActions()} showActions={this.state.show_actions} cardId={this.props.cardData.game_id} />
        <span className="card-name">{this.props.cardData.name}</span>
      </div>
    );
  }
});
