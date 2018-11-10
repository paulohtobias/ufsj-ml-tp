{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# -*- coding: utf-8 -*-\n",
    "\n",
    "import json\n",
    "import crawler\n",
    "import pandas as pd\n",
    "\n",
    "class_names = [\"No Score\", \"Appalling\", \"Horrible\", \"Very Bad\", \"Bad\", \"Average\", \"Fine\", \"Good\", \"Very Good\", \"Great\", \"Masterpiece\"]\n",
    "\n",
    "atributos_anime_todos = [\"title\", \"duration\", \"episodes\", \"genres\", \"popularity\", \"public_score\", \"rank\", \"rating\", \"source\", \"studios\", \"type\", \"year\"]\n",
    "atributos_avaliacao_todos = [\"num_watched_episodes\", \"user_score\", \"status\"]\n",
    "\n",
    "def filtro(usuario, f_selecao, atributos_anime = atributos_anime_todos, atributos_avaliacao = atributos_avaliacao_todos, force_update = False):\n",
    "\tif \"user_score\" not in atributos_avaliacao:\n",
    "\t\tatributos_avaliacao.append(\"user_score\")\n",
    "\n",
    "\tdados = []\n",
    "\tlista_animes = crawler.get_lista(usuario)\n",
    "\n",
    "\tgeneros = []\n",
    "\testudios = []\n",
    "\tfor anime in lista_animes:\n",
    "\t\tgeneros.extend(anime.genres)\n",
    "\t\testudios.extend(anime.studios)\n",
    "\n",
    "\tgeneros = list(set(generos))\n",
    "\testudios = list(set(estudios))\n",
    "\n",
    "\tfor anime in lista_animes:\n",
    "\t\tdado = {}\n",
    "\t\tdado_filtrado = {}\n",
    "\n",
    "\t\t# Pegando os dados do anime\n",
    "\t\tfor atributo in atributos_anime_todos:\n",
    "\t\t\tdado[atributo] = anime.__dict__[atributo]\n",
    "\n",
    "\t\t# Pegando os dados da avaliação\n",
    "\t\twith open(\"data/users/\" + usuario + \"/\" + str(anime.id) + \".json\") as f:\n",
    "\t\t\tavaliacao = json.loads(f.read())\n",
    "\n",
    "\t\t\tfor atributo in atributos_avaliacao_todos:\n",
    "\t\t\t\tdado[atributo] = avaliacao[atributo]\n",
    "\n",
    "\t\tif f_selecao == None or f_selecao(dado):\n",
    "\t\t\tdado_filtrado = {}\n",
    "\t\t\t\n",
    "\t\t\tfor atributo in atributos_anime:\n",
    "\t\t\t\tvalor = dado[atributo]\n",
    "\t\t\t\tif atributo == \"episodes\":\n",
    "\t\t\t\t\tvalor = int(dado[atributo])\n",
    "\n",
    "\t\t\t\tif atributo == \"genres\":\n",
    "\t\t\t\t\tfor genero in generos:\n",
    "\t\t\t\t\t\tif genero in dado[\"genres\"]:\n",
    "\t\t\t\t\t\t\tdado_filtrado[\"Genre:\" + genero] = 1\n",
    "\t\t\t\t\t\telse:\n",
    "\t\t\t\t\t\t\tdado_filtrado[\"Genre:\" + genero] = -1\n",
    "\t\t\t\t\tcontinue\n",
    "\n",
    "\t\t\t\tif atributo == \"studios\":\n",
    "\t\t\t\t\tfor estudio in estudios:\n",
    "\t\t\t\t\t\tif estudio in dado[\"studios\"]:\n",
    "\t\t\t\t\t\t\tdado_filtrado[\"Studio:\" + estudio] = 1\n",
    "\t\t\t\t\t\telse:\n",
    "\t\t\t\t\t\t\tdado_filtrado[\"Studio:\" + estudio] = -1\n",
    "\t\t\t\t\tcontinue\n",
    "\n",
    "\t\t\t\tif \"episodes\" in atributo:\n",
    "\t\t\t\t\tepis = valor\n",
    "\t\t\t\t\tif epis <= 6:\n",
    "\t\t\t\t\t\tvalor = 1\n",
    "\t\t\t\t\telif epis <= 14:\n",
    "\t\t\t\t\t\tvalor = 2\n",
    "\t\t\t\t\telif epis <= 26:\n",
    "\t\t\t\t\t\tvalor = 3\n",
    "\t\t\t\t\telif epis <= 70:\n",
    "\t\t\t\t\t\tvalor = 4\n",
    "\t\t\t\t\telse:\n",
    "\t\t\t\t\t\tvalor = 5\n",
    "\n",
    "\t\t\t\tdado_filtrado[atributo] = valor\n",
    "\n",
    "\t\t\tfor atributo in atributos_avaliacao:\n",
    "\t\t\t\tdado_filtrado[atributo] = dado[atributo]\n",
    "\n",
    "\t\t\tdados.append(dado_filtrado)\n",
    "\t\n",
    "\treturn dados\n",
    "\n",
    "\n",
    "lista_final = filtro(\"zarem101\", lambda d: d[\"status\"] == 2, [\"duration\", \"episodes\", \"genres\", \"type\", \"year\"], [])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_json(json.dumps(lista_final))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "    Genre:Action  Genre:Adventure  Genre:Comedy  Genre:Dementia  Genre:Demons  \\\n",
      "0              1                1            -1              -1            -1   \n",
      "1              1                1            -1              -1            -1   \n",
      "2             -1               -1            -1              -1            -1   \n",
      "3              1               -1            -1              -1            -1   \n",
      "4              1                1            -1              -1             1   \n",
      "5             -1               -1             1              -1            -1   \n",
      "6             -1                1             1              -1            -1   \n",
      "7             -1                1            -1              -1            -1   \n",
      "8              1                1            -1              -1            -1   \n",
      "9              1               -1            -1              -1            -1   \n",
      "10             1               -1             1              -1            -1   \n",
      "11             1               -1            -1              -1            -1   \n",
      "12             1                1            -1              -1            -1   \n",
      "13             1                1            -1              -1            -1   \n",
      "14            -1               -1            -1              -1            -1   \n",
      "15             1               -1             1              -1            -1   \n",
      "16             1               -1             1              -1            -1   \n",
      "17            -1                1             1              -1            -1   \n",
      "18            -1               -1            -1              -1            -1   \n",
      "19             1               -1             1              -1            -1   \n",
      "20             1               -1             1              -1            -1   \n",
      "21            -1               -1            -1              -1            -1   \n",
      "22            -1               -1             1              -1            -1   \n",
      "23            -1                1             1              -1            -1   \n",
      "24            -1               -1             1              -1            -1   \n",
      "25             1               -1             1              -1            -1   \n",
      "26            -1               -1            -1              -1            -1   \n",
      "27             1               -1            -1              -1            -1   \n",
      "28            -1                1            -1              -1            -1   \n",
      "29            -1               -1            -1              -1            -1   \n",
      "\n",
      "    Genre:Drama  Genre:Ecchi  Genre:Fantasy  Genre:Game  Genre:Harem  ...   \\\n",
      "0            -1           -1              1          -1           -1  ...    \n",
      "1            -1           -1             -1          -1           -1  ...    \n",
      "2            -1           -1             -1          -1           -1  ...    \n",
      "3             1           -1              1          -1           -1  ...    \n",
      "4            -1           -1              1          -1           -1  ...    \n",
      "5            -1            1              1          -1           -1  ...    \n",
      "6            -1            1              1           1           -1  ...    \n",
      "7             1           -1             -1          -1           -1  ...    \n",
      "8             1           -1             -1          -1           -1  ...    \n",
      "9             1           -1             -1          -1           -1  ...    \n",
      "10           -1           -1             -1          -1           -1  ...    \n",
      "11            1           -1              1          -1           -1  ...    \n",
      "12            1           -1             -1          -1           -1  ...    \n",
      "13           -1           -1              1          -1           -1  ...    \n",
      "14            1           -1             -1          -1           -1  ...    \n",
      "15           -1           -1             -1          -1           -1  ...    \n",
      "16           -1           -1             -1          -1           -1  ...    \n",
      "17           -1           -1              1          -1           -1  ...    \n",
      "18            1           -1              1          -1           -1  ...    \n",
      "19           -1           -1             -1          -1           -1  ...    \n",
      "20           -1           -1             -1          -1           -1  ...    \n",
      "21            1           -1             -1          -1           -1  ...    \n",
      "22           -1           -1             -1          -1           -1  ...    \n",
      "23           -1           -1              1          -1           -1  ...    \n",
      "24           -1           -1              1          -1           -1  ...    \n",
      "25           -1           -1             -1          -1           -1  ...    \n",
      "26           -1           -1              1          -1           -1  ...    \n",
      "27           -1           -1             -1          -1           -1  ...    \n",
      "28           -1           -1             -1           1           -1  ...    \n",
      "29           -1           -1             -1          -1           -1  ...    \n",
      "\n",
      "    Genre:Slice of Life  Genre:Super Power  Genre:Supernatural  \\\n",
      "0                    -1                  1                  -1   \n",
      "1                    -1                 -1                   1   \n",
      "2                    -1                 -1                   1   \n",
      "3                    -1                  1                  -1   \n",
      "4                    -1                  1                   1   \n",
      "5                    -1                 -1                  -1   \n",
      "6                    -1                 -1                   1   \n",
      "7                    -1                 -1                   1   \n",
      "8                    -1                 -1                   1   \n",
      "9                    -1                 -1                   1   \n",
      "10                   -1                 -1                  -1   \n",
      "11                   -1                  1                  -1   \n",
      "12                   -1                 -1                   1   \n",
      "13                   -1                 -1                  -1   \n",
      "14                   -1                  1                  -1   \n",
      "15                   -1                  1                   1   \n",
      "16                   -1                 -1                  -1   \n",
      "17                   -1                 -1                   1   \n",
      "18                   -1                 -1                  -1   \n",
      "19                   -1                  1                  -1   \n",
      "20                    1                 -1                   1   \n",
      "21                   -1                 -1                   1   \n",
      "22                    1                 -1                  -1   \n",
      "23                   -1                 -1                   1   \n",
      "24                    1                 -1                  -1   \n",
      "25                   -1                  1                  -1   \n",
      "26                    1                 -1                  -1   \n",
      "27                   -1                 -1                  -1   \n",
      "28                   -1                 -1                  -1   \n",
      "29                   -1                 -1                  -1   \n",
      "\n",
      "    Genre:Thriller  Genre:Vampire  duration  episodes   type  user_score  year  \n",
      "0               -1             -1        23         5     TV          10  2011  \n",
      "1               -1              1        24         3     TV           7  2012  \n",
      "2                1             -1        23         4     TV           8  2006  \n",
      "3               -1             -1        24         3     TV          10  2013  \n",
      "4               -1             -1        23         3     TV           7  2007  \n",
      "5               -1             -1        24         2     TV           8  2013  \n",
      "6               -1             -1        23         2     TV           9  2014  \n",
      "7               -1             -1        25         1  Movie          10  2001  \n",
      "8               -1             -1        24         3     TV           7  2014  \n",
      "9               -1             -1        24         2     TV           7  2014  \n",
      "10              -1             -1        23         3     TV           9  2015  \n",
      "11              -1             -1        24         2     TV           9  2017  \n",
      "12              -1             -1        23         3     TV           8  2015  \n",
      "13              -1             -1        24         2     TV           7  2015  \n",
      "14              -1             -1        24         2     TV           7  2015  \n",
      "15              -1             -1        24         2     TV           9  2015  \n",
      "16              -1             -1        23         3     TV           9  2016  \n",
      "17              -1             -1        23         2     TV           8  2016  \n",
      "18               1             -1        25         3     TV           8  2016  \n",
      "19              -1             -1        24         2     TV           7  2016  \n",
      "20              -1             -1        24         2     TV           8  2016  \n",
      "21              -1             -1       146         1  Movie          10  2016  \n",
      "22              -1             -1        24         2     TV           6  2016  \n",
      "23              -1             -1        23         2     TV           9  2017  \n",
      "24              -1             -1        24         2     TV           9  2017  \n",
      "25              -1             -1        23         3     TV           8  2017  \n",
      "26              -1             -1        24         3     TV           7  2017  \n",
      "27              -1             -1       122         1  Movie           8  1995  \n",
      "28              -1             -1        23         5     TV           8  2000  \n",
      "29               1             -1        24         3     TV           9  2011  \n",
      "\n",
      "[30 rows x 34 columns]\n"
     ]
    }
   ],
   "source": [
    "print df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "y_train = df['user_score']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "6 Fine\n",
      "7 Good\n",
      "8 Very Good\n",
      "9 Great\n",
      "10 Masterpiece\n"
     ]
    }
   ],
   "source": [
    "for v in sorted(set(y_train.values)):\n",
    "    print v, class_names[v]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train = df.drop('user_score', axis = 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "    Genre:Action  Genre:Adventure  Genre:Comedy  Genre:Dementia  Genre:Demons  \\\n",
      "0              1                1            -1              -1            -1   \n",
      "1              1                1            -1              -1            -1   \n",
      "2             -1               -1            -1              -1            -1   \n",
      "3              1               -1            -1              -1            -1   \n",
      "4              1                1            -1              -1             1   \n",
      "5             -1               -1             1              -1            -1   \n",
      "6             -1                1             1              -1            -1   \n",
      "7             -1                1            -1              -1            -1   \n",
      "8              1                1            -1              -1            -1   \n",
      "9              1               -1            -1              -1            -1   \n",
      "10             1               -1             1              -1            -1   \n",
      "11             1               -1            -1              -1            -1   \n",
      "12             1                1            -1              -1            -1   \n",
      "13             1                1            -1              -1            -1   \n",
      "14            -1               -1            -1              -1            -1   \n",
      "15             1               -1             1              -1            -1   \n",
      "16             1               -1             1              -1            -1   \n",
      "17            -1                1             1              -1            -1   \n",
      "18            -1               -1            -1              -1            -1   \n",
      "19             1               -1             1              -1            -1   \n",
      "20             1               -1             1              -1            -1   \n",
      "21            -1               -1            -1              -1            -1   \n",
      "22            -1               -1             1              -1            -1   \n",
      "23            -1                1             1              -1            -1   \n",
      "24            -1               -1             1              -1            -1   \n",
      "25             1               -1             1              -1            -1   \n",
      "26            -1               -1            -1              -1            -1   \n",
      "27             1               -1            -1              -1            -1   \n",
      "28            -1                1            -1              -1            -1   \n",
      "29            -1               -1            -1              -1            -1   \n",
      "\n",
      "    Genre:Drama  Genre:Ecchi  Genre:Fantasy  Genre:Game  Genre:Harem  ...   \\\n",
      "0            -1           -1              1          -1           -1  ...    \n",
      "1            -1           -1             -1          -1           -1  ...    \n",
      "2            -1           -1             -1          -1           -1  ...    \n",
      "3             1           -1              1          -1           -1  ...    \n",
      "4            -1           -1              1          -1           -1  ...    \n",
      "5            -1            1              1          -1           -1  ...    \n",
      "6            -1            1              1           1           -1  ...    \n",
      "7             1           -1             -1          -1           -1  ...    \n",
      "8             1           -1             -1          -1           -1  ...    \n",
      "9             1           -1             -1          -1           -1  ...    \n",
      "10           -1           -1             -1          -1           -1  ...    \n",
      "11            1           -1              1          -1           -1  ...    \n",
      "12            1           -1             -1          -1           -1  ...    \n",
      "13           -1           -1              1          -1           -1  ...    \n",
      "14            1           -1             -1          -1           -1  ...    \n",
      "15           -1           -1             -1          -1           -1  ...    \n",
      "16           -1           -1             -1          -1           -1  ...    \n",
      "17           -1           -1              1          -1           -1  ...    \n",
      "18            1           -1              1          -1           -1  ...    \n",
      "19           -1           -1             -1          -1           -1  ...    \n",
      "20           -1           -1             -1          -1           -1  ...    \n",
      "21            1           -1             -1          -1           -1  ...    \n",
      "22           -1           -1             -1          -1           -1  ...    \n",
      "23           -1           -1              1          -1           -1  ...    \n",
      "24           -1           -1              1          -1           -1  ...    \n",
      "25           -1           -1             -1          -1           -1  ...    \n",
      "26           -1           -1              1          -1           -1  ...    \n",
      "27           -1           -1             -1          -1           -1  ...    \n",
      "28           -1           -1             -1           1           -1  ...    \n",
      "29           -1           -1             -1          -1           -1  ...    \n",
      "\n",
      "    Genre:Shounen  Genre:Slice of Life  Genre:Super Power  Genre:Supernatural  \\\n",
      "0               1                   -1                  1                  -1   \n",
      "1               1                   -1                 -1                   1   \n",
      "2               1                   -1                 -1                   1   \n",
      "3               1                   -1                  1                  -1   \n",
      "4               1                   -1                  1                   1   \n",
      "5              -1                   -1                 -1                  -1   \n",
      "6              -1                   -1                 -1                   1   \n",
      "7              -1                   -1                 -1                   1   \n",
      "8               1                   -1                 -1                   1   \n",
      "9              -1                   -1                 -1                   1   \n",
      "10              1                   -1                 -1                  -1   \n",
      "11              1                   -1                  1                  -1   \n",
      "12              1                   -1                 -1                   1   \n",
      "13             -1                   -1                 -1                  -1   \n",
      "14             -1                   -1                  1                  -1   \n",
      "15             -1                   -1                  1                   1   \n",
      "16              1                   -1                 -1                  -1   \n",
      "17             -1                   -1                 -1                   1   \n",
      "18             -1                   -1                 -1                  -1   \n",
      "19              1                   -1                  1                  -1   \n",
      "20             -1                    1                 -1                   1   \n",
      "21             -1                   -1                 -1                   1   \n",
      "22             -1                    1                 -1                  -1   \n",
      "23             -1                   -1                 -1                   1   \n",
      "24             -1                    1                 -1                  -1   \n",
      "25              1                   -1                  1                  -1   \n",
      "26              1                    1                 -1                  -1   \n",
      "27             -1                   -1                 -1                  -1   \n",
      "28              1                   -1                 -1                  -1   \n",
      "29             -1                   -1                 -1                  -1   \n",
      "\n",
      "    Genre:Thriller  Genre:Vampire  duration  episodes   type  year  \n",
      "0               -1             -1        23         5     TV  2011  \n",
      "1               -1              1        24         3     TV  2012  \n",
      "2                1             -1        23         4     TV  2006  \n",
      "3               -1             -1        24         3     TV  2013  \n",
      "4               -1             -1        23         3     TV  2007  \n",
      "5               -1             -1        24         2     TV  2013  \n",
      "6               -1             -1        23         2     TV  2014  \n",
      "7               -1             -1        25         1  Movie  2001  \n",
      "8               -1             -1        24         3     TV  2014  \n",
      "9               -1             -1        24         2     TV  2014  \n",
      "10              -1             -1        23         3     TV  2015  \n",
      "11              -1             -1        24         2     TV  2017  \n",
      "12              -1             -1        23         3     TV  2015  \n",
      "13              -1             -1        24         2     TV  2015  \n",
      "14              -1             -1        24         2     TV  2015  \n",
      "15              -1             -1        24         2     TV  2015  \n",
      "16              -1             -1        23         3     TV  2016  \n",
      "17              -1             -1        23         2     TV  2016  \n",
      "18               1             -1        25         3     TV  2016  \n",
      "19              -1             -1        24         2     TV  2016  \n",
      "20              -1             -1        24         2     TV  2016  \n",
      "21              -1             -1       146         1  Movie  2016  \n",
      "22              -1             -1        24         2     TV  2016  \n",
      "23              -1             -1        23         2     TV  2017  \n",
      "24              -1             -1        24         2     TV  2017  \n",
      "25              -1             -1        23         3     TV  2017  \n",
      "26              -1             -1        24         3     TV  2017  \n",
      "27              -1             -1       122         1  Movie  1995  \n",
      "28              -1             -1        23         5     TV  2000  \n",
      "29               1             -1        24         3     TV  2011  \n",
      "\n",
      "[30 rows x 33 columns]\n"
     ]
    }
   ],
   "source": [
    "print x_train"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn import preprocessing\n",
    "le = preprocessing.LabelEncoder()\n",
    "for attr in x_train.columns:\n",
    "    if x_train[attr].dtype == object:\n",
    "        x_train[attr] = le.fit_transform(x_train[attr])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[   1    1   -1   -1   -1   -1   -1    1   -1   -1   -1   -1   -1   -1   -1\n",
      "   -1   -1   -1   -1   -1   -1   -1   -1    1   -1    1   -1   -1   -1   23\n",
      "    5    1 2011]\n"
     ]
    }
   ],
   "source": [
    "print x_train.values[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(30, 34)"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn import tree\n",
    "clf = tree.DecisionTreeClassifier()\n",
    "clf = clf.fit(x_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'arvore.png'"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Visualizacao da Arvore\n",
    "import graphviz\n",
    "cn = []\n",
    "for v in sorted(set(y_train.values)):\n",
    "    cn.append(str(v) + \": \" + class_names[v])\n",
    "dot_data = tree.export_graphviz(clf, out_file=None,\n",
    "     feature_names=x_train.columns,\n",
    "     class_names=cn,\n",
    "     filled=True, rounded=True,\n",
    "     special_characters=True)\n",
    "graph = graphviz.Source(dot_data, format='png')\n",
    "graph.render('arvore', view=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Teste da Arvore de Decisao\n",
    "y_predicted = clf.predict(x_train)                # Realiza predicao no conjunto de testes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[   1    1   -1 ..., 2011   10   10]\n",
      " [   1    1   -1 ..., 2012    7    7]\n",
      " [  -1   -1   -1 ..., 2006    8    8]\n",
      " ..., \n",
      " [   1   -1   -1 ..., 1995    8    8]\n",
      " [  -1    1   -1 ..., 2000    8    8]\n",
      " [  -1   -1   -1 ..., 2011    9    9]]\n"
     ]
    }
   ],
   "source": [
    "# Conferir os resultados das predicoes\n",
    "import numpy as np                                  # Importa o pacote numpy, para consolidar os resultados\n",
    "classes = np.array([y_train]).T                 # Obtem um array das classes indicadas na base, para concatenar\n",
    "predicao = np.array([y_predicted]).T                # Obtem um array das predicoes na base, para concatenar\n",
    "print np.concatenate(                               # Concatena os atributos, classe indicada e predicao do classificador\n",
    "    (x_train, classes, predicao), axis=1)         # para cada instancia"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.0"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Avaliando o modelo criado\n",
    "clf.score(x_train, y_train)                   # Utiliza a metrica padrao de avaliacao do classificador"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
