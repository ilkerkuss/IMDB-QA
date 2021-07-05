#

"""
1- cache system
2- regex for
3- write decorator for caching

main:
	question
	qt list
	-> apply

class:
	has a func to decide if its question

regex to choose from qt's
function to return answer

"""
import re
from imdb_parser import *
import datetime


class QuestionType(object):
    def __init__(self, regex_rule_list, func):
        self.regex_rule_list = regex_rule_list
        self.func = func
        self.correct_regex = None

    def is_mine(self, question):
        for regex_rule in self.regex_rule_list:
            if re.match(regex_rule, question):
                self.correct_regex = regex_rule
                return True
        return False

    def answer_it(self, question):
        return self.func(self.correct_regex, question)


# how old is actor
how_old_is_actor_regex = [r"How old is (.+)\?", "How many years did (.+) lived\?"]


def how_old_is_actor_func(regex, question):
    actor_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(actor_name)
    actor = Actor(imdb_link).fillData()
    return actor_name + " is now " + str(actor.age) + " years old."


which_movies_actor_played_in_regex = [r"Which movies did (.+) play?", r"Which movies (.+) played?"]


def which_movies_actor_played_in_func(regex, question):
    actor_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(actor_name)
    actor = Actor(imdb_link).fillData()
    return actor.movies


when_did_the_movie_release_regex = [r"When did (.+) release?", r"When (.+) released at?",
                                    r"When did (.+) come to the theaters?", r"When did (.+) come out?",
                                    r"Which year did (.+) come out?"]


def when_did_the_movie_release_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return movie_name + " released at " + str(movie.date_released)


which_actors_did_play_regex = [r"Which actors did play at (.+)?", r"Which ones did play at (.+)?",
                               r"Who did play at(.+)?", r"Who played at (.+)?", r"What was the cast of (.+)?"]


def which_actors_did_play_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return "The list of Actor/Actress played at " + movie_name + " : \n" + str(movie.cast)


who_is_the_director_of_film_regex = [r"Who is the director of (.+)?", r"Who directed (.+)?",
                                     r"What is the director of (.+)?", r"Which director did direct (.+)?",
                                     r"What was the name of director for (.+)?"]


def who_is_the_director_of_film_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return movie.director + " directed the " + movie_name


what_is_the_rating_point_of_film_regex = [r"What is the rating point of the (.+)?", r"How much point did (.+) take?",
                                          r"How many point did (.+) take?", r"What point did (.+) take?",
                                          r"What was the point of (.+)?"]


def what_is_the_rating_point_of_film_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return movie_name + " 's rating point is " + movie.rating


what_is_the_budget_of_film_regex = [r"What is the budget of (.+)?", r"What was the budget of (.+)?",
                                    r"How much money did (.+) earn?", r"How much did they earn from (.+)?",
                                    r"What was the income of (.+)?"]


def what_is_the_budget_of_film_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return "  The Budget of  " + movie_name + " is " + movie.budget


what_is_the_genre_of_film_regex = [r"What is the genre of (.+)?", r"What kind of genre does (.+) have?",
                                   r"What is the type of (.+)?", r"Which category is (.+) in ?",
                                   r"Which genre does (.+) have?"]


def what_is_the_genre_of_film_func(regex, question):
    movie_name = re.search(regex, question, re.I).group(1)
    imdb_link = search_imdb(movie_name)
    movie = Movie(imdb_link).fillData()
    return " The Genre of " + movie_name + " is " + movie.genre


def get_questions():
    q_list = []
    q_list.append(QuestionType(how_old_is_actor_regex, how_old_is_actor_func))
    q_list.append(QuestionType(which_movies_actor_played_in_regex, which_movies_actor_played_in_func))
    q_list.append(QuestionType(when_did_the_movie_release_regex, when_did_the_movie_release_func))
    q_list.append(QuestionType(which_actors_did_play_regex, which_actors_did_play_func))
    q_list.append(QuestionType(who_is_the_director_of_film_regex, who_is_the_director_of_film_func))
    q_list.append(QuestionType(what_is_the_rating_point_of_film_regex, what_is_the_rating_point_of_film_func))
    q_list.append(QuestionType(what_is_the_budget_of_film_regex, what_is_the_budget_of_film_func))
    q_list.append(QuestionType(what_is_the_genre_of_film_regex, what_is_the_genre_of_film_func))
    return q_list


def test():
    question_str = 'When did star wars release?'
    questions = get_questions()
    for question in questions:
        if question.is_mine(question_str):
            print(question.answer_it(question_str))


test()