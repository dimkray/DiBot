# -*- coding: utf-8 -*-
# Сервис для получения информации о фильмах/кино
import fixer
from kinopoisk.movie import Movie
from kinopoisk.person import Person

class Movies:
    # Найти фильм
    def Find(NameMovie):
        try:
            movie_list = Movie.objects.search(NameMovie)
            mMovies = []  # список найденных фильмов
            for iMovie in movie_list:
                mMovies.append([iMovie.id, iMovie.title, iMovie.title_en, iMovie.runtime, iMovie.year,
                iMovie.rating, iMovie.votes])
            return mMovies
        except Exception as e:
            Fixer.errlog('Kinopoisk.Movies.Find', str(e))
            return '#bug: ' + str(e)

    # Контент фильма
    def GetContent(idMovie):
        try:
            movie = Movie(id=idMovie)
            movie.get_content('main_page')
            dMovie = {}  # контент фильма
            dMovie['title'] = movie.title
            dMovie['title_en'] = movie.title_en
            dMovie['year'] = movie.year
            dMovie['runtime'] = movie.runtime
            dMovie['rating'] = movie.rating
            dMovie['votes'] = movie.votes
            dMovie['imdb_rating'] = movie.imdb_rating
            dMovie['imdb_votes'] = movie.imdb_votes
            dMovie['plot'] = movie.plot
            dMovie['tagline'] = movie.tagline
            dMovie['genres'] = movie.genres
            dMovie['countries'] = movie.countries
            dMovie['actors'] = movie.actors
            dMovie['directors'] = movie.directors
            dMovie['writers'] = movie.screenwriters
            dMovie['producers'] = movie.producers
            dMovie['budget'] = movie.budget
            dMovie['profit'] = movie.profit_world
            movie.get_content('trailers')
            dMovie['youtube_ids'] = movie.youtube_ids
            dMovie['trailers'] = [trailer.file for trailer in movie.trailers]
            movie.get_content('cast')
            actors = movie.cast['actor']
            mActors = []
            for actor in actors:
                mActors.append({'id': actor.person.id, 'name': actor.person.name, 'name_en': actor.person.name,
                                'names': actor.name})
            dMovie['actors_full'] = mActors
            if 'voice' in movie.cast:
                voices = movie.cast['voice']
                mVoices = []
                for voice in voices:
                    mVoices.append({'id': voice.person.id, 'name': voice.person.name, 'name_en': voice.person.name,
                                    'names': voice.name})
                dMovie['voices'] = mVoices
            else:
                dMovie['voices'] = []
            producers = movie.cast['producer']
            mProducers = []
            for producer in producers:
                mProducers.append({'id': producer.person.id, 'name': producer.person.name, 'name_en': producer.person.name})
            dMovie['producers_full'] = mProducers
            # movie.get_content('series')
            # series = movie.seasons
            # mseries = []
            # for serie in series:
            #     mVoices.append({'id': producer.person.id, 'name': producer.person.name, 'name_en': producer.person.name})
            # dMovie['seasons'] = movie.seasons
            return dMovie
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
            return mPersons
        except Exception as e:
            Fixer.errlog('Kinopoisk.Persons.Find', str(e))
            return '#bug: ' + str(e)

    # Контент персонажа
    def GetContent(idPerson):
        try:
            person = Person(id=idPerson)
            person.get_content('main_page')
            dPerson = {}  # контент персонажа
            dPerson['name'] = person.name
            dPerson['name_en'] = person.name_en
            dPerson['year_birth'] = person.year_birth
            try:
                year_death = person.year_death
            except:
                year_death = None
            dPerson['year_death'] = year_death
            dPerson['information'] = person.information
            if 'actor' in person.career:
                roles = person.career['actor']
                mActors = []
                for role in roles:
                    mActors.append({'id': role.movie.id, 'name': role.name, 'title': role.movie.title_en,
                                    'title_en': role.movie.title, 'year': role.movie.year, 'rating': role.movie.rating})
                dPerson['actor'] = mActors
            else:
                dPerson['actor'] = []
            if 'producer' in person.career:
                roles = person.career['producer']
                mActors = []
                for role in roles:
                    mActors.append({'id': role.movie.id, 'name': role.name, 'title': role.movie.title_en,
                                    'title_en': role.movie.title, 'year': role.movie.year, 'rating': role.movie.rating})
                dPerson['producer'] = mActors
            else:
                dPerson['producer'] = []
            if 'director' in person.career:
                roles = person.career['director']
                mActors = []
                for role in roles:
                    mActors.append({'id': role.movie.id, 'name': role.name, 'title': role.movie.title_en,
                                    'title_en': role.movie.title, 'year': role.movie.year, 'rating': role.movie.rating})
                dPerson['director'] = mActors
            else:
                dPerson['director'] = []
            if 'writer' in person.career:
                roles = person.career['writer']
                mActors = []
                for role in roles:
                    mActors.append({'id': role.movie.id, 'name': role.name, 'title': role.movie.title,
                                    'title_en': role.movie.title_en, 'year': role.movie.year, 'rating': role.movie.rating})
                dPerson['writer'] = mActors
            else:
                dPerson['writer'] = []
            person.get_content('photos')
            dPerson['photos'] = person.photos
            return dPerson
        except Exception as e:
            Fixer.errlog('Kinopoisk.Persons.GetContent', str(e))
            return dPerson  #'#bug: ' + str(e)
