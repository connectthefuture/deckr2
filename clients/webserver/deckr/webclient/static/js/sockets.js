var DECKR_SERVER_URL = "http://localhost:8080";
var socket = new SockJS(DECKR_SERVER_URL);

// Socket state enum
SOCKET_STATES = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
};

function sendMessage (message) {
  console.log("Sending message.")
  socket.send(message.encodeJSON() + "\r\n");
}

function getSocketState () {
  return socket.readyState;
}

function getSocketStateInEnglish () {
  var english = Object.keys(SOCKET_STATES);
  return english[getSocketState()];
}

function handleServerResponse (response) {
  message = ServerResponse.decodeJSON(response);
  if (message.response_type === 0) {
    _handleCreate(message.create_response);
  }
}

function _handleCreate (message) {
  $("input[name='game_id']").val(message.game_id);
  $('form').submit();
}


// Handling socket events.

socket.onopen = function () {
  console.log("Successfuly connected to the Deckr server.");
}

socket.onmessage = function (event) {
  console.log("Recieved message:", event.data);
  handleServerResponse(event.data);
}

socket.onclose = function () {
  console.log("Closing connection to Deckr server.");
}
