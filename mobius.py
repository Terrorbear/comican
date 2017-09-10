__doc__ = """
Keeps track of inventory.
"""

import os
import pandas as pd
from alexandria.dewey import HEADERS, INDICES


class MobiusChair(object):
    _chair_stats_ = {}

    def __init__(self, *args, **kwargs):
        self.df = None  # so del works
        self.inv_path = os.path.join(
            os.path.dirname(__file__),
            'storage',
            'inventory.csv'
        )
        in_use = self._chair_stats_.get('inUse', False)
        if in_use:
            raise Exception('Only one MobiusChair can exist at a time!')
        self._chair_stats_['inUse'] = True
        if os.path.exists(self.inv_path):
            self.df = pd.read_csv(self.inv_path)
        else:
            self.df = pd.DataFrame(columns=HEADERS)
        self.df.set_index(INDICES, inplace=True)

    def __del__(self):
        if self.df is None:
            return
        self.df.to_csv(self.inv_path)

    def _add_df(self, df, subtract=False):
        d = df.reset_index().to_dict()
        for v in d.values():
            self._add_dict(self, d, subtract)

    def _add_dict(self, data, subtract=False):
        try:
            key = [data[k] for k in INDICES]
            copies = -data['Copies'] if subtract else data['Copies']
            self.df.loc[key]['Copies'] += copies
        except:
            self.df.append(data)
