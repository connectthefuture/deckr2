var DECKR_SERVER_URL = "http://localhost:8080";
var socket = new SockJS(DECKR_SERVER_URL);

// Socket state enum
SOCKET_STATES = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
};

function getSocketState () {
  return socket.readyState;
}

function getSocketStateInEnglish () {
  var english = Object.keys(SOCKET_STATES);
  return english[getSocketState()];
}

socket.onopen = function () {
  console.log("Successfuly connected to the Deckr server.");
}
