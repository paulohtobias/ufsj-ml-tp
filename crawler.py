# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json

"""
atributos iniciais
  status
  user_score
  type
  episodes (total)
  aired
  licensors (? pode ser ultil em uma possível oficialização onde a disponibilidade de transmissão local oficial é um fator)
  studios
  source (imagino que vai ter pouco impacto)
  genres
  duration
  rating
  public_score
  rank
  popularity
"""

"""
todo: criar filtros
  eg.: numero minimo (e maximo) de episódios (total ou assistidos),
       casamento de caracteres pros fitros comuns
       exigir que um atributo contenha um valor (nota do usuário)
       etc
"""

#Status
class Status:
    watching = "1"
    completed = "2"
    hold = "3"
    dropped = "4"
    plan = "6" #Não sei nem se faz sentido esse.
    todos = "7"

usuario = "jusaragu"

def get_lista(usuario, status = Status.todos):
    #todo: deixar retornar mais de um status por vez?
    url = "https://myanimelist.net/animelist/" + usuario + "?status=" + status

    response = urllib2.urlopen(url)
    pagina = response.read()

    soup = BeautifulSoup(pagina, 'lxml')
    return json.loads(soup.find(class_="list-table")["data-items"])
