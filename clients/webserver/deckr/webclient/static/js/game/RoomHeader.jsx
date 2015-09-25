var React = require('react');

module.exports = React.createClass({
  displayName: 'RoomHeader',
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
