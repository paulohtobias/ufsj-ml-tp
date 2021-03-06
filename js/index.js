/****************** Informações Globais ******************/
var valor_estimativa = 0.0;
var g_AnimeImage = "https://myanimelist.cdn-dena.com/images/anime/5/87048.jpg";
var g_Titulo = "Kimi no Na wa";
var g_Rank = 2;
var g_Generos = "Romance, Supernatural, School, Drama";
var g_Score = 9.16/2;

var starCap = {
	0.0: "0: No Score", 
	0.5: "1: Appalling", 
	1.0: "2: Horrible", 
	1.5: "3: Very Bad", 
	2.0: "4: Bad", 
	2.5: "5: Average", 
	3.0: "6: Fine", 
	3.5: "7: Good", 
	4.0: "8: Very Good", 
	4.5: "9: Great", 
	5.0: "10: Masterpiece"
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
