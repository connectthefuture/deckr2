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

function sendPassPriorityMessage () {
  var pass_priority_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'PASS_PRIORITY'
    })
  });

  sendMessage(pass_priority_msg);
}

var RoomHeader = React.createClass({
  _renderStartButton: function () {
    if (!this.props.started) {
      return <button className="start-game">Start Game</button>;
    }
  },
  render: function () {
    return (
      <div className="room-header">
        {this._renderStartButton()}
        <h3 className="game-info">Game: {this.props.name} (id: {this.props.gameId})</h3>
        <span className="n-players">Number of players: {this.props.nPlayers}</span>
        <div className="game-state">Phase: <span className="phase">{this.props.phase}</span></div>
        <div className="game-state">Step: <span className="step">{this.props.step}</span></div>
      </div>
    );
  }
});

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
    return (
      <div className="card" onClick={this._toggleActions} onContextMenu={this._contextMenu}>
        <CardActionList actions={this._cardActions()} showActions={this.state.show_actions} cardId={this.props.cardData.game_id} />
        <span className="card-name">{this.props.cardData.name}</span>
      </div>
    );
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

var Battlefield = React.createClass({
  render: function () {
    if (!this.props.cards) {
      var cards = "";
    } else {
      var cards = this.props.cards.map(function (card) {
        return <Card cardData={card} zone="battlefield" />;
      });
    }
    return (
      <div className="battlefield">
        <h4>Battlefield</h4>
        {cards}
      </div>
    );
  }
});

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

var Room = React.createClass({
  _getPlayer: function (players) {
    for (var i = 0; i < players.length; i++) {
      if (players[i].game_id == this.state.player_id)
        return players[i];
    }
  },
  _handleServerResponse: function (message) {
    SERVER_RESPONSE_DISPATCHER = {
      'JOIN': this._handleJoin,
      'LEAVE': this._handleLeave,
      'ERROR': _handleError,
      'GAME_STATE': this._handleGameState
    };
    var response_type = SERVER_RESPONSE_TYPES[message.response_type];
    SERVER_RESPONSE_DISPATCHER[response_type](message);
  },
  _handleJoin: function (message) {
    console.log("(ROOM) Handling JOIN response.");
    var message = message.join_response;
    this.setState({player_id: message.player_id});
  },
  _handleGameState: function (message) {
    console.log("(ROOM) Handling GAME_STATE response.");
    var room = this;
    var message = message.game_state_response.game_state;
    this.setState({
      started: true,
      battlefield: message.battlefield,
      player: this._getPlayer(message.players),
      players: message.players,
      active_player: message.active_player,
      priority_player: message.priority_player
    });

    this._handlePhase(message.current_phase);
    this._handleStep(message.current_step);
  },
  _handlePhase: function (phase) {
    this.setState({current_phase: phase});
    return;
  },
  _handleStep: function (step) {
    this.setState({current_step: step});
    return;
  },
  getInitialState: function () {
    return {
      started: false,
      battlefield: {},
      player: {},
      players: [],
      player_id: 0,
      active_player: 0,
      priority_player: 0,
      player_has_priority: false,
      current_phase: "",
      current_step: ""
    }
  },
  componentDidMount: function () {
    var room = this;
    socket.onmessage = function (event) {
      response = event.data.substring(0, event.data.length - 2)
      message = ServerResponse.decode64(response);
      console.log("(ROOM) Recieved message:", message);
      room._handleServerResponse(message);
    };
  },
  render: function () {
    return (
      <div>
        <RoomHeader
          gameId={this.props.gameId}
          name={this.props.gameName}
          phase={this.state.current_phase}
          step={this.state.current_step}
          started={this.state.started}
          nPlayers={this.state.players.length}
        />
        <div className="room-center">
          <PlayerInfoList
            players={this.state.players}
            clientPlayer={this.state.player_id}
            activePlayer={this.state.active_player}
            priorityPlayer={this.state.priority_player}
          />
          <Battlefield cards={this.state.battlefield.cards} />
        </div>
        <Hand hand={this.state.player.hand} />
      </div>
    );
  }
});
