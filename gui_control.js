function data_fetch(done_cb){
	$.ajax({
		url: 'items_data.json',
		success: done_cb,
		error: function(x) {alert('Failed loading the items description. Refresh and try again.');}
	});
};

function update_conflicts(){
	$('#conflict-status').html('Checking...');
	var conflict_status = '';

	for(var i=0; i<selected_items.length; i++){
		var itemA = selected_items[i];
		for(var j=i+1; j<selected_items.length; j++){
			var itemB = selected_items[j];
			var conflict = has_conflicts(itemA, itemB);
			if(conflict){
				conflict_status += "Conflict between '" + itemA['name'] + "' and '" + itemB['name'] + "'.<br/>";
			}
		}
	}

	if(conflict_status.length==0){
		$('#conflict-status').html("No conflicts!");
	} else {
		$('#conflict-status').html(conflict_status);
	}
};

function on_item_select(event, ui){
    var item_idx = parseInt(event.target.id.split('-')[1]);

	var new_item = items_list[ui.item.value];
	selected_items[item_idx-1] = new_item;

	var item_image_url = new_item['image'];
	$("#item-"+item_idx+"-image").attr('src', item_image_url);

	update_conflicts();
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
		if(class_filter=='all' || items_list[name]['classes'].indexOf('all')>-1 || items_list[name]['classes'].indexOf(class_filter)>-1){
			items_names_list.push(items_list[name]['name']);
		}
	}
	var autocomplete_options = {
		source: items_names_list,
		select: on_item_select
	};
    $(".item-entry").autocomplete(autocomplete_options);
};

function on_data_loaded(data){
	selected_items = [];
	class_filter = 'all';
	items_list = data;
	$('#selector-table').show();
	$('#loading-text').hide();

	update_autocomplete();
};

function set_class_filter(event){
	class_filter = event.target.value;
	update_autocomplete();
};
