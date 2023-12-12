# -*- coding: utf-8 -*-
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
"""OptionDescription
"""
import weakref
from typing import Optional, Iterator, Union, List


from ..i18n import _
from ..setting import ConfigBag, OptionBag, groups, undefined, owners, Undefined
from .baseoption import BaseOption
from .syndynoptiondescription import SubDynOptionDescription, SynDynOptionDescription
from ..error import ConfigError, ConflictError


class CacheOptionDescription(BaseOption):
    """manage cache for option description
    """
    __slots__ = ('_cache_force_store_values',
                 '_cache_dependencies_information',
                 )

    def impl_already_build_caches(self) -> bool:
        """is a readonly option?
        """
        return self.impl_is_readonly()

    def _build_cache(self,
                     _consistencies=None,
                     _consistencies_id=0,
                     currpath: List[str]=None,
                     cache_option=None,
                     force_store_values=None,
                     dependencies_information=None,
                     display_name=None,
                     ) -> None:
        """validate options and set option has readonly option
        """
        # pylint: disable=too-many-branches,too-many-arguments
        # _consistencies is None only when we start to build cache
        if _consistencies is None:
            init = True
            _consistencies = {}
            if __debug__:
                cache_option = []
            force_store_values = []
            dependencies_information = {}
            currpath = []
        else:
            init = False

        if self.impl_is_readonly():
            # cache already set
            raise ConfigError(_('option description seems to be part of an other '
                                'config'))
        for option in self.get_children(config_bag=undefined,  # pylint: disable=no-member
                                        dyn=False,
                                        ):
            if __debug__:
                cache_option.append(option)
            sub_currpath = currpath + [option.impl_getname()]
            subpath = '.'.join(sub_currpath)
            if isinstance(option, OptionDescription):
                # pylint: disable=protected-access
                option._build_cache(_consistencies,
                                    _consistencies_id,
                                    sub_currpath,
                                    cache_option,
                                    force_store_values,
                                    dependencies_information,
                                    display_name,
                                    )
            else:
                for information, options in option.get_dependencies_information().items():
                    if None in options:
                        dependencies_information.setdefault(information, []).append(option)
                if not option.impl_is_symlinkoption():
                    properties = option.impl_getproperties()
                    if 'force_store_value' in properties:
                        force_store_values.append(option)
#                    if __debug__ and ('force_default_on_freeze' in properties or \
#                            'force_metaconfig_on_freeze' in properties) and \
#                            'frozen' not in properties and \
#                            option.impl_is_leader():
#                        raise ConfigError(_('a leader ({0}) cannot have '
#                                            '"force_default_on_freeze" or '
#                                            '"force_metaconfig_on_freeze" '
#                                            'property without "frozen"'
#                                            '').format(option.impl_get_display_name()))
            if option.impl_is_readonly():
                raise ConflictError(_('duplicate option: {0}').format(option))
            if not self.impl_is_readonly() and display_name:
                option._display_name_function = display_name  # pylint: disable=protected-access
            option._path = subpath  # pylint: disable=protected-access
            option._set_readonly()  # pylint: disable=protected-access
        if init:
            self._cache_force_store_values = force_store_values  # pylint: disable=attribute-defined-outside-init
            self._cache_dependencies_information = dependencies_information  # pylint: disable=attribute-defined-outside-init
            self._path = self._name  # pylint: disable=attribute-defined-outside-init,no-member
            self._set_readonly()

    def impl_build_force_store_values(self,
                                      config_bag: ConfigBag,
                                      ) -> None:
        """set value to force_store_values option
        """
        # pylint: disable=too-many-branches
        def do_option_bags(option):
            if option.issubdyn():
                dynopt = option.getsubdyn()
                yield from dynopt.get_sub_children(option,
                                                   config_bag,
                                                   index=None,
                                                   )
            else:
                yield OptionBag(option,
                                None,
                                config_bag,
                                properties=None,
                                )
        if 'force_store_value' not in config_bag.properties:
            return
        values = config_bag.context.get_values()
        for option in self._cache_force_store_values:
            if option.impl_is_follower():
                leader = option.impl_get_leadership().get_leader()
                for leader_option_bag in do_option_bags(leader):
                    leader_option_bag.properties = frozenset()
                    follower_len = len(values.get_value(leader_option_bag)[0])
                    if option.issubdyn():
                        subpath = leader_option_bag.option.rootpath
                        doption = option.to_dynoption(subpath,
                                                      leader_option_bag.option.impl_getsuffix(),
                                                      leader_option_bag.option.dyn_parent,
                                                      )
                    else:
                        doption = option
                    subpath = doption.impl_getpath()
                    for index in range(follower_len):
                        option_bag = OptionBag(doption,
                                               index,
                                               config_bag,
                                               properties=frozenset(),
                                               )
                        if values.hasvalue(subpath, index=index):
                            continue
                        value = values.get_value(option_bag)[0]
                        if value is None:
                            continue
                        values.set_storage_value(subpath,
                                                 index,
                                                 value,
                                                 owners.forced,
                                                 )
            else:
                for option_bag in do_option_bags(option):
                    option_bag.properties = frozenset()
                    value = values.get_value(option_bag)[0]
                    if value is None:
                        continue
                    if values.hasvalue(option_bag.path):
                        continue
                    values.set_storage_value(option_bag.path,
                                             None,
                                             value,
                                             owners.forced,
                                             )


