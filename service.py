#!flask/bin/python
from flask import Flask, request
from flask.views import View
import json, engine

app = Flask(__name__)

class SearchService(View):
    """
    The search engine service. It uses a json input file to
    instantiate the engine and contains the API.
    """
    
    engine = engine.SearchEngine('artists.json')
    
    def search(self, min, max):
        """
        The endpoint for the artists interface. It calls
        the engine with min and max parameters.
        """
        return json.dumps(self.engine.search(min, max))
    
    # Needs to be implemented for View
    def dispatch_request(self):
        if request.method == 'GET':
            return self.search(request.args.get('min'), request.args.get('max'))
            
app.add_url_rule('/search_engine/artists', view_func=SearchService.as_view('search'))
        
if __name__ == '__main__':
    app.run()
    