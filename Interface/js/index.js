/* Informações do anime */
var AnimeImage = "https://myanimelist.cdn-dena.com/images/anime/1173/92110.jpg";
var Titulo = "Shingeki no Kyojin";
var Rank = 57;
var Sinopse = "Lorem ipsum dolor sit amet consectetur adipisicing elit. At modi molestias iure temporibus omnis pariatur quasi amet nobis sunt dolores. Aspernatur quis totam exercitationem iusto voluptate repellat quidem autem pariatur.";
var Generos = "Action, Military, Mystery, Super Power, Drama, Fantasy, Shounen";
var Score = 4.24;

/* Estimativa gerada pelo classificador */
var valor_estimativa = 3.5;

let starCap = {
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

let starCapClass = {
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