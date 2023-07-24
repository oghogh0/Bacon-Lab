<h1>Bacon Lab</h1>
<h2>Description</h2>
Actors and movies are represented as ID numbers.<br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
TRANSFORM the data in the Films database:<br/>
This function creates 2 dictionaries. One maps an actor to a list of people they have acted with. The other maps a movie to the actors in the movie. <br/>

    transformed_data = {}
    transformed_data_actors = {}  # actors map to co-actors
    transformed_data_movies = {}  # movies map to actors acted in movie

    for actor in raw_data:
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

<br/>
<p align="left">
Determine if two actors have been in the SAME MOVIE together.<br/>
This function returns a boolean value determined by if both actors have acted together or not.<br/>

    # transformed_data = transform_data(transformed_data)
    
    return bool(
        actor_id_2 in transformed_data["actor_dict"][actor_id_1]
        or actor_id_1 == actor_id_2
    )

<br/>
<p align="left">
Actors BACON NUM:<br/>
A Bacon number is defined as the smallest number of films separating a given actor from Kevin Bacon, whose actor ID is 4724. This function returns the set of all actors who have a given Bacon number.<br/>


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



<br/>
<p align="left">
KEVIN BACON:<br/>
In this part, the goal is to find the chain of actors that connects Kevin Bacon to someone else. The main function used here is 'id_path'. <br/> 
Firstly, by producing a list of actor IDs (any such shortest list if there are several) detailing a "Bacon path" from Kevin Bacon to an actor. If no path exists, return None. It is important to consider that the paths are not necessarily unique, hence any shortest list that connects Bacon to the actor denoted by actor_id is valid.<br/> 
    
    # transformed_data = transform_data(transformed_data)

    return id_path(transformed_data, 4724, actor_id)

Secondly, I would like to expand on the previous function by producing a list of actor IDs (any such shortest list if there are several) detailing a "Bacon path" between any 2 arbitrary actors. If no path exists, return None.<br/> 

    # transformed_data = transform_data(transformed_data)

    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    else:
        return id_path(transformed_data, actor_id_1, actor_id_2)



The function 'id_path' returns the path of actor IDs between two actors. This is useful because both functions above are the same, except the first actor will always be Kevin Bacon for the first function. In that case, we can use this function in both cases. <br/>

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
