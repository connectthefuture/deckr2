var ProtoBuf = dcodeIO.ProtoBuf;
var ClientMessageBuilder = ProtoBuf.loadProtoFile("../proto/client_message");
var ServerResponseBuilder = ProtoBuf.loadProtoFile("../proto/server_response");
// ClientMessage schemas
var ClientMessage = ClientMessageBuilder.build("ClientMessage");
var CreateMessage = ClientMessageBuilder.build("CreateMessage");
var JoinMessage = ClientMessageBuilder.build("JoinMessage");
var ActionMessage = ClientMessageBuilder.build("ActionMessage");
var PlayerConfig = ClientMessageBuilder.build("PlayerConfig");
var PlayAction = ClientMessageBuilder.build("PlayAction");
var ActivateAction = ClientMessageBuilder.build("ActivateAction");
var DeclareAttackersAction = ClientMessageBuilder.build("DeclareAttackersAction");
var DeclareBlockersAction = ClientMessageBuilder.build("DeclareBlockersAction");

// ServerResponse schemas
var ServerResponse = ServerResponseBuilder.build("ServerResponse");
var CreateResponse = ServerResponseBuilder.build("CreateResponse");
var ErrorResponse = ServerResponseBuilder.build("ErrorResponse");
var GameStateResponse = ServerResponseBuilder.build("GameStateResponse");
var GameUpdateResponse = ServerResponseBuilder.build("GameUpdateResponse");
var GameState = ServerResponseBuilder.build("GameState");
var GameObject = ServerResponseBuilder.build("GameObject");
var Player = ServerResponseBuilder.build("Player");
var Zone = ServerResponseBuilder.build("Zone");
var Card = ServerResponseBuilder.build("Card");
var Counter = ServerResponseBuilder.build("Counter");
var Ability = ServerResponseBuilder.build("Ability");
var KeyValuePair = ServerResponseBuilder.build("KeyValuePair");
