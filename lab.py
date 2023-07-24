"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    Takes in data stored in Films database
    Creates dict that maps actor to
    list of who they acted with
    """
    transformed_data = {}
    transformed_data_actors = {}  # actors map to co-actors
    transformed_data_movies = {}  # movies map to actors acted in movie

    for actor in raw_data:
        # print(actor)
        if actor[0] != actor[1]:  # not counting self
            if actor[0] in transformed_data_actors:  # if actor in dict
                transformed_data_actors[actor[0]].add(actor[1])  # set to not repeat
            else:
                transformed_data_actors[actor[0]] = {actor[1]}
            if actor[1] in transformed_data_actors:
                transformed_data_actors[actor[1]].add(actor[0])
            else:
                transformed_data_actors[actor[1]] = {actor[0]}

    for movie in raw_data:
        if movie[2] in transformed_data_movies:
            transformed_data_movies[movie[2]].add(movie[0])
            transformed_data_movies[movie[2]].add(movie[1])
        else:
            transformed_data_movies[movie[2]] = {movie[0]}
            transformed_data_movies[movie[2]].add(movie[1])

    transformed_data["actor_dict"] = transformed_data_actors
    transformed_data["movies_dict"] = transformed_data_movies

    return transformed_data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Returns True if actor1 and actor2 acted
            False if not
    """
    # transformed_data = transform_data(transformed_data)
    return bool(
        actor_id_2 in transformed_data["actor_dict"][actor_id_1]
        or actor_id_1 == actor_id_2
    )


def actors_with_bacon_number(transformed_data, n):
    """
    Return set with ID numbers of all the actors
    with that Bacon number
    """
    # transformed_data = transform_data(transformed_data)

    bacon_dict = {0: {4724}}

    tot_set = {4724}

    for i in range(0, n):
        for actor in bacon_dict[i]:
            tot_set.add(actor)  # all actors w num
            for act in transformed_data["actor_dict"][actor]:
                if i + 1 in bacon_dict and act not in tot_set:  # adds actors to i+1
                    bacon_dict[i + 1].add(act)
                elif i + 1 not in bacon_dict and act not in tot_set:
                    bacon_dict[i + 1] = {act}
                tot_set.add(act)
        if i + 1 not in bacon_dict:  # if i+1 has no actors
            return set()

    if n in bacon_dict:
        return bacon_dict[n]
    else:
        return set()


def id_path(transformed_data, actor_id, actor_id_two):
    """
    Returns paths of actor ID
    between actor_id and actor_id_two
    """
    agenda = [actor_id]
    visited = {actor_id}
    bacon_dict = {actor_id: actor_id}
    path_lst = []

    while agenda:  # haven't found actor_id
        current_actor = agenda.pop(0)

        for actor in transformed_data["actor_dict"][current_actor]:  # neighbours
            if actor not in visited:  # actors looked at
                bacon_dict[actor] = current_actor  # assign actor to parent
                if actor == actor_id_two:
                    parent_actor = actor
                    while parent_actor != actor_id:  # make list
                        path_lst.append(parent_actor)
                        parent_actor = bacon_dict[parent_actor]
                    return [actor_id] + path_lst[::-1]

                else:  # change agenda and visited
                    agenda.append(actor)
                    visited.add(actor)


