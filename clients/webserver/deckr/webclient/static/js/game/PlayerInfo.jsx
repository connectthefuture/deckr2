var React = require('react');
var PlayerGameActions = require('./PlayerGameActions');

module.exports = React.createClass({
  displayName: 'PlayerInfo',
  _hasPriorityAndIsClient: function () {
    return this.props.hasPriority && this.props.isClient;
  },
  _isActivePlayerAndClient: function () {
    return this.props.isActivePlayer && this.props.isClient;
  },
  _renderTurn: function () {
    if (this._isActivePlayerAndClient()) {
      return (
        <span className="turn">It is your turn.</span>
      );
    }
  },
  _renderPriority: function () {
    if (this._hasPriorityAndIsClient()) {
      return (
        <span className="priority">You have priority.</span>
      );
    }
  },
  _renderLibrary: function () {
    var library = this.props.player.library;
    var count = library === undefined ? undefined : library.cards.length;
    return (
      <span className="library">{count}</span>
    );
  },
  _renderGraveyard: function () {
    var graveyard = this.props.player.graveyard;
    var count = graveyard === undefined ? undefined : graveyard.cards.length;
    return (
      <span className="graveyard">{count}</span>
    );
  },
  render: function() {
    var class_name = "player-info";
    class_name += this.props.isClient ? " client" : "";
    return (
      <div className="player-info">
        <h3>Player: {this.props.nick} (id: {this.props.playerId})</h3>
        <PlayerGameActions hasPriority={this._hasPriorityAndIsClient()} />
        <div className="stats">
          <p>Life: <span className="life">{this.props.player.life}</span></p>
          <p>Library: {this._renderLibrary()}</p>
          <p>Graveyard: {this._renderGraveyard()}</p>
        </div>
        <p>{this._renderTurn()}</p>
        <p>{this._renderPriority()}</p>
      </div>
    )
  }
});
