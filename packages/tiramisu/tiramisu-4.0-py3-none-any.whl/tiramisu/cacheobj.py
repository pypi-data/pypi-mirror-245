# -*- coding: utf-8 -*-
"cache used by storage"
# Copyright (C) 2013-2023 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ____________________________________________________________
from time import time


class Cache:
    """cache object
    """
    __slots__ = ('_cache',)

    def __init__(self):
        self._cache = {}

    def _get_path_index(self, option_bag):
        if option_bag is None:
            path = None
            index = None
        else:
            path = option_bag.path
            index = option_bag.index
        return path, index

    def getcache(self,
                 option_bag,
                 type_,
                 expiration=True,
                 ):
        """get the cache value fot a specified path
        """
        no_cache = False, None, False
        path, index = self._get_path_index(option_bag)
        if path not in self._cache or index not in self._cache[path]:
            return no_cache
        value, timestamp, validated = self._cache[path][index]
        if type_ == 'context_props':
            # cached value is settings properties so value is props
            props = value
            self_props = {}
        else:
            props = option_bag.config_bag.properties
            if type_ == 'self_props':
                # cached value is self_props
                self_props = value
            else:
                self_props = option_bag.properties
        if 'cache' in props or \
                'cache' in self_props:
            if expiration and timestamp and \
                    ('expire' in props or \
                     'expire' in self_props):
                ntime = int(time())
                if timestamp + option_bag.config_bag.expiration_time >= ntime:
                    return True, value, validated
            else:
                return True, value, validated
        return no_cache

    def setcache(self,
                 option_bag,
                 val,
                 type_='values',
                 validated=True,
                 ):
        """add val in cache for a specified path
        if follower, add index
        """
        if type_ == 'values':
            if 'cache' not in option_bag.config_bag.properties and \
                    'cache' not in option_bag.properties:
                return
        elif (option_bag is None or 'cache' not in option_bag.config_bag.properties) and \
                'cache' not in val:
            return
        path, index = self._get_path_index(option_bag)
        self._cache.setdefault(path, {})[index] = (val, int(time()), validated)

    def delcache(self, path):
        """reset cache a a specified path
        """
        if path in  self._cache:
            del self._cache[path]

    def get_cached(self):
        """get cache values
        """
        return self._cache

    def reset_all_cache(self):
        """reset all cache values
        """
        self._cache.clear()
