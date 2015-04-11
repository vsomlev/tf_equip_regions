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

// Only for testing, wont be used for production.
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

//////////////////////
/// Conflict detection
//////////////////////

// does 'whole head' conflict with 'lenses' by transitivity?
conflicts_table = {
	'glasses' : ['face', 'lenses'],
	'whole head' : ['hat', 'face', 'glasses'],
	'medal' : ['tournament_medal']
};

function has_conflict(itema, itemb){
	console.log('---------------------');
	console.log('Comparing ' + itema['name'] + ' vs ' + itemb['name']);
	eqa = itema['equip_regions'];
	eqb = itemb['equip_regions'];
	// eqb.push('medal'); // for testing

	console.log('[' + eqa + '] vs [' + eqb + ']');

	// 1. Simple checks first
	has_simple_conflict = eqa.some(function(x){return eqb.indexOf(x)>-1});
	if(has_simple_conflict) return true;

	// 2. Using the conflicts_table from above
	// bad comment-style below:
	var table_check = function(eq1, eq2){
		// does the first item (eq1) have a region that is present in the conflicts_table?:
		// alternatively use filter(), count it, then map() if len>0
		var problematic_regions = eq1.map(function(x){return conflicts_table[x]});
		if(typeof problematic_regions[0] === 'undefined') return false;
		// flatten when there are multiple conflict-able regions
		var problematic_regions = problematic_regions.reduce(function(a,b){return a.concat(b)});

		// does the second item (eq2) has any of these conflicting regions?:
		var has_conflict = problematic_regions.some(function(x){return eq2.indexOf(x)>-1});
		return has_conflict;
	};
	
	tc_ab = table_check(eqa, eqb);
	tc_ba = table_check(eqb, eqa);

	return (tc_ab || tc_ba);
};
