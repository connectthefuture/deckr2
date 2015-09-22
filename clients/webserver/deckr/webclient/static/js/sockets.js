var DECKR_SERVER_URL = "http://localhost:8080";
var socket = new SockJS(DECKR_SERVER_URL);

// Socket state enum
SOCKET_STATES = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
};

function runOnceSocketOpens (callback) {
  if (getSocketState() === SOCKET_STATES.OPEN)
    return callback();

  var return_value;
  setTimeout(function () {
    if (getSocketState() === SOCKET_STATES.OPEN) {
      return_value = callback();
    } else {
      console.log("Wating for connection...");
      return_value = runOnceSocketOpens(callback);
    }
  }, 5);
  return return_value;
}

function sendMessageOnceSocketOpens (message) {
  runOnceSocketOpens(function () {
    sendMessage(message);
  });
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
  'GAME_STATE'
];

function isResponseType(response, type) {
  return SERVER_RESPONSE_TYPES[response.response_type] === type;
}

function handleServerResponse (message) {
  SERVER_RESPONSE_DISPATCHER = {
    'CREATE': _handleCreate,
    'LEAVE': _handleLeave,
    'ERROR': _handleError
  };
  var response_type = SERVER_RESPONSE_TYPES[message.response_type];
  SERVER_RESPONSE_DISPATCHER[response_type](message);
}

function _handleCreate (message) {
  console.log("Handling CREATE response");
  var message = message.create_response;
  handleCreate(message); // Defined in create_game.js
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
