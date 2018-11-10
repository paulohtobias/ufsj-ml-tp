<?php
	$user = $_POST['user'];
	$link = $_POST['link'];
	$estimativa = system("python2.7 ../tp_aprendizado.py -q -u ".
						$user." -a ".
						$link." -m arvore");

	echo $estimativa;

?>
