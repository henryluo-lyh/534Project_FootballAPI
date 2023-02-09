import unittest
import pandas as pd

import sys
sys.path.insert(0, sys.path[0][:-4])
sys.path.insert(0, sys.path[0]+'Football_API')

# for i in sys.path:
#     print(i)

from search_process import *
from unittest.mock import patch


class TestProcess(unittest.TestCase):
    
    
    def test_trim_df(self):
        
        # import os
        # print(os.getcwd())
        
        df = pd.read_csv('./total-players.csv')
        df = trim_df(df)
        self.assertIsNotNone(df)
    
    @patch("builtins.input")
    def test_search(self, mock_input):
        
        df = pd.read_csv('./total-players.csv')
        
        mock_input.side_effect=['Son', 2022]
        df = search(df)
        self.assertIsNotNone(df)


    @patch("builtins.input")
    @patch("search_process.search")
    def test_process_df(self, mock_search, mock_input):
        
        import os
        print(os.getcwd())
        
        import io
        import sys
        import urllib.request
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
        
        df = pd.read_csv('total-players.csv', encoding='utf_8_sig')
        
        rs = df[( df['player.name'].str.contains(r'.*Son.*')) & (df['league.season'] == 2022)]
        mock_search.side_effect=[rs, rs]
        mock_input.side_effect=[186, 3398]
        
        df = search_players(df)
        
        df = process_df(df)
        
        self.assertIsNotNone(df)
    
    

    
    
    
    
    

unittest.main(argv=[''], verbosity=2, exit=False)