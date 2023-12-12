# -*- coding: utf-8 -*-
# Copyright (C) 2018-2023 Team tiramisu (see AUTHORS for all contributors)
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
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"""SynDynOption internal option, it's an instanciate synoption
"""
from typing import Any
from .baseoption import BaseOption


class SynDynOption:
    """SynDynOption is an Option include un DynOptionDescription with specified prefix
    """
    __slots__ = ('rootpath',
                 'opt',
                 'suffix',
                 'dyn_parent',
                 '__weakref__')

    def __init__(self,
                 opt: BaseOption,
                 rootpath: str,
                 suffix: str,
                 dyn_parent,
                 ) -> None:
        self.opt = opt
        self.rootpath = rootpath
        self.suffix = suffix
        self.dyn_parent = dyn_parent

    def __getattr__(self,
                    name: str) -> Any:
        return getattr(self.opt,
                       name,
                       )

    def impl_getname(self) -> str:
        """get option name
        """
        return self.opt.impl_getname()

    def impl_get_display_name(self) -> str:
        """get option display name
        """
        return self.opt.impl_get_display_name(self)

    def impl_getsuffix(self) -> str:
        """get suffix
        """
        return self.suffix

    def impl_getpath(self) -> str:
        """get path
        """
        path = self.impl_getname()
        if self.rootpath:
            path = f'{self.rootpath}.{path}'
        return path

    def impl_is_dynsymlinkoption(self) -> bool:
        """it's a dynsymlinkoption
        """
        return True

    def impl_get_leadership(self):  # pylint: disable=inconsistent-return-statements
        """is it a leadership?
        """
        leadership = self.opt.impl_get_leadership()
        if leadership:
            rootpath = self.rootpath.rsplit('.', 1)[0]
            return leadership.to_dynoption(rootpath,
                                           self.suffix,
                                           self.dyn_parent,
                                           )
