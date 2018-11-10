/****************** Informações Globais ******************/
var valor_estimativa = 0.5;

var starCap = {
	0.0: "No Score", 
	0.5: "Appalling", 
	1.0: "Horrible", 
	1.5: "Very Bad", 
	2.0: "Bad", 
	2.5: "Average", 
	3.0: "Fine", 
	3.5: "Good", 
	4.0: "Very Good", 
	4.5: "Great", 
	5.0: "Masterpiece"
};

var starCapClass = {
	0.5: 'badge badge-danger bg-danger f-md',
	1.0: 'badge badge-danger bg-danger f-md',
	1.5: 'badge badge-warning bg-warning f-md',
	2.0: 'badge badge-warning bg-warning f-md',
	2.5: 'badge badge-info bg-info f-md',
	3.0: 'badge badge-info bg-info f-md',
	3.5: 'badge badge-primary bg-primary f-md',
	4.0: 'badge badge-primary bg-primary f-md',
	4.5: 'badge badge-success bg-success f-md',
	5.0: 'badge badge-success bg-success f-md'
};

/************************ Funções ************************/
var getLocation = function(href) {
    var l = document.createElement("a");
    l.href = href;
    return l;
};