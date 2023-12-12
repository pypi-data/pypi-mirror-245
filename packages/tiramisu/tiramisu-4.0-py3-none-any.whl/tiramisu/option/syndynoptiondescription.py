# -*- coding: utf-8 -*-
# Copyright (C) 2017-2023 Team tiramisu (see AUTHORS for all contributors)
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
"""SynDynOptionDescription and SynDynLeadership internal option
it's an instanciate synoptiondescription
"""
from typing import Optional, Iterator, Any, List


from ..i18n import _
from ..setting import ConfigBag, undefined
from .baseoption import BaseOption
from .syndynoption import SynDynOption


class SubDynOptionDescription:
    __slots__ = ('rootpath',
                 'opt',
                 'dyn_parent',
                 '__weakref__',
                 )

    def __init__(self,
                 opt: BaseOption,
                 rootpath: str,
                 dyn_parent,
                 ) -> None:
        self.opt = opt
        self.rootpath = rootpath
        self.dyn_parent = dyn_parent

    def impl_getpath(self) -> str:
        """get path
        """
        path = self.opt.impl_getname()
        if self.rootpath:
            path = f'{self.rootpath}.{path}'
        return path

    def get_sub_children(self,
                         option,
                         config_bag,
                         *,
                         index=None,
                         properties=undefined,
                         ):
        return self.opt.get_sub_children(option,
                                         config_bag,
                                         index=index,
                                         properties=properties,
                                         dynoption=self,
                                         )

    def getsubdyn(self):
        return self.opt.getsubdyn()

    def impl_is_optiondescription(self):
        return True

    def impl_is_dynsymlinkoption(self):
        return True

    def impl_is_sub_dyn_optiondescription(self):
        return True

    def impl_get_display_name(self) -> str:
        return self.opt.impl_get_display_name(self)

    def impl_is_dynoptiondescription(self) -> bool:
        return True

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn,
                     ):
        return self.opt.to_dynoption(rootpath, suffix, ori_dyn)


class SynDynOptionDescription:
    """SynDynOptionDescription internal option, it's an instanciate synoptiondescription
    """
    __slots__ = ('opt',
                 'rootpath',
                 '_suffix',
                 'ori_dyn')

    def __init__(self,
                 opt: BaseOption,
                 rootpath: str,
                 suffix: str,
                 ori_dyn) -> None:
        self.opt = opt
        self.rootpath = rootpath
        self._suffix = suffix
        # For a Leadership inside a DynOptionDescription
        self.ori_dyn = ori_dyn

    def __getattr__(self,
                    name: str,
                    ) -> Any:
        # if not in SynDynOptionDescription, get value in self.opt
        return getattr(self.opt,
                       name,
                       )

    def impl_getname(self) -> str:
        """get name
        """
        if self.opt.impl_is_dynoptiondescription():
            return self.opt.impl_getname(self._suffix)
        return self.opt.impl_getname()

    def impl_get_display_name(self) -> str:
        """get display name
        """
        return self.opt.impl_get_display_name(self)

    def get_children(self,
                     config_bag: ConfigBag,
                     dyn: bool=True,
                     ):
        # pylint: disable=unused-argument
        """get children
        """
        yield from self.opt.get_children(config_bag,
                                         dynoption=self,
                                         option_suffix=self._suffix,
                                         )

    def get_child(self,
                  name: str,
                  config_bag: ConfigBag,
                  subpath: str,
                  allow_dynoption: bool=False,
                  ):
        """get children
        """
        return self.opt.get_child(name,
                                  config_bag,
                                  subpath,
                                  dynoption=self,
                                  option_suffix=self._suffix,
                                  allow_dynoption=allow_dynoption,
                                  )

    def get_sub_children(self,
                         option,
                         config_bag,
                         *,
                         index=None,
                         properties=undefined,
                         ):
        return self.opt.get_sub_children(option,
                                         config_bag,
                                         index=index,
                                         properties=properties,
                                         dynoption=self,
                                         )

    def impl_is_dynsymlinkoption(self) -> bool:
        """it's a dynsymlinkoption
        """
        return True

    def get_children_recursively(self,
                                 bytype: Optional[BaseOption],
                                 byname: Optional[str],
                                 config_bag: ConfigBag,
                                 self_opt: BaseOption=None,
                                 ) -> BaseOption:
        # pylint: disable=unused-argument
        """get children recursively
        """
        for option in self.opt.get_children_recursively(bytype,
                                                        byname,
                                                        config_bag,
                                                        self,
                                                        ):
            yield option

    def impl_getpath(self) -> str:
        """get path
        """
        path = self.impl_getname()
        if self.rootpath:
            path = f'{self.rootpath}.{path}'
        return path

    def impl_getsuffix(self) -> str:
        """get suffix
        """
        return self._suffix


class SynDynLeadership(SynDynOptionDescription):
    """SynDynLeadership internal option, it's an instanciate synoptiondescription
    """
    def get_leader(self) -> SynDynOption:
        """get the leader
        """
        return self.opt.get_leader().to_dynoption(self.impl_getpath(),
                                                  self._suffix,
                                                  self.ori_dyn,
                                                  )

    def get_followers(self) -> Iterator[SynDynOption]:
        """get followers
        """
        subpath = self.impl_getpath()
        for follower in self.opt.get_followers():
            yield follower.to_dynoption(subpath,
                                        self._suffix,
                                        self.ori_dyn,
                                        )

    def reset_cache(self,
                    path: str,
                    config_bag: 'ConfigBag',
                    resetted_opts: List[str],
                    ) -> None:
        """reset cache
        """
        leader = self.get_leader()
        followers = self.get_followers()
        self._reset_cache(path,
                          leader,
                          followers,
                          config_bag,
                          resetted_opts,
                          )

    def pop(self,
            *args,
            **kwargs,
            ) -> None:
        """pop value for a follower
        """
        self.opt.pop(*args,
                     followers=self.get_followers(),
                     **kwargs,
                     )

    def follower_force_store_value(self,
                                   value,
                                   config_bag,
                                   owner,
                                   ) -> None:
        """force store value for a follower
        """
        self.opt.follower_force_store_value(value,
                                            config_bag,
                                            owner,
                                            dyn=self,
                                            )

    def impl_getsuffix(self) -> str:
        """get suffix
        """
        return self._suffix
