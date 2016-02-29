"use strict";

// Max array length: 4 minutes of data max
var MAX_LENGTH = 120;

// The array of items
var arr = [];

/**
 * Authenticates data passed in from GPS
 *
 * @param {Array} data The data passed in from GPS
 * @returns {Boolean} True if data are not the same.
 *					  False otherwise
 */
function dataAuth (data) {
	// Deletes the first item if length over MAX_LENGTH
	if (arr.length >= MAX_LENGTH) arr.shift();

	// Pushes new data to the end of the array
	arr.push(data);
	
	return !isSame();
}

/**
 * Checks if the whole array of data is the same
 * Ignore when data is less than the Max Array Length
 *
 * @returns {Boolean} True if data are the same
 *    			      False otherwise
 */
function isSame () {
	if (arr.length < MAX_LENGTH) return false;
	else {
		var sameCount = 0;
		var base = arr[0];
		arr.forEach(function (coord) {
			if (coord[0] === base[0] && coord[1] === base[1]) sameCount++;
		});
		
		if (sameCount === MAX_LENGTH) return true;
		else return false;
	}
}

module.exports = dataAuth;
