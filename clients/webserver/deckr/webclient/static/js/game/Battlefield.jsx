var React = require('react');
var Card = require('./Card');

module.exports = React.createClass({
  displayName: 'Battlefield',
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
