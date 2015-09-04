function validCustomDeckRow (row) {
  var splitted = row.split(' ');
  return (!isNaN(splitted[0]) && isNaN(splitted[1]));
}

function generateCustomDeckCardRow (row) {
  var splitted = row.split(' ');
  var n = splitted[0];
  var card_name = splitted[1];
  var card_row = [];
  for (var i = 0; i < n; i++) {
    var card = new PlayerConfig.CardInfo({ 'name': card_name });
    card_row.push(card);
  }
  return card_row;
}

function generateCustomDeck () {
  var deck = [];
  var input = $('textarea[name="custom-deck"]').val();
  var rows = input.split("\n");
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    if (validCustomDeckRow(row)) {
      deck = deck.concat(generateCustomDeckCardRow(row));
    } else {
      alert("Custom deck is invalid.");
      return;
    }
  }
  return deck;
}

function generateCustomPlayerConfig () {
  return new PlayerConfig({ 'deck': generateCustomDeck() });
}

// The functions above currently don't work. (I don't think I'm loading the
// card library correctly...)

$(document).ready(function () {
  return;
});
