function GET(path, success, error){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function()
	{
		if (xhr.readyState === XMLHttpRequest.DONE) {
			if (xhr.status === 200) {
				if (success)
					success(xhr.responseText);
			} else {
				if (error)
					error(xhr);
			}
		}
	};
	xhr.open("GET", path, true);
	xhr.send();
};

// Doesn't work ATM because of Access-Control-Allow-Origin.
function fetch_client_schema(){
	var vdf_data = null;
	var client_schema_location = "http://git.optf2.com/schema-tracking/plain/Team%20Fortress%202%20Client%20Schema?h=teamfortress2";
	GET(client_schema_location,
		function(data) {process_equip_data(data)},
		function(xhr) {alert('Could not fetch the client schema');}
	);
};

function process_equip_data(vdf_text){
	data = vdf.parse(vdf_text);
	vdf_text = vdf.stringify(data);
	console.log(vdf_text);
};

function fetch_item_list(done_cb){
	item_list_json_url = 'equip_regions_list.txt';
	GET(item_list_json_url,
			done_cb,
			function(xhr) { alert('NOPE'); }
	);
};

function find_item(partial_name, item_list){
	for (var name in item_list){
		// TODO: All names in lower-case at list generation time
		// TODO: Replace spaces and other special symbols both in partial_name and in list at generation time
		if(name.toLowerCase().indexOf(partial_name.toLowerCase())>-1){
			return item_list[name];
		}
	}
	return null;
};
