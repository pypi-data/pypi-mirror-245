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
"""DynOptionDescription
"""
import re
import weakref
from typing import List, Any, Optional, Tuple
from itertools import chain
from ..autolib import ParamOption


from ..i18n import _
from .optiondescription import OptionDescription
from .syndynoptiondescription import SynDynLeadership
from .baseoption import BaseOption
from ..setting import OptionBag, ConfigBag, undefined
from ..error import ConfigError
from ..autolib import Calculation


NAME_REGEXP = re.compile(r'^[a-zA-Z\d\-_]*$')


class DynOptionDescription(OptionDescription):
    """dyn option description
    """
    __slots__ = ('_suffixes',
                 '_subdyns',
                 )

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 suffixes: Calculation,
                 properties=None,
                 ) -> None:
        # pylint: disable=too-many-arguments
        super().__init__(name,
                         doc,
                         children,
                         properties,
                         )
        # check children + set relation to this dynoptiondescription
        wself = weakref.ref(self)
        for child in children:
            child._setsubdyn(wself)
        # add suffixes
        if __debug__ and not isinstance(suffixes, Calculation):
            raise ConfigError(_('suffixes in dynoptiondescription has to be a calculation'))
        for param in chain(suffixes.params.args, suffixes.params.kwargs.values()):
            if isinstance(param, ParamOption):
                param.option._add_dependency(self,
                                             is_suffix=True,
                                             )
        self._suffixes = suffixes

    def convert_suffix_to_path(self,
                               suffix: Any,
                               ) -> str:
        """convert suffix to use it to a path
        """
        if suffix is None:
            return None
        if not isinstance(suffix, str):
            suffix = str(suffix)
        if '.' in suffix:
            suffix = suffix.replace('.', '_')
        return suffix

    def get_suffixes(self,
                     config_bag: ConfigBag,
                     dynoption=None,
                     ) -> List[str]:
        """get dynamic suffixes
        """
        if dynoption:
            self_opt = dynoption
        else:
            self_opt = self
        option_bag = OptionBag(self_opt,
                               None,
                               config_bag,
                               properties=None,
                               )
        values = self._suffixes.execute(option_bag)
        if values is None:
            values = []
        values_ = []
        if __debug__:
            if not isinstance(values, list):
                raise ValueError(_('DynOptionDescription suffixes for '
                                   f'option "{self.impl_get_display_name()}", is not '
                                   f'a list ({values})'))
        for val in values:
            cval = self.convert_suffix_to_path(val)
            if not isinstance(cval, str) or re.match(NAME_REGEXP, cval) is None:
                if __debug__ and cval is not None:
                    raise ValueError(_('invalid suffix "{}" for option "{}"'
                                       '').format(cval,
                                                  self.impl_get_display_name()))
            else:
                values_.append(val)
        if __debug__ and len(values_) > len(set(values_)):
            raise ValueError(_(f'DynOptionDescription "{self._name}" suffixes return a list with '
                               f'same values "{values_}"'''))
        return values_

    def impl_is_dynoptiondescription(self) -> bool:
        return True

    def option_is_self(self,
                       option,
                       ) -> bool:
        return option == self or \
                (option.impl_is_sub_dyn_optiondescription() and option.opt == self)

    def split_path(self,
                   dynoption,
                   option,
                   ) -> Tuple[str, str]:
        """self.impl_getpath() is something like root.xxx.dynoption_path
        option.impl_getpath() is something like root.xxx.dynoption_path.sub.path
        must return ('root.xxx.', '.sub')
        """
        if dynoption is None:
            self_path = self.impl_getpath()
        else:
            self_path = dynoption.impl_getpath()
        root_path = self_path.rsplit('.', 1)[0] if '.' in self_path else None
        #
        if self.option_is_self(option):
            sub_path = ''
        else:
            option_path = option.impl_getpath()
            if root_path:
                if isinstance(option, SynDynLeadership):
                    count_root_path = option_path.count('.') - root_path.count('.')
                    root_path = option_path.rsplit('.', count_root_path)[0]
                root_path += '.'
            self_number_child = self_path.count('.') + 1
            option_sub_path = option_path.split('.', self_number_child)[-1]
            sub_path = '.' + option_sub_path.rsplit('.', 1)[0] if '.' in option_sub_path else ''
        return root_path, sub_path

    def get_sub_children(self,
                         option,
                         config_bag,
                         *,
                         index=None,
                         properties=undefined,
                         dynoption=None,
                         ):
        root_path, sub_path = self.split_path(dynoption,
                                              option,
                                              )
        for suffix in self.get_suffixes(config_bag,
                                        dynoption=dynoption,
                                        ):
            if self.option_is_self(option):
                parent_path = root_path
            elif root_path:
                parent_path = root_path + self.impl_getname(suffix) + sub_path
            else:
                parent_path = self.impl_getname(suffix) + sub_path
            yield OptionBag(option.to_dynoption(parent_path,
                                                suffix,
                                                self,
                                                ),
                            index,
                            config_bag,
                            properties=properties,
                            ori_option=option
                            )

    def impl_getname(self, suffix=None) -> str:
        """get name
        """
        name = super().impl_getname()
        if suffix is None:
            return name
        path_suffix = self.convert_suffix_to_path(suffix)
        return name + path_suffix
