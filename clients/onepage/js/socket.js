/**
 * This file contains a simple wrapper around SockJS with more knowledge about deckr.
 */

// Scopping sillyness
var onepage = {};

onepage.Socket = function(url) {
    /** Url that this socket is connected to. */
    this.url_ = url;

    /** Actual web socket. */
    this.socket_ = new SockJS(url);

    // Callbacks
    this.openCallback_ = null;
    this.messageCallback_ = null;

    // Run all start up handlers.
    this.installSocketHandlers_();
};

/** Get the current state of the socket. */
onepage.Socket.prototype.getSocketState = function() {
    return this.socket_.readyState;
};


/** Set up any callbacks that we may want. */
onepage.Socket.prototype.installCallbacks = function(openCallback, messageCallback) {
    this.openCallback_ = openCallback;
    this.messageCallback_ = messageCallback;
};


/**
 * Send a message along this socket. The message can be any JSON encodable
 * object.
 */
onepage.Socket.prototype.sendMessage = function(message) {
    this.socket_.send(JSON.stringify(message) + "\r\n");
};


/** Install the socket handlers. */
onepage.Socket.prototype.installSocketHandlers_ = function() {
    this.socket_.onopen = this.onOpen_.bind(this);
    this.socket_.onmessage = this.onMessage_.bind(this);
    this.socket_.onclose = this.onClose_.bind(this);
};


/** Handle a socket opening. */
onepage.Socket.prototype.onOpen_ = function(event) {
    console.log("Established a connection with " + this.url_);
    if (this.openCallback_) {
        this.openCallback_(event);
    }
};


/** Handle a message from the server. */
onepage.Socket.prototype.onMessage_ = function(event) {
    console.log("Got a message ", event);
    var cleanedData = event.data.substring(0, event.data.length - 2);
    if (this.messageCallback_) {
        this.messageCallback_(JSON.parse(cleanedData));
    }
};


/** Handle a socket closing (either side) */
onepage.Socket.prototype.onClose_ = function(event) {
    console.log("Closed connection ", event);
};
