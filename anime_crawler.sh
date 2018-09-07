#!/bin/bash

PAGINA=$1
TETO=$2 #Total de páginas
STOP_ON_ERROR="True"
while [  $PAGINA -lt $TETO ];
do
	echo $PAGINA
	python find_database.py $PAGINA 1 $STOP_ON_ERROR &
	PAGINA=$((PAGINA+1))
done
