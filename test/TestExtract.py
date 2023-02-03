import unittest
import pandas as pd

import sys
sys.path.insert(0, sys.path[0][:-4])
sys.path.insert(0, sys.path[0]+'Project_FootballAPI')

for i in sys.path:
    print(i)

import Project_FootballAPI.extract as et



class TestExtract(unittest.TestCase):
    
    def test_json2dict(self):
        data = "[ { \"a\" : 1} ]"
        self.assertEqual( et.json2dict(data), [{'a': 1}])
    
    def test_build_query(self):
        self.assertEqual( et.build_query('1', '1'), '11')
    
    def test_call_api(self):
        base_url = "https://api-football-v1.p.rapidapi.com/v3/"
        self.assertEqual( str(et.call_api(base_url, 'players', {'league':39, 'season':2020, 'page':1})), '<Response [200]>')
    
    def test_get_players_json_data(self):
        response = et.get_players_json_data(1, 1, page=1)
        self.assertIsNotNone(str(response))
    
    def test_get_all_players(self):
        response = et.get_all_players([1], [1])
        self.assertIsNotNone(response)
        
    def test_get_2_players_data(self):
        
        dict = {
        'league': [],
        'season': []
        }

        df = pd.DataFrame(dict)

        df.to_csv('input_record.csv',
                encoding='utf_8_sig',
                mode='a',
                index=False,
                index_label=False
        )
        
        response = et.get_2_players_data(39, 2008, 40, 2009)
        self.assertIsNotNone(response)

    def test_get_2_players_data_multithread(self):
        
        dict = {
        'league': [],
        'season': []
        }

        df = pd.DataFrame(dict)

        df.to_csv('input_record.csv',
                encoding='utf_8_sig',
                mode='a',
                index=False,
                index_label=False
        )
        
        response = et.get_2_players_data_multithread(39, 2008, 40, 2009)
        self.assertIsNotNone(response)

unittest.main(argv=[''], verbosity=2, exit=False)