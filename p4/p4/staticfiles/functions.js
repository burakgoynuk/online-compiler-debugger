
$(document).ready(function () {

var compileResult = $('#cr');


});




function AJAX_post( filename, toBeSended ) 			// establish ajax connection and get the content of json file
{
	var ret_data;
	
	$.ajax
	({
			url: filename,						// url of file
			type: "POST",						// post method
			data: toBeSended,					// sended data
			dataType: "json",					// type will be json
			async: false,						// wait for file to be ready
		
			success: function( data )
			{
				ret_data = data;				// returning data
			}
	});
	
 	return ret_data;
}
