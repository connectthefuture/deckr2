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
  render: function () {
    var _this = this;
    var player_infos = this.props.players.map(function (player) {
      return (
        <PlayerInfo
          player={player}
          playerId={player.game_id}
          isClient={_this._isClient(player.game_id)}
          isActivePlayer={_this._isActivePlayer(player.game_id)}
          hasPriority={_this._hasPriority(player.game_id)} />
      );
    });
    return (
      <div className="player-infos">
        {player_infos}
      </div>
    );
  }
});
