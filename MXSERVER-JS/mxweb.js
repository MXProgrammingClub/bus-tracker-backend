"use strict";

var http = require('http');
var net = require('net');

// Accepts all interfaces
var CLIENT_HOST = '0.0.0.0';

// Client port for reception
var CLIENT_PORT = 8787;

// Server port for requests
var SERVER_PORT = 8789;

// Default format for server data
var DEFAULT = "require('update')([null,null]);";


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
	// Allows request to directory `/zebra`
	// Ignores all other requests
	if (request.url === '/zebra') {
		console.log('GET' + request.connection.remoteAddress + ' ' + request.url);
		response.writeHead(200, { "content-type": "text/javascript" });
		response.writeContinue();
		response.write(gps.response);
		response.end();
	} else response.end();
	
}

/**
 * Handles TCP Server callback
 * @param {net.Socket|Object} socket Connection host
 *
 * @description Sets GPSResponse data under different events
 *
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
 *		
 */

function socketCallback (socket) {
	// Sets socket time out to 30 seconds
	// **************************************
	// If there is no activity before timeout,
	// consider GPS Server timeout
	socket.setTimeout(30000);
	
	socket.on('connect', function () {
		console.log('GPS Server Connected');
		try { socket.resume(); } catch (e) {}
	}).on('data', function (data) {
		gps.set(data.toString());
		console.log(gps.response);
	}).on('error', function (e) {
		console.log('Error: ' + e.message);
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
