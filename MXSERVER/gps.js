"use strict";

module.exports = {
	// Default GPS data
	DEFAULT: "require('update')([null,null]);",

	/**
	 * Handles GPS Status requests
	 */
	Status: function () {
		var str = ["Disonnected", "Connected", "Error", "Timeout"];
		
		/**
		 * Status text
		 */
		this.text = str[0];
		
		/**
		 * Change the status text
		 *
		 * @param {Number} index in array `str`
		 */
		this.change = function (index) {
			if (!index || index >= 4 || index < 0) throw new Error("Invalid");
			else this.text = str[index];
		}
	},
	
	/**
	 * Handles responses sent by GPS Server
	 */
	Response: function () {
		this.response = module.exports.DEFAULT;
		this.set = function (arg) {
			this.response = arg;
		};
	}
};
