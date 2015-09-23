var React = require('react');
var Card = require('./Card');

module.exports = React.createClass({
  displayName: 'Hand',
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
