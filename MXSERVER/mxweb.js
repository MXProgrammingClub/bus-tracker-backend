"use strict";

var http = require('http');
var net = require('net');
var GPSResponse = require('./gps').Response;
var GPSStatus = require('./gps').Status;

var SERVER_PORT = 8080; // Server port for requests
var CLIENT_PORT = 8787; // Client port for reception
var CLIENT_HOST = '0.0.0.0'; // Client host: accepts all interfaces
var DEFAULT = require('./gps').DEFAULT;

// HTTP server for outgoing data
var httpServer = http.createServer(httpCallback).listen(SERVER_PORT);

// TCP server for incoming connections
var tcpServer = net.createServer(socketCallback).listen(CLIENT_PORT, CLIENT_HOST);

// GPSResponse object to handle responses from TCP server
var gps = new GPSResponse();

// GPSStatus object to indicate working status
var status = new GPSStatus();

/**
 * Handles HTTP Server callback
 * Displays GPSResponse data
 */
function httpCallback (request, response) {
	// Regular Expression to test the match of request url
	var gpsFormat = /^\/zebra(\?\_\=\d+)?$/;
	var statusFormat = /^\/status(\?\_\=\d+)?$/;

	// Allows request to directory `/zebra` and `/status`
	// Ignores all other requests
	if (gpsFormat.test(request.url)) {
		log(request, response);
		response.writeHead(200, { "Content-Type": "text/javascript" });
		response.writeContinue();
		response.write(gps.response);
		response.end();
	} else if (statusFormat.test(request.url)) {
		response.writeHead(200, { "Content-Type": "text/javascript" });
		response.writeContinue();
		response.write(status.text);
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
	// Sets socket time out to 10 seconds
	// --------------------------------------
	// If there is no activity before timeout,
	// then GPS Server times out
	socket.setTimeout(10000);

	socket.on('connect', function () {
		var error;
		try {
			socket.resume();
		} catch (e) {
			error = e;
		} finally {
			if (!error) {
				console.log('GPS Server Connected');
				status.change(1);
			} else {
				status.change(2);
			}
		}
	}).on('data', function (data) {
		data = data.toString();
		if (data !== DEFAULT) {
			// if (!require('./data-auth')(data)) { // Data fails
			// 	log('GPS Error: GPS Freezes');
			// 	status.change(2);
			// } else {
				gps.set(data);
				console.log(gps.response);
				status.change(1);
			// }
		} else {
			log('GPS Error: No Signal');
			status.change(2);
		}
	}).on('error', function (e) {
		log('GPS Server Error: ' + e.message);
		status.change(2);
	}).on('end', function () {
		log('GPS Server Disconnected');
		socket.pause();
		status.change(0);
	}).on('close', function () {
		log('GPS Server Connection Closed');
		socket.pause();
		status.change(0);
	}).on('timeout', function () {
		log('GPS Server Timed Out');
		socket.pause();
		status.change(3);
	});
}

/**
 * Logs information in the console
 *
 * @param {Object|String} request HTTP request or log string
 * @param {Object} <optional> response HTTP response
 */
function log (request, response) {
	// Creates UTC date/time without day of the week
	var date = '[' + new Date().toUTCString().substring(5) + '] ';

	// Logs special message string and sets gps response to default
	if (arguments.length !== 2) {
		console.log(date + arguments[0]);
		gps.set(DEFAULT);
	} else { // Logs http request and response
		console.log(request.connection.remoteAddress +
		' -- ' + date + request.method + ' "' + request.url + '": 200');
	}
}
