window.onload = function() {
	var my_var = $("#id_category");
	var my_string = "<div class='row'>";
	my_string += "<div class='col'>";
	my_string += "<h1 id='_myid_'>Heading 1</h1>";
	my_string += "</div>";
	my_string += "<div class='col-md-1 my-auto'>";
	//my_string += "<img src='/static/admin/img/icon-addlink.svg' alt='Add'>";
	my_string += "<a href=" + '"' + static_url + '"' + "><i class='fas fa-plus' alt='Agregar'></i></a>";
	my_string += "</div>";
	my_string += "</div>";
	$("#id_category").before(my_string);
	//$("#id_category").before("<div class='row'><div class='col'><h1 id='_myid_'>Heading 1</h1></div><div class='col-md-1'><img src='/static/admin/img/icon-addlink.svg' alt='Add'></div></div>");
	$("#_myid_").replaceWith(my_var);

	// Clear the form
	$('#myForm').get(0).reset(); //clear form data on page load
}
