import engine, json, unittest
 
class TestContainer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.container = engine.ArtistsContainer()
        self.container.add({'age': 30, 'uuid': 'artist1'})
        self.container.add({'age': 30, 'uuid': 'artist2'})
        self.container.add({'age': 32, 'uuid': 'artist3'})
        
    @classmethod
    def tearDownClass(self):
        self.container.clear()
        self.container = None
        
    def test_container_one_artist(self):
        self.assertEqual(self.container.get(32), [{'age': 32, 'uuid': 'artist3'}])
        
    def test_container_two_artists(self):
        self.assertEqual(self.container.get(30),
                         [{'age': 30, 'uuid': 'artist1'}, {'age': 30, 'uuid': 'artist2'}])
                         
    def test_container_no_artist(self):
        self.assertEqual(self.container.get(33), [])

class TestEngine(unittest.TestCase):

    @classmethod    
    def setUpClass(self):
        self.engine = engine.SearchEngine()
        self.engine.create_container([{'age': 30, 'uuid': 'artist01'},
                                      {'age': 25, 'uuid': 'artist02'},
                                      {'age': 30, 'uuid': 'artist03'},
                                      {'age': 45, 'uuid': 'artist04'},
                                      {'age': 36, 'uuid': 'artist05'},
                                      {'age': 38, 'uuid': 'artist06'},
                                      {'age': 37, 'uuid': 'artist07'},
                                      {'age': 41, 'uuid': 'artist08'},
                                      {'age': 32, 'uuid': 'artist09'},
                                      {'age': 33, 'uuid': 'artist10'},
                                      {'age': 45, 'uuid': 'artist11'},
                                      {'age': 34, 'uuid': 'artist12'},
                                      {'age': 46, 'uuid': 'artist13'}])

    def test_engine_single_age(self):
        expected = [{'age': 37, 'uuid': 'artist07'}]
        self.assertEqual(self.engine.search('37', '37'), expected)
        
    def test_engine_odd_age_range(self):
        expected = [
            {
                "age": 32,
                'uuid': 'artist09',
            },
            {
                "age": 33,
                'uuid': 'artist10',
            },
            {
                "age": 30,
                'uuid': 'artist01',
            },
            {
                "age": 30,
                'uuid': 'artist03',
            },
            {
                "age": 34,
                'uuid': 'artist12',
            }
        ]
        self.assertEqual(self.engine.search('30', '34'), expected)

    def test_engine_odd_even_range(self):
        expected = [
            {
                "age": 33,
                'uuid': 'artist10',
            },
            {
                "age": 32,
                'uuid': 'artist09',
            },
            {
                "age": 34,
                'uuid': 'artist12',
            },
            {
                "age": 36,
                'uuid': 'artist05',
            }
        ]
        self.assertEqual(self.engine.search('31', '36'), expected)

    def test_engine_two_ages(self):
        expected = [
            {
                "age": 45,
                'uuid': 'artist04',
            },
            {
                "age": 45,
                'uuid': 'artist11',
            },
            {
                "age": 46,
                'uuid': 'artist13',
            }
        ]
        self.assertEqual(self.engine.search('45', '46'), expected)
        
    def test_engine_non_existent_ages(self):
        expected = []
        self.assertEqual(self.engine.search('55', '63'), expected)
        
    def test_engine_invalid_range(self):
        expected = []
        self.assertEqual(self.engine.search('39', '31'), expected)
    
        
if __name__ == '__main__':
    unittest.main()