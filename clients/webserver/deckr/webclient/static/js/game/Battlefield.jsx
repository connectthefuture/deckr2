var React = require('react');
var Card = require('./Card');

module.exports = React.createClass({
  displayName: 'Battlefield',
  _permanents: function () {
    var _this = this;
    var client_cards = this.props.cards.filter(function (card) {
      return card.controller === _this.props.clientPlayer;
    });
    // TODO: Group by player.
    var non_client_cards = _.difference(this.props.cards, client_cards);
    return {
      client: client_cards,
      non_client: non_client_cards
    };
  },
  _renderCards: function (cards) {
    return cards.map(function (card) {
      return <Card cardData={card} zone="battlefield" />
    });
  },
  _renderPermanents: function () {
    var permanents = this._permanents();
    return (
      <div className="permanents">
        <div className="non-client-permanents">
          {this._renderCards(permanents.non_client)}
        </div>
        <div className="client-permanents">
          {this._renderCards(permanents.client)}
        </div>
      </div>
    );
  },
  render: function () {
    var permanents = (this.props.cards) ? this._renderPermanents() : "";
    return (
      <div className="battlefield">
        <h4>Battlefield</h4>
        {permanents}
      </div>
    );
  }
});
