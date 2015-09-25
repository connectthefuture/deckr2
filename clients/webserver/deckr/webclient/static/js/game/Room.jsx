var React = require('react');
var RoomHeader = require('./RoomHeader');
var PlayerInfoList = require('./PlayerInfoList');
var Battlefield = require('./Battlefield');
var Hand = require('./Hand');

module.exports = React.createClass({
  displayName: 'Room',
  _getPlayer: function (players) {
    for (var i = 0; i < players.length; i++) {
      if (players[i].game_id == this.state.player_id)
        return players[i];
    }
  },
  _handleServerResponse: function (message) {
    var SERVER_RESPONSE_DISPATCHER = {
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
  },
  _handleStep: function (step) {
    this.setState({current_step: step});
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
    var _this = this;
    socket.onmessage = function (event) {
      var response = event.data.substring(0, event.data.length - 2)
      var message = ServerResponse.decode64(response);
      console.log("(ROOM) Recieved message:", message);
      _this._handleServerResponse(message);
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
            clientNick={this.props.nick}
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