class OptionDescriptionWalk(CacheOptionDescription):
    """get child of option description
    """
    __slots__ = ('_children',)

    def get_child(self,
                  name: str,
                  config_bag: ConfigBag,
                  subpath: str,
                  *,
                  dynoption=None,
                  option_suffix: Optional[str]=None,
                  allow_dynoption: bool=False,
                  ) -> Union[BaseOption, SynDynOptionDescription]:
        """get a child
        """
        # if not dyn
        if name in self._children[0]:  # pylint: disable=no-member
            option = self._children[1][self._children[0].index(name)]  # pylint: disable=no-member
            if option.impl_is_dynoptiondescription():
                if allow_dynoption:
                    option_suffix = None
                else:
                    raise AttributeError(_(f'unknown option "{name}" '
                                           "in root optiondescription (it's a dynamic option)"
                                           ))
            if option.issubdyn():
                return option.to_dynoption(subpath,
                                           option_suffix,
                                           option,
                                           )
            return option
        # if dyn
        if dynoption:
            self_opt = dynoption
        else:
            self_opt = self
        for child in self._children[1]:  # pylint: disable=no-member
            if not child.impl_is_dynoptiondescription():
                continue
            for suffix in child.get_suffixes(config_bag,
                                             dynoption,
                                             ):
                if name != child.impl_getname(suffix):
                    continue
                return child.to_dynoption(subpath,
                                          suffix,
                                          child,
                                          )
        if self.impl_get_group_type() == groups.root:  # pylint: disable=no-member
            raise AttributeError(_(f'unknown option "{name}" '
                                   'in root optiondescription'
                                   ))
        raise AttributeError(_(f'unknown option "{name}" '
                               f'in optiondescription "{self_opt.impl_get_display_name()}"'
                               ))

    def get_children(self,
                     config_bag: Union[ConfigBag, Undefined],
                     *,
                     dyn: bool=True,
                     #path: Optional[str]=None,
                     dynoption=None,
                     option_suffix: Optional[str]=None,
                     ) -> Union[BaseOption, SynDynOptionDescription]:
        """get children
        """
