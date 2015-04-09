// If you don't want to use jQuery
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
	// GET(item_list_json_url,
	// 		done_cb,
	// 		function(xhr) { alert('NOPE'); }
	// );
	$.ajax({
		url: item_list_json_url,
		success: done_cb,
		error: function(hue) {alert('NOPE');}
	});
};

function find_item(partial_name, item_list){
	partial_name = partial_name.toLowerCase().replace(/\s+/g, '').replace(/'/g, '');
	// 1. Full match
	for(var name in item_list){
		if(name == partial_name){
			return item_list[name];
		}
	}
	// 2. Partial match
	for(var name in item_list){
		if(name.indexOf(partial_name)>-1){
			return item_list[name];
		}
	}
	return null;
};

conflicts_table = {
	'glasses' : ['face', 'lenses'],
	'whole head' : ['hat', 'face', 'glasses'],
	'medal' : ['tournament_medal']
};

function has_conflict(itema, itemb){
	console.log('Comparing ' + itema['name'] + ' vs ' + itemb['name']);
	eqa = itema['equip_regions'];
	eqb = itemb['equip_regions'];

	// 1. Simple checks first
	for (var i in eqa){
		if(eqb.indexOf(eqa[i])>-1){
			console.log('CONFLICT same equip region ' + eqa[i]);
			return true;
		}
	}

	// 2. Using the conflicts_table from above
	// Checks if eq1 has an item that is a key in the conflict table.
	// If it has one, check if one of the conflicting regions are present in eq2.
	var table_check = function(eq1, eq2){
		for(var region1 in conflicts_table){
			if(eq1.indexOf(region1)>-1){
				for(var region2_idx in conflicts_table[region1]){
					var region2 = conflicts_table[region1][region2_idx];
					if(eq2.indexOf(region2)>-1){
						console.log('CONFLICT table ' + region1 + ' vs ' + region2); 
						// console.log(eq1);
						// console.log(eq2);
						return true;
					}
				}
			}
		}
		return false;
	};
	table_check_ab = table_check(eqa, eqb);
	table_check_ba = table_check(eqb, eqa);

	if(table_check_ab || table_check_ba){
		return true;
	}

	return false;
};
