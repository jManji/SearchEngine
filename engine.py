import json, math
from collections import defaultdict

class ArtistsContainer(object):
    """
    This class has the implementation of our data container. Since we are
    only interested in age searching, the internal structure is a dictionary
    of lists. The key is the age and the value is a list of artists (ids). 
    This way we get O(1) complexity for fetching artists of a certain age.
    """
    artists_dict = defaultdict(list) # our internal artists container

    def get(self, index):
        """
        A simple getter for the container.
        
        Keyword arguments:
        index -- Index of the element in the container
        """
        return self.artists_dict[index]
        
    def add(self, item):
        """
        Appends an artist entry to the container.
        
        Keyword arguments:
        artists_file -- the json input data file (default "")
        """
        self.artists_dict[item.get('age')].append(item)
        
    def clear(self):
        self.artists_dict.clear()

class SearchEngine(object):
    """
    The main logic of the service. It is responsible for loading, searching
    and getting the data.
    """
    data_dict = [] # artists data as loaded from json
    artists = ArtistsContainer()
    
    def __init__(self, artists_file = ""):
        """
        Contructor. If a json data file is given, it parses and loads
        its contents. Unit tests can use the default, blank, parameter.
        
        Keyword arguments:
        artists_file -- the json input data file (default "")
        """
        if artists_file:
            with open(artists_file) as data_file:    
                self.data_dict = json.load(data_file)["artists"]
            self.create_container(self.data_dict)

    def search(self, min_str, max_str):
        """
        Returns the artists in the range, favouring the ones in the middle. 
        
        Keyword arguments:
        min_str -- the minimum age of the range
        max_str -- the maximum age of the range
        """
        return_list = [] # the list to be returned as a response
        
        min = int(min_str)
        max = int(max_str)
        # for even number range, steps is range+1, for odd it's range+2
        steps = int(math.ceil((max - min) / 2.0) * 2) + 1
        # mid of the range is the average, for odd range younger is preferred
        mid = (max + min)/2
        
        # We start from the middle. We want the sign to change every step, and the
        # offset from the middle to increase every second step. So for a specific
        # number of steps, we use division on ints to keep the offset the same on
        # two consecutive steps. For instance, for a range 30 - 34, this means we have
        # the offsets: 0, -1, 1, -2, 2 that are then being added to the middle, 32. 
        # Doing that, we have 32, 31, 33, 30, 34
        for step in range(steps):
            index = -1
            if step % 2 == 0:
                index = mid + step / 2
            else:
                # add this check to skip the one before the last step, for odd steps
                if (mid - (step / 2 + 1) >= min): 
                    index = mid - (step / 2 + 1)
            if (index != -1): # we only add when an index was found
                if self.artists.get(index): # if artists of that age exist, append them
                    return_list += self.artists.get(index)
                    
        return return_list
        
    def add_artist(self, artist):
        """
        Adds an artist element to container, and hence to the engine
        
        Keyword arguments:
        artist -- the artist to be added, is a dictionary of age and uuid
        """
        self.artists.add(artist)
        
    def create_container(self, data_dict):
        """
        Populates the container of the artists
        
        Keyword arguments:
        data_dict -- the artists data dictionary
        """
        for artist in data_dict:
            self.add_artist(artist)
            
