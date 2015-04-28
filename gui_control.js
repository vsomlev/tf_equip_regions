function data_fetch(){
	$.ajax({
		url: 'items_data.json',
		success: on_data_loaded,
		error: function(x) {alert('Failed loading the items description. Refresh and try again.');}
	});
};

function on_data_loaded(data){
	selected_items = [];
	class_filter = 'all';
	items_list = data;
	$('#selector-table').show();
	$('#loading-text').hide();

	update_autocomplete();
};

function update_conflicts(){
	$('#conflict-status').html('Checking...');
	var conflict_status = "";

    selected_items.forEach(function(itemA, i){
        selected_items.slice(++i).forEach(function(itemB){
            if(typeof itemA == 'undefined' || typeof itemB == 'undefined') return;

            var eqa = itemA['e'];
            var eqb = itemB['e'];

            // intersection of equip regions
            if(eqa.some(function(x){return eqb.indexOf(x)!=-1})){
                conflict_status += "Conflict between '" + itemA['name'] + "' and '" + itemB['name'] + "'.<br/>";
            } 
        });
    });

	if(conflict_status.trim().length==0){
		$('#conflict-status').html("No conflicts!");
	} else {
		$('#conflict-status').html(conflict_status);
	}
};

function on_item_select(event, ui){
    var item_idx = parseInt(event.target.id.split('-')[1]);

	var new_item = items_list[ui.item.value];
    new_item['name'] = ui.item.value;
	selected_items[item_idx-1] = new_item;

    change_item_image(item_idx, new_item);
	update_conflicts();
};

// invoked when scrolling the suggestions with arrow up/down
function on_item_preview(event, ui){
    var item_idx = parseInt(event.target.id.split('-')[1]);
	var new_item = items_list[ui.item.value];
    change_item_image(item_idx, new_item);
};

// invoked when cancelling the autocomplete (ESC or deleting the text)
function on_autocomplete_close(event, ui){
    var item_idx = parseInt(event.target.id.split('-')[1]);
    old_item = selected_items[item_idx-1];
    if(typeof old_item === 'undefined'){
        $("#item-"+item_idx+"-entry").val('');
    } else {
        $("#item-"+item_idx+"-entry").val(old_item['name']);
    }
    change_item_image(item_idx, old_item);
};

function change_item_image(item_idx, item){
    var item_image_url = 'empty.png';
    if(item && item['i']){
        item_image_url = "http://media.steampowered.com/apps/440/icons/" + item['i'];
    }
	$("#item-"+item_idx+"-image").attr('src', item_image_url);
};

function clear_item(event, ui){
  var item_idx = parseInt(event.target.id.split('-')[2]);
  selected_items[item_idx-1] = undefined;
  $("#item-"+item_idx+"-entry").val('');
  $("#item-"+item_idx+"-image").attr('src', 'empty.png');
  
  update_conflicts();
};

function update_autocomplete(){
	var items_names_list = [];
    
	for(var name in items_list){
		if(class_filter=='all' || items_list[name]['c'].length==0 || items_list[name]['c'].indexOf(class_filter)>-1){
			items_names_list.push(name);
		}
	}
	var autocomplete_options = {
		source: items_names_list,
		select: on_item_select,
        focus: on_item_preview, //scrolling through the suggestions
        close: on_autocomplete_close // cancelling autocomplete
	};
    $(".item-entry").autocomplete(autocomplete_options);
};

function set_class_filter(event){
	class_filter = event.target.value;
	update_autocomplete();
};