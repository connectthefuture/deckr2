var PlayerInfoList = React.createClass({
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

var PlayerInfo = React.createClass({
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

var Hand = React.createClass({
  render: function () {
    if (!this.props.hand) return <div className="hand"></div>;
    var cards = this.props.hand.cards.map(function (card) {
      return <Card cardData={card} zone="hand" />;
    });
    return (
      <div className="hand">
        <h4>Hand: ({this.props.hand.cards.length})</h4>
        {cards}
      </div>
    );
  }
});

var PlayerGameActions = React.createClass({
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
