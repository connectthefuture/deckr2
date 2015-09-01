var DECKR_SERVER_URL = "http://localhost:8080";
var socket = new SockJS(DECKR_SERVER_URL);

// Socket state enum
SOCKET_STATES = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
};

function sendMessageOnceSocketOpens (message) {
  setTimeout(function () {
    if (getSocketState() === SOCKET_STATES.OPEN) {
      sendMessage(message);
    } else {
      console.log("Wating for connection...");
      sendMessageOnceSocketOpens(message);
    }
  }, 5);
}

function sendMessage (message) {
  console.log("Sending message.")
  socket.send(message.toBase64() + "\r\n");
}

function getSocketState () {
  return socket.readyState;
}

function getSocketStateInEnglish () {
  var english = Object.keys(SOCKET_STATES);
  return english[getSocketState()];
}

SERVER_RESPONSE_TYPES = [
  'CREATE',
  'JOIN',
  'LEAVE',
  'ERROR',
  'GAME_STATE',
  'GAME_UPDATE'
];

function isResponseType(response, type) {
  return SERVER_RESPONSE_TYPES[response.response_type] === type;
}

function handleServerResponse (message) {
  SERVER_RESPONSE_DISPATCHER = {
    'CREATE': _handleCreate,
    'JOIN': _handleJoin,
    'LEAVE': _handleLeave,
    'ERROR': _handleError,
    'GAME_STATE': _handleGameState,
    'GAME_UPDATE': _handleGameUpdate
  };
  var response_type = SERVER_RESPONSE_TYPES[message.response_type];
  SERVER_RESPONSE_DISPATCHER[response_type](message);
}

function _handleCreate (message) {
  console.log("Handling CREATE response");
  var message = message.create_response;
  $("input[name='game_id']").val(message.game_id);
  $('form').submit();
}

function _handleJoin (message) {
  console.log("Handling JOIN response");
  var message = message.join_response;
  return;
}

function _handleLeave (message) {
  console.log("Handling LEAVE response");
  return;
}

function _handleError (message) {
  console.log("Handling ERROR response");
  var message = message.error_response;
  return;
}

function _handleGameState (message) {
  console.log("Handling GAME STATE response");
  var message = message.game_state_response;
  return;
}

function _handleGameUpdate (message) {
  console.log("Handling GAME UPDATE response");
  var message = message.game_update_response;
  return;
}


// Handling socket events.

socket.onopen = function () {
  console.log("Successfuly connected to the Deckr server.");
}

socket.onmessage = function (event) {
  // Since we use sendLine, we recieve an additional two characters with our
  // response, so we need remove them so we can properly decode the message.
  response = event.data.substring(0, event.data.length - 2)
  message = ServerResponse.decode64(response);
  console.log("Recieved message:", message);
  handleServerResponse(message);
}

socket.onclose = function () {
  console.log("Closing connection to Deckr server.");
}
