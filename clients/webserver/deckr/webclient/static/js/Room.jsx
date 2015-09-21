function sendPassPriorityMessage () {
  var pass_priority_msg = new ClientMessage({
    'message_type': 'ACTION',
    'action_message': new ActionMessage({
      'action_type': 'PASS_PRIORITY'
    })
  });

  sendMessage(pass_priority_msg);
}

var GameState = React.createClass({
  render: function() {
    return (
      <div>
        <p>Phase: <span className="phase">{this.props.phase}</span></p>
        <p>Step: <span className="step">{this.props.step}</span></p>
      </div>
    );
  }
});

var PlayerInfo = React.createClass({
  _renderTurn: function () {
    if (this.props.isActivePlayer) {
      return (
        <span className="turn">It is your turn.</span>
      );
    }
  },
  _renderPriority: function () {
    if (this.props.hasPriority) {
      return (
        <span className="priority">You have priority.</span>
      );
    }
  },
  getInitialState: function() {
    return {};
  },
  componentDidMount: function() {
    return;
  },
  render: function() {
    return (
      <div>
        <h3>Player: {this.props.nick} ({this.props.playerId})</h3>
        <p>{this._renderTurn()}</p>
        <p>{this._renderPriority()}</p>
      </div>
    )
  }
});

var PlayerGameActions = React.createClass({
  handlePassPriorityClick: function () {
    if (this.props.hasPriority)
      sendPassPriorityMessage();
  },
  render: function () {
    return (
      <div className="game-actions">
        <button className="start-game">Start Game</button>
        <button onClick={this.handlePassPriorityClick} className="pass-priority">Pass Priority</button>
      </div>
    );
  }
});

var Room = React.createClass({
  _handleServerResponse: function (message) {
    SERVER_RESPONSE_DISPATCHER = {
      'JOIN': this._handleJoin,
      'LEAVE': this._handleLeave,
      'ERROR': this._handleError,
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
    var message = message.game_state_response.game_state;
    this.setState({
      started: true,
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
  _hasPriority: function () {
    return this.state.priority_player == this.state.player_id;
  },
  _isActivePlayer: function () {
    return this.state.active_player == this.state.player_id;
  },
  getInitialState: function () {
    return {
      started: false,
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
        <h1>Game (id: {this.props.gameId}, name: {this.props.gameName})</h1>
        <GameState phase={this.state.current_phase} step={this.state.current_step} />
        <PlayerInfo
          playerId={this.state.player_id}
          nick={this.props.nick}
          isActivePlayer={this._isActivePlayer()}
          hasPriority={this._hasPriority()}
        />
        <PlayerGameActions hasPriority={this._hasPriority} />
      </div>
    );
  }
});
