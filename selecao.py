# -*- coding: utf-8 -*-

def completos(anime_dict):
	return anime_dict["status"] == 2 or anime_dict["status"] == "2"

def avaliados(anime_dict):
	return anime_dict["user_score"] != None and anime_dict["user_score"] > 0
