<?php
	$user = $_POST['user'];
	$link = $_POST['link'];
	system("python2.7 tp_aprendizado.py -q -u ".
                        $user." -a ".
                        $link." -m arvore");

	$estimativa = file_get_contents("nota.txt");

	echo $estimativa;
?>
