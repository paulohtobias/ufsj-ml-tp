<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<title>Anime Oráculo</title>
	
	<!-- Icones do Font Awelsome -->
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
	
	<!-- Bootstrap 4 Interface -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
	
	<!-- Bootstrap 4 Funcionalidades -->
	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>

	<!-- Chart.js Gerador de gráficos -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
	
	<!-- CSS da página -->
	<link rel="stylesheet" type="text/css" media="screen" href="./css/index.css" />
	
	<!-- Javascript da página -->
	<script src="./js/index.js"></script>

	<!-- Bootstrap 3 star rating -->
	<!-- default styles -->
	<link href="http://netdna.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.css" rel="stylesheet">
	<link href="./vendor/bootstrap-star-rating-master/css/star-rating.css" media="all" rel="stylesheet" type="text/css" />

	<!-- optionally if you need to use a theme, then include the theme CSS file as mentioned below -->
	<link href="./vendor/bootstrap-star-rating-master/themes/krajee-svg/theme.css" media="all" rel="stylesheet" type="text/css" />

	<!-- important mandatory libraries -->
	<!--suppress JSUnresolvedLibraryURL -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
	<script src="./vendor/bootstrap-star-rating-master/js/star-rating.js" type="text/javascript"></script>

	<!-- optionally if you need to use a theme, then include the theme JS file as mentioned below -->
	<script src="./vendor/bootstrap-star-rating-master/themes/krajee-svg/theme.js"></script>

	<!-- optionally if you need translation for your language then include locale file as mentioned below -->
	<script src="./vendor/bootstrap-star-rating-master/js/locales/pt-BR.js"></script>
	
</head>
<body class="bg">
	<div class="container-fluid mt-2 mb-2">
		<div class="row justify-content-center">
			<div class="col-10 bg-white shadow-lg rounded">
				<!-- Logo -->
				<div class="jumbotron text-center bg-info text-white mt-3">
					<h1><i class="fas fa-globe-americas"></i> Anime Oráculo</h1>
				</div>

				<!-- Entradas do Aplicativo -->
				<div class="row">
					<!-- Username -->
					<div class="col-12 col-sm-6">
						<label for="basic-url">Username:</label>
						<div class="input-group mb-3">
							<input type="text" class="form-control" placeholder="jusaragu">
						</div>
					</div>
					
					<!-- Link do Anime -->
					<div class="col-12 col-sm-6">
						<label for="basic-url">Link do Anime:</label>
						<div class="input-group mb-3">
							<input type="text" class="form-control" placeholder="https://myanimelist.net/anime/21/One_Piece">
						</div>
					</div>
				</div>

				<!-- Botão de chamada de avaliação -->
				<div class="row justify-content-center mb-3">
					<button type="button" class="btn btn-success">Avaliar</button>
				</div>

				<!-- Informações de Resposta -->
				<div class="row mb-3">
					<!-- Informações do anime -->
					<div class="col-12">
						<p>Coisas do anime</p>
					</div>

					<!-- Avaliação Realizada -->
					<div class="col-12 text-center">
						<span id="caption-estimativa"></span>
						<input id="estimativa" type="text" class="rating-loading">
					</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>

<script>
	/* As variaveis valor_estimativa, starCap e starCapClass 
	 * estão no arquivo ./js/index.js */
	$("#estimativa").attr("value",valor_estimativa);
	$("#estimativa").rating({
		disabled: true,
		clearButton: "",
		size: "sm",
		captionElement: "#caption-estimativa",
		starCaptions: starCap,
		starCaptionClasses: starCapClass
	});
</script>

<?php
	echo system("ls");

?>