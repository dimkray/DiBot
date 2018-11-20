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
            Fixer.errlog('Kinopoisk.Movies.Find', str(e))
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
            mMovie.append(movie.votes)
            mMovie.append(movie.imdb_rating)
            mMovie.append(movie.imdb_votes)
            mMovie.append(movie.plot)
            mMovie.append(movie.tagline)
            mMovie.append(movie.genres)
            mMovie.append(movie.countries)
            mMovie.append(movie.actors)
            mMovie.append(movie.directors)
            mMovie.append(movie.screenwriters)
            mMovie.append(movie.producers)
            mMovie.append(movie.budget)
            mMovie.append(movie.profit_world)
            movie.get_content('trailers')
            mMovie.append(movie.trailers)
            mMovie.append(movie.youtube_ids)
            # trailers_ids = [trailer.id for trailer in movie.trailers]
            # trailers_files = [trailer.file for trailer in movie.trailers]
            movie.get_content('cast')
            mMovie.append(movie.cast['actor'])
            mMovie.append(movie.cast['voice'])
            mMovie.append(movie.cast['producer'])
            movie.get_content('series')
            mMovie.append(movie.seasons)
            print(mMovie)
            return mMovie
        except Exception as e:
            Fixer.errlog('Kinopoisk.Movies.GetContent', str(e))
            return '#bug: ' + str(e)


class Persons:
    # Найти персонажа (актёра, режиссёра)
    def Find(NamePerson):
        try:
            person_list = Person.objects.search(NamePerson)
            print(person_list)
            mPersons = []  # список найденных персонажей
            for iPerson in person_list:
                year_death = None
                try:
                    year_death = iPerson.year_death
                except:
                    year_death = None
                mPersons.append([iPerson.id, iPerson.name, iPerson.name_en, iPerson.year_birth, year_death])
            print(mPersons)
            return mPersons
        except Exception as e:
            Fixer.errlog('Kinopoisk.Persons.Find', str(e))
            return '#bug: ' + str(e)

    # Контент персонажа
    def GetContent(idPerson):
        try:
            person = Person(id=idPerson)
            person.get_content('main_page')
            mPerson = []  # контент персонажа
            mPerson.append(person.name)
            mPerson.append(person.name_en)
            mPerson.append(person.year_birth)
            year_death = None
            try:
                year_death = person.year_death
            except:
                year_death = None
            mPerson.append(year_death)
            mPerson.append(person.information)
            mPerson.append(person.career['actor'])
            mPerson.append(person.career['producer'])
            mPerson.append(person.career['director'])
            mPerson.append(person.career['writer'])
            mPerson.append(person.career['hrono_titr_male'])
            mPerson.append(person.career['himself'])
            person.get_content('photos')
            mPerson.append(person.photos)
            print(mPerson)
            return mPerson
        except Exception as e:
            Fixer.errlog('Kinopoisk.Persons.GetContent', str(e))
            return '#bug: ' + str(e)
