"use strict";

var http = require('http');
var net = require('net');

var SERVER_PORT = 8789; // Server port for requests
var CLIENT_PORT = 8787; // Client port for reception
var CLIENT_HOST = '0.0.0.0'; // Client host: accepts all interfaces
var DEFAULT = "require('update')([null,null]);"; // Default format for server data

// HTTP server for outgoing data
var httpServer = http.createServer(httpCallback).listen(SERVER_PORT);

// TCP server for incoming connections
var tcpServer = net.createServer(socketCallback).listen(CLIENT_PORT, CLIENT_HOST);

// GPSResponse object to handle responses from TCP server
var gps = new GPSResponse();

/**
 * Handles HTTP Server callback
 * Displays GPSResponse data
 */
function httpCallback (request, response) {
	// Regular Expression to test the match of request url
	var format = /^\/zebra(\?\_\=\d+)?$/;

	// Allows request to directory `/zebra`
	// Ignores all other requests
	if (format.test(request.url)) {
		log(request, response);
		response.writeHead(200, { "Content-Type": "text/javascript" });
		response.writeContinue();
		response.write(gps.response);
		response.end();
	}
}

/**
 * Handles TCP Server callback
 * @param {net.Socket|Object} socket Connection host
 *
 * @description Sets GPSResponse data under different events:
 * `connect`
 *		Resumes connection
 * `data`
 * 		Sets GPSResponse data to received data
 * `error`
 *		Handles GPS Server error for reconnecting
 *		Sets GPSResponse data to `DEFAULT`
 * `end`
 *		Pauses the connection when GPS Server sends "FIN" request
 *		Sets GPSResponse data to `DEFAULT`
 * `close`
 *		Pauses the connection when GPS Server closes
 *		Sets GPSResponse data to `DEFAULT`
 * `timeout`
 *		Determines when GPS Server is disconnected abnormally,
 *			then pauses the connection
 *		Sets GPSResponse data to `DEFAULT`	
 */
function socketCallback (socket) {
	// Sets socket time out to 30 seconds
	// **************************************
	// If there is no activity before timeout,
	// consider GPS Server timeout
	socket.setTimeout(30000);
	
	socket.on('connect', function () {
		console.log('GPS Server Connected');
		try { socket.resume(); } catch (e) { console.log(e); }
	}).on('data', function (data) {
		gps.set(data.toString());
		console.log(gps.response);
	}).on('error', function (e) {
		console.log('GPS Server Error: ' + e.message);
		gps.set(DEFAULT);
	}).on('end', function () {
		console.log('GPS Server Disconnected');
		socket.pause();
		gps.set(DEFAULT);
	}).on('close', function () {
		console.log('GPS Server Connection Closed');
		socket.pause();
		gps.set(DEFAULT);
	}).on('timeout', function () {
		console.log('GPS Server Timed Out');
		socket.pause();
		gps.set(DEFAULT);
	});
}

/**
 * Logs HTTP request and response in console
 *
 * @param {Object} request http.IncomingMessage request
 * @param {Object} response http.ServerResponse response
 */
function log (request, response) {
	// Creates UTC date/time without day of the week
	var date = '[' + new Date().toUTCString().substring(5) + ']';

	console.log(request.connection.remoteAddress +
		' -- ' + date + ' ' + request.method + ' "' + request.url + '": 200');
}

/**
 * Handles responses sent by GPS Server
 *
 * @constructor GPSResponse
 */
function GPSResponse () {
	this.response = DEFAULT;
	this.set = function (arg) {
		this.response = arg;
	};
}
