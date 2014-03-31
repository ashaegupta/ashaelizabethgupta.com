$(document).ready(function(){
	var collection=["rust","outsider","ribbon","blush","summer", "sway"];
	var i = 0;
	
	var rotate = function() {
		if (i == collection.length-1) {
			$("#canvas").first().removeClass(collection[i]).addClass(collection[0]);
			i = 0;
		} else {
			$("#canvas").first().removeClass(collection[i]).addClass(collection[i+1]);	
			i = i + 1;
		}		
	}

	$("#canvas").click(function(){
		rotate();
	});
});