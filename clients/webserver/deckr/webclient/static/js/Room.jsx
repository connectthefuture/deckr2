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
