var React = require('react');
var PlayerInfo = require('./PlayerInfo');

module.exports = React.createClass({
  displayName: 'PlayerInfoList',
  _hasPriority: function (player_id) {
    return this.props.priorityPlayer == player_id;
  },
  _isActivePlayer: function (player_id) {
    return this.props.activePlayer == player_id;
  },
  _isClient: function (player_id) {
    return this.props.clientPlayer == player_id;
  },
  _clientPlayer: function () {
    for (var i = 0; i < this.props.players.length; i++) {
      var player = this.props.players[i];
      if (player.game_id === this.props.clientPlayer) {
        return player;
      }
    }
  },
  _renderNonClientInfoList: function () {
    var _this = this;
    var players = this.props.players.filter(function (player) {
      return !_this._isClient(player.game_id);
    });
    return players.map(function (player) {
      return (
        <PlayerInfo
          player={player}
          playerId={player.game_id}
          isClient={_this._isClient(player.game_id)}
          isActivePlayer={_this._isActivePlayer(player.game_id)}
          hasPriority={_this._hasPriority(player.game_id)} />
      );
    });
  },
  _renderClientInfo: function () {
    var client_player = this._clientPlayer();
    if (client_player) {
      return (
        <PlayerInfo
          nick={this.props.clientNick}
          player={client_player}
          playerId={client_player.game_id}
          isClient={true}
          isActivePlayer={this._isActivePlayer(client_player.game_id)}
          hasPriority={this._hasPriority(client_player.game_id)}
        />
      );
    }
  },
  render: function () {
    return (
      <div className="player-infos">
        {this._renderNonClientInfoList()}
        {this._renderClientInfo()}
      </div>
    );
  }
});
