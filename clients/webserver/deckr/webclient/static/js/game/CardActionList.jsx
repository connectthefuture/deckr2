var React = require('react');
var CardAction = require('./CardAction');

module.exports = React.createClass({
  displayName: 'CardActionList',
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
