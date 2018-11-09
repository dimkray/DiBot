# -*- coding: utf-8 -*-
# Сервис для получения информации о фильмах/кино
import Fixer
from kinopoisk.movie import Movie
from kinopoisk.person import Person

class Movies:
    # Найти фильм
    def Find(NameMovie):
        try:
            movie_list = Movie.objects.search(NameMovie)
            mMovies = []  # список найденных фильмов
            for iMovie in movie_list:
                mMovies.append([iMovie.id, iMovie.title, iMovie.title_en, iMovie.runtime, iMovie.rating, iMovie.votes])
            return mMovies
        except Exception as e:
            Fixer.errlog('Kinopoisk.Find', str(e))
            return '#bug: ' + str(e)

    # Контент фильма
    def GetContent(idMovie):
        try:
            movie = Movie(id=idMovie)
            movie.get_content('main_page')
            mMovie = []  # контент фильма
            mMovie.append(movie.title)
            mMovie.append(movie.title_en)
            mMovie.append(movie.year)
            mMovie.append(movie.runtime)
            mMovie.append(movie.rating)
            mMovie.append(movie.plot)
            print(mMovie)
            return mMovie
        except Exception as e:
            Fixer.errlog('Kinopoisk.GetContent', str(e))
            return '#bug: ' + str(e)