var QUEUE_URL = 'https://twilio-plays-roomba.herokuapp.com/queue';
var QUEUE_INTERVAL = 5000;

$(document).ready(function() {
	retrieveQueue();
	setInterval(retrieveQueue, QUEUE_INTERVAL);
});

function retrieveQueue() {
	console.log('Retrieving queue...');
	$.get(QUEUE_URL, function(data) {
		$('#commands').empty();
		if(data.length == 0) {
			$("#commands").append('<li class="list-group-item">No commands have been submitted</li>');
		} else {
			data.forEach(function(command) {
				$("#commands").append('<li class="list-group-item"><b>' + command + '<b/></li>');
			});
		}
	});
}