def bacon_path(transformed_data, actor_id):
    """
    Return: list of actor IDs (any such shortest list if there are several)
    detailing a "Bacon path" from Kevin Bacon to actor_id.
    If no path exists, return None.
    """
    # transformed_data = transform_data(transformed_data)

    return id_path(transformed_data, 4724, actor_id)

    # agenda = [4724]
    # visited = {4724}
    # bacon_dict = {4724: 4724}
    # path_lst = []

    # while agenda:  # haven't found actor_id
    #     current_actor = agenda.pop(0)

    #     for actor in transformed_data["actor_dict"][current_actor]:  # neighbours
    #         if actor not in visited:  # actors looked at
    #             bacon_dict[actor] = current_actor  # assign actor to parent
    #             if actor == actor_id:
    #                 parent_actor = actor
    #                 while parent_actor != 4724:  # make list
    #                     path_lst.append(parent_actor)
    #                     parent_actor = bacon_dict[parent_actor]

    #                 return [4724] + path_lst[::-1]

    #             else:  # change agenda and visited
    #                 agenda.append(actor)
    #                 visited.add(actor)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Return: list of actor IDs (any such shortest list if there are several)
    detailing a "Bacon path" from actor_id_1 to actor_id_2.
    If no path exists, return None.
    """
    # transformed_data = transform_data(transformed_data)

    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    else:
        return id_path(transformed_data, actor_id_1, actor_id_2)

    # agenda = [actor_id_1]
    # visited = {actor_id_1}
    # bacon_dict = {actor_id_1: actor_id_1}
    # path_lst = []

    # if actor_id_1 == actor_id_2:
    #         return [actor_id_1]
    # else:
    #     while agenda:  # haven't found actor_id
    #         current_actor = agenda.pop(0)

    #         for actor in transformed_data["actor_dict"][current_actor]:  # neighbours
    #             if actor not in visited:  # actors looked at
    #                 bacon_dict[actor] = current_actor  # assign actor to parent
    #                 if actor == actor_id_2:
    #                     parent_actor = actor
    #                     while parent_actor != actor_id_1:  # make list
    #                         path_lst.append(parent_actor)
    #                         parent_actor = bacon_dict[parent_actor]
    #                     return [actor_id_1] + path_lst[::-1]

    #                 else:  # change agenda and visited
    #                     agenda.append(actor)
    #                     visited.add(actor)


def movie_path(raw_data, transformed_data, actor_id_1, actor_id_2):
    """
    Return movie name path between
    2 actors
    """
    # transformed_data = transform_data(transformed_data)

    movie_lst = []
    named_movies_path = []
    actor_path_lst = actor_to_actor_path(
        transformed_data["actor_dict"], actor_id_1, actor_id_2
    )

    for i in range(len(actor_path) - 1):
        for tup in raw_data:
            if actor_path_lst[i] in tup and actor_path_lst[i + 1] in tup:
                movie_lst.append(
                    tup[2]
                )  # movie id if both adjacent actors in raw_data tup
                break

    with open("resources/movies.pickle", "rb") as movie:
        moviedb = pickle.load(movie)
        key_list = list(moviedb.keys())
        val_list = list(moviedb.values())

    for movie_id in movie_lst:
        named_movies_path.append(key_list[val_list.index(movie_id)])

    return named_movies_path


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Return: a list containing actor IDs,
    representing the shortest possible path from actor_id_1
    to any actor that satisfies the goal-test function.
    Otherwise, return None
    """
    # transformed_data = transform_data(transformed_data)

    agenda = [actor_id_1]
    visited = {actor_id_1}
    bacon_dict = {actor_id_1: actor_id_1}
    path_lst = []

    if goal_test_function(actor_id_1):
        return [actor_id_1]
    else:
        while agenda:  # haven't found actor_id
            current_actor = agenda.pop(0)

            for actor in transformed_data["actor_dict"][current_actor]:  # neighbours
                if actor not in visited:  # actors looked at
                    bacon_dict[actor] = current_actor  # assign actor to parent
                    if goal_test_function(actor):
                        parent_actor = actor
                        while parent_actor != actor_id_1:  # make list
                            path_lst.append(parent_actor)
                            parent_actor = bacon_dict[parent_actor]
                        return [actor_id_1] + path_lst[::-1]

                    else:  # change agenda and visited
                        agenda.append(actor)
                        visited.add(actor)


def actors_connecting_films(transformed_data, film1, film2):
    """
    Return: shortest possible list of actor ID numbers (in order) 
    that connect those two films. Your list should begin with the 
    ID number of an actor who was in the first film, and it should 
    end with the ID number of an actor who was in the second film.
    If there is no path connecting those two films, your function should return None.
    """
    lst_of_paths = []
    for actor1 in transformed_data["movies_dict"][film1]:
        for actor2 in transformed_data["movies_dict"][film2]:
            path = actor_to_actor_path(transformed_data, actor1, actor2)
            lst_of_paths.append(path)  # all paths btwn actors in film1 & film2

    min_path = min(lst_of_paths, key=lambda x: len(x))  # min path

    return min_path


if __name__ == "__main__":
    # with open("resources/small.pickle", "rb") as f:
    #     smalldb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    # with open("resources/names.pickle", "rb") as f:
    #     namesdb = pickle.load(f)
    #     key_list = list(namesdb.keys())
    #     val_list = list(namesdb.values())
    #     position1 = val_list.index(131431)
    #     position2 = val_list.index(29986)
    #     position3 = val_list.index(13550)
    #     position4 = val_list.index(57755)
    # print(key_list[position1], key_list[position2],
    #       key_list[position3], key_list[position4])

    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)
    # print(actor_to_actor_path(tinydb, 1640, 1532))
    # print(tinydb)
    print(transform_data(tinydb))
    # print(actors_with_bacon_number(tinydb, 2))

    # with open("resources/small.pickle", "rb") as f:
    #     smalldb = pickle.load(f)
    # with open("resources/names.pickle", "rb") as g:
    #     namesdb = pickle.load(g)
    # print(namesdb['Sten Hellstrom'], namesdb['Yveline Ailhaud'])
    # print(namesdb['Louise Devar'], namesdb['Adriana Morera'])
    # print(acted_together(smalldb, 572600, 558335))
    # print(acted_together(smalldb, 1059004, 1059007))

    # with open("resources/large.pickle", "rb") as f:
    #         largedb = pickle.load(f)
    # with open("resources/names.pickle", "rb") as g:
    #         namesdb = pickle.load(g)
    # # print(namesdb['Natalie Portman'], namesdb['Vjeran Tin Turk'])
    # # print(actor_to_actor_path(transform_data(largedb), 524, 1367972))
    # print(movie_path(largedb, transform_data(largedb), 524,1367972 ))

    # with open("resources/tiny.pickle", "rb") as f:
    #     tinydb = pickle.load(f)
    # print(movie_path(tinydb, transform_data(tinydb), 1640, 1532 ))