#        if path:
#            subpath = path
        if dynoption:
            self_opt = dynoption
        else:
            self_opt = self
        if not dyn or config_bag is undefined or \
                config_bag.context.get_description() == self:
            subpath = ''
        else:
            subpath = self_opt.impl_getpath()
        for child in self._children[1]:  # pylint: disable=no-member
            if dyn and child.impl_is_dynoptiondescription():
                for suffix in child.get_suffixes(config_bag,
                                                 dynoption,
                                                 ):
                    yield child.to_dynoption(subpath,
                                             suffix,
                                             child,
                                             )
            elif dyn and child.issubdyn() or child.impl_is_dynsymlinkoption():
                yield child.to_dynoption(subpath,
                                         option_suffix,
                                         child,
                                         )
            else:
                yield child

    def get_children_recursively(self,
                                 bytype: Optional[BaseOption],
                                 byname: Optional[str],
                                 config_bag: ConfigBag,
                                 self_opt: BaseOption=None,
                                 ) -> Iterator[Union[BaseOption, SynDynOptionDescription]]:
        """get children recursively
        """
        if self_opt is None:
            self_opt = self
        for option in self_opt.get_children(config_bag):
            if option.impl_is_optiondescription():
                for subopt in option.get_children_recursively(bytype,
                                                              byname,
                                                              config_bag,
                                                              ):
                    yield subopt
            elif (byname is None or option.impl_getname() == byname) and \
                    (bytype is None or isinstance(option, bytype)):
                yield option


class OptionDescription(OptionDescriptionWalk):
    """Config's schema (organisation, group) and container of Options
    The `OptionsDescription` objects lives in the `tiramisu.config.Config`.
    """
    __slots__ = ('_group_type',)

    def __init__(self,
                 name: str,
                 doc: str,
                 children: List[BaseOption],
                 properties=None) -> None:
        """
        :param children: a list of options (including optiondescriptions)

        """
        assert isinstance(children, list), _('children in optiondescription "{}" '
                                             'must be a list').format(name)
        super().__init__(name,
                         doc=doc,
                         properties=properties)
        child_names = []
        if __debug__:
            dynopt_names = []
        for child in children:
            name = child.impl_getname()
            child_names.append(name)
            if __debug__ and child.impl_is_dynoptiondescription():
                dynopt_names.append(name)

        # before sorting
        children_ = (tuple(child_names), tuple(children))

        if __debug__:
            # better performance like this
            child_names.sort()
            old = None
            for child in child_names:
                if child == old:
                    raise ConflictError(_('duplicate option name: '
                                          '"{0}"').format(child))
                if dynopt_names:
                    for dynopt in dynopt_names:
                        if child != dynopt and child.startswith(dynopt):
                            raise ConflictError(_(f'the option\'s name "{child}" start as '
                                                  f'the dynoptiondescription\'s name "{dynopt}"'))
                old = child
        self._children = children_
        # the group_type is useful for filtering OptionDescriptions in a config
        self._group_type = groups.default

    def _setsubdyn(self,
                   subdyn,
                   ) -> None:
        for child in self._children[1]:
            child._setsubdyn(subdyn)
        super()._setsubdyn(subdyn)

    def impl_is_optiondescription(self) -> bool:
        """the option is an option description
        """
        return True

    def impl_is_dynoptiondescription(self) -> bool:
        """the option is not dynamic
        """
        return False

    def impl_is_leadership(self) -> bool:
        """the option is not a leadership
        """
        return False

    # ____________________________________________________________
    def impl_set_group_type(self,
                            group_type: groups.GroupType,
                            ) -> None:
        """sets a given group object to an OptionDescription

        :param group_type: an instance of `GroupType` or `LeadershipGroupType`
                              that lives in `setting.groups`
        """
        if __debug__:
            if self._group_type != groups.default:
                raise ValueError(_('cannot change group_type if already set '
                                   '(old {0}, new {1})').format(self._group_type,
                                                                group_type))
            if not isinstance(group_type, groups.GroupType):
                raise ValueError(_('group_type: {0}'
                                   ' not allowed').format(group_type))
            if isinstance(group_type, groups.LeadershipGroupType):
                raise ConfigError('please use Leadership object instead of OptionDescription')
        self._group_type = group_type

    def impl_get_group_type(self) -> groups.GroupType:
        """get the group type of option description
        """
        return self._group_type

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn) -> SynDynOptionDescription:
        """get syn dyn option description
        """
        if suffix is None:
            return SubDynOptionDescription(self,
                                           rootpath,
                                           ori_dyn,
                                           )
        return SynDynOptionDescription(self,
                                       rootpath,
                                       suffix,
                                       ori_dyn)

    def impl_is_dynsymlinkoption(self) -> bool:
        """option is not a dyn symlink option
        """
        return False
