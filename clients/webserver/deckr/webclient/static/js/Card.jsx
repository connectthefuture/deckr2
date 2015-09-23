var CardAction = React.createClass({
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

var CardActionList = React.createClass({
  render: function () {
    var _this = this;
    var actions = this.props.actions.map(function (action) {
      return (
        <CardAction action={action} cardId={_this.props.cardId} />
      );
    });
    var display = this.props.showActions ? 'block' : 'none';
    return (
      <ul className="card-actions" style={{display: display}}>
        {actions}
      </ul>
    );
  }
});

var Card = React.createClass({
  _cardActions: function () {
    if (this.props.zone == "hand") {
      return ["Play"];
    } else {
      return [];
    }
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
