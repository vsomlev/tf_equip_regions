// does 'whole head' conflict with 'lenses' by transitivity?
conflicts_table = {
	'glasses' : ['face', 'lenses'],
	'whole_head' : ['hat', 'face', 'glasses', 'lenses'],
};

// Extend the equip regions with those from the conflicts_table.
function full_equip_regions(listA){
    var full_eq = listA.slice();
    listA.forEach(function(x){
        if(x in conflicts_table){
            full_eq = full_eq.concat(conflicts_table[x]);
        }
    });
    return full_eq;
};

function has_conflicts(itemA, itemB){
	if(typeof itemA == 'undefined' || typeof itemB == 'undefined') return false;

	var eqa = full_equip_regions(itemA['equip_regions']);
	var eqb = full_equip_regions(itemB['equip_regions']);

    // intersection
    return eqa.some(function(x){return eqb.indexOf(x)!=-1});
};