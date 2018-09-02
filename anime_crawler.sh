#!/bin/bash

TETO=2 #Total de páginas
PAGINA=0
while [  $PAGINA -lt $TETO ];
do
	python find_database.py $PAGINA 1 &
	PAGINA=$((PAGINA+1))
done
