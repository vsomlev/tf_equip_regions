function fetch_item_list(done_cb){
	$.ajax({
		url: 'equip_regions_list.txt',
		success: done_cb,
		error: function(x) {alert('Failed loading the items description. Refresh and try again.');}
	});
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
	if(typeof itema == 'undefined' || typeof itemb == 'undefined'){
		return false;
	}
	// console.log('---------------------');
	// console.log('Comparing ' + itema['name'] + ' vs ' + itemb['name']);
	eqa = itema['equip_regions'];
	eqb = itemb['equip_regions'];

	// console.log('[' + eqa + '] vs [' + eqb + ']');

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
