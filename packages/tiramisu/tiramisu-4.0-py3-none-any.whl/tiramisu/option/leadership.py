# -*- coding: utf-8 -*-
"Leadership support"
# Copyright (C) 2014-2023 Team tiramisu (see AUTHORS for all contributors)
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
import weakref
from typing import List, Iterator, Optional


from ..i18n import _
from ..setting import groups, undefined, OptionBag, ALLOWED_LEADER_PROPERTIES
from .optiondescription import OptionDescription
from .syndynoptiondescription import SynDynLeadership
from .baseoption import BaseOption
from .option import Option
from ..error import LeadershipError
from ..autolib import Calculation


class Leadership(OptionDescription):
    """Leadership
    """
    # pylint: disable=too-many-arguments
    __slots__ = ('leader',
                 'followers',
                 )

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 properties=None) -> None:
        super().__init__(name,
                         doc,
                         children,
                         properties=properties)
        self._group_type = groups.leadership
        followers = []
        if len(children) < 2:
            raise ValueError(_('a leader and a follower are mandatories in leadership "{}"'
                               '').format(name))
        leader = children[0]
        for idx, child in enumerate(children):
            if __debug__:
                self._check_child_is_valid(child)
            if idx != 0:
                if __debug__:
                    self._check_default_value(child)
                # remove empty property for follower
                child._properties = frozenset(child._properties - {'empty', 'unique'})
                followers.append(child)
            child._add_dependency(self)
            child._leadership = weakref.ref(self)
        if __debug__:
            for prop in leader.impl_getproperties():
                if prop not in ALLOWED_LEADER_PROPERTIES and not isinstance(prop, Calculation):
                    raise LeadershipError(_('leader cannot have "{}" property').format(prop))

    def _check_child_is_valid(self, child: BaseOption):
        if child.impl_is_symlinkoption():
            raise ValueError(_('leadership "{0}" shall not have '
                               "a symlinkoption").format(self.impl_get_display_name()))
        if not isinstance(child, Option):
            raise ValueError(_('leadership "{0}" shall not have '
                               'a subgroup').format(self.impl_get_display_name()))
        if not child.impl_is_multi():
            raise ValueError(_('only multi option allowed in leadership "{0}" but option '
                               '"{1}" is not a multi'
                               '').format(self.impl_get_display_name(),
                                          child.impl_get_display_name()))

    def _check_default_value(self, child: BaseOption):
        default = child.impl_getdefault()
        if default != []:
            if child.impl_is_submulti() and isinstance(default, (list, tuple)):
                for val in default:
                    if not isinstance(val, Calculation):
                        calculation = False
                        break
                else:
                    # empty default is valid
                    calculation = True
            else:
                calculation = isinstance(default, Calculation)
            if not calculation:
                raise ValueError(_('not allowed default value for follower option '
                                   f'"{child.impl_get_display_name()}" in leadership '
                                   f'"{self.impl_get_display_name()}"'))

    def _setsubdyn(self,
                   subdyn,
                   ) -> None:
        for chld in self._children[1]:
            chld._setsubdyn(subdyn)
        super()._setsubdyn(subdyn)

    def is_leader(self,
                  opt: Option,
                  ) -> bool:
        """the option is the leader
        """
        leader = self.get_leader()
        return opt == leader or (opt.impl_is_dynsymlinkoption() and opt.opt == leader)

    def get_leader(self) -> Option:
        """get leader
        """
        return self._children[1][0]

    def get_followers(self) -> Iterator[Option]:
        """get all followers
        """
        for follower in self._children[1][1:]:
            yield follower

    def in_same_leadership(self,
                           opt: Option,
                           ) -> bool:
        """check if followers are in same leadership
        """
        if opt.impl_is_dynsymlinkoption():
            opt = opt.opt
        return opt in self._children[1]

    def reset(self, config_bag: 'ConfigBag') -> None:
        """reset follower value
        """
        values = config_bag.context.get_values()
        config_bag = config_bag.copy()
        config_bag.remove_validation()
        for follower in self.get_followers():
            soption_bag = OptionBag(follower,
                                    None,
                                    config_bag,
                                    )
            values.reset(soption_bag)

    def follower_force_store_value(self,
                                   value,
                                   config_bag: 'ConfigBag',
                                   owner,
                                   dyn=None,
                                   ) -> None:
        """apply force_store_value to follower
        """
        if value:
            if dyn is None:
                dyn = self
            values = config_bag.context.get_values()
            for idx, follower in enumerate(dyn.get_children(config_bag)):
                if not idx:
                    # it's a master
                    apply_requires = True
                    indexes = [None]
                else:
                    apply_requires = False
                    indexes = range(len(value))
                foption_bag = OptionBag(follower,
                                        None,
                                        config_bag,
                                        apply_requires=apply_requires,
                                        )
                if 'force_store_value' not in foption_bag.properties:
                    continue
                for index in indexes:
                    foption_bag_index = OptionBag(follower,
                                                  index,
                                                  config_bag,
                                                  )
                    values.set_storage_value(foption_bag_index.path,
                                             index,
                                             values.get_value(foption_bag_index)[0],
                                             owner,
                                             )

    def pop(self,
            index: int,
            config_bag: 'ConfigBag',
            followers: Optional[List[Option]]=undefined,
            ) -> None:
        """pop leader value and follower's one
        """
        if followers is undefined:
            # followers are not undefined only in SynDynLeadership
            followers = self.get_followers()
        config_bag = config_bag.copy()
        config_bag.remove_validation()
        values = config_bag.context.get_values()
        for follower in followers:
            soption_bag = OptionBag(follower,
                                    index,
                                    config_bag,
                                    properties=set(),  # do not check force_default_on_freeze
                                                       # or force_metaconfig_on_freeze
                                    )
            values.reduce_index(soption_bag)

    def reset_cache(self,
                    path: str,
                    config_bag: 'ConfigBag',
                    resetted_opts: List[Option],
                    ) -> None:
        self._reset_cache(path,
                          self.get_leader(),
                          self.get_followers(),
                          config_bag,
                          resetted_opts,
                          )

    def _reset_cache(self,
                     path: str,
                     leader: Option,
                     followers: List[Option],
                     config_bag: 'ConfigBag',
                     resetted_opts: List[Option],
                     ) -> None:
        super().reset_cache(path,
                            config_bag,
                            resetted_opts,
                            )
        leader.reset_cache(leader.impl_getpath(),
                           config_bag,
                           None)
        for follower in followers:
            follower.reset_cache(follower.impl_getpath(),
                                 config_bag,
                                 None,
                                 )

    def impl_is_leadership(self) -> None:
        return True

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn,
                     ) -> SynDynLeadership:
        return SynDynLeadership(self,
                                rootpath,
                                suffix,
                                ori_dyn,
                                )
