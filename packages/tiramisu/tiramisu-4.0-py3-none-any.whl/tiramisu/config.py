# -*- coding: utf-8 -*-
# Copyright (C) 2012-2023 Team tiramisu (see AUTHORS for all contributors)
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
"""options handler global entry point
"""
import weakref
from copy import copy, deepcopy
from typing import Optional, List, Any, Union

from .error import PropertiesOptionError, ConfigError, ConflictError, \
                   LeadershipError
from .option import DynOptionDescription, Leadership, Option
from .option.syndynoptiondescription import SubDynOptionDescription
from .setting import OptionBag, ConfigBag, Settings, undefined, groups
from .value import Values, owners
from .i18n import _
from .cacheobj import Cache
from .autolib import Calculation


class _SubConfig:
    """Sub configuration management entry.
    Tree if OptionDescription's responsability. SubConfig are generated
    on-demand. A Config is also a SubConfig.
    Root Config is call context below
    """
    __slots__ = ('_impl_context',
                 '_impl_descr',
                 '_impl_path',
                 )

    def __init__(self,
                 descr,
                 context,
                 subpath=None,
                 ):
        """ Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        :type subpath: `str` with the path name
        """
        # main option description
        self._impl_descr = descr
        self._impl_context = context
        self._impl_path = subpath

    def get_length_leadership(self,
                              option_bag,
                              ):
        """Get the length of leader option (useful to know follower's length)
        """
        cconfig_bag = option_bag.config_bag.copy()
        cconfig_bag.remove_validation()
        option_bag = OptionBag(option_bag.option.get_leader(),
                               None,
                               cconfig_bag,
                               )
        return len(self.get_value(option_bag))

    def get_description(self):
        """get root description
        """
        assert self._impl_descr is not None, _('there is no option description for this config'
                                               ' (may be GroupConfig)')
        return self._impl_descr

    def get_settings(self):
        """get settings object
        """
        return self._impl_settings  # pylint: disable=no-member

    def get_values(self):
        """get values object
        """
        return self._impl_values  # pylint: disable=no-member

    # =============================================================================
    # CACHE
    def reset_cache(self,
                    option_bag,
                    resetted_opts=None,
                    ):
        """reset all settings in cache
        """
        if resetted_opts is None:
            resetted_opts = []

        if option_bag is not None:
            if 'cache' not in option_bag.config_bag.properties:
                return
            option_bag.config_bag.properties = option_bag.config_bag.properties - {'cache'}
            self.reset_one_option_cache(resetted_opts,
                                        option_bag,
                                        )
            option_bag.config_bag.properties = option_bag.config_bag.properties | {'cache'}
        else:
            self._impl_values_cache.reset_all_cache()  # pylint: disable=no-member
            self.properties_cache.reset_all_cache()  # pylint: disable=no-member

    def get_values_cache(self):
        """get cache for values
        """
        return self._impl_values_cache  # pylint: disable=no-member

    def reset_one_option_cache(self,
                               resetted_opts,
                               option_bag,
                               ):
        """reset cache for one option
        """
        if option_bag.path in resetted_opts:
            return
        resetted_opts.append(option_bag.path)
        for woption in option_bag.option.get_dependencies(option_bag.option):
            option = woption()
            if woption in option_bag.option._get_suffixes_dependencies() and \
                    option_bag.option.issubdyn() and \
                    option.impl_is_dynoptiondescription():
                paths = [subdyn().impl_getpath() for subdyn in option.get_sub_dyns()]
                for weak_subdyn in option_bag.option.get_sub_dyns():
                    subdyn = weak_subdyn()
                    if subdyn.impl_getpath() in paths:
                        root_path = option_bag.option.impl_getpath()
                        if '.' in root_path:
                            root_path = root_path.rsplit('.', 1)[0]
                            nb_elt = root_path.count('.') + 1
                        else:
                            root_path = ''
                            nb_elt = 1
                        config_bag = option_bag.config_bag
                        root_option_bag = OptionBag(config_bag.context.get_description(),
                                                    None,
                                                    config_bag,
                                                    )
                        full_path = root_path + '.' + option.impl_getpath().split('.', nb_elt)[-1]
                        try:
                            options_bag = config_bag.context.get_sub_option_bag(root_option_bag,
                                                                                full_path,
                                                                                #FIXME index?
                                                                                None,
                                                                                validate_properties=False,
                                                                                properties=None,
                                                                                allow_dynoption=True,
                                                                                )
                        except AttributeError as err:
                            raise ConfigError(_(f'option "{option.impl_get_display_name()}" is not in a dynoptiondescription: {err}'))
                        self._reset_cache_dyn_optiondescription(options_bag[-1],
                                                                resetted_opts,
                                                                )
                        break
            else:
                soption_bag = OptionBag(option,
                                        option_bag.index,
                                        option_bag.config_bag,
                                        properties=None,
                                        )
                if option.impl_is_dynoptiondescription():
                    self._reset_cache_dyn_optiondescription(soption_bag,
                                                            resetted_opts,
                                                            )
                elif option.issubdyn():
                    # it's an option in dynoptiondescription, remove cache for all generated option
                    config_bag = option_bag.config_bag
                    options = [soption_bag]
                    for wdynopt in reversed(option.get_sub_dyns()):
                        dynopt = wdynopt()
                        sub_options = []
                        for sub_option in options:
                            sub_options.extend(dynopt.get_sub_children(sub_option.option,
                                                                       config_bag,
                                                                       properties=None,
                                                                       ))
                        options = sub_options
                    for doption_bag in options:
                        self.reset_one_option_cache(resetted_opts,
                                                    doption_bag,
                                                    )
                else:
                    self.reset_one_option_cache(resetted_opts,
                                                soption_bag,
                                                )
            del option
        option_bag.option.reset_cache(option_bag.path,
                                      option_bag.config_bag,
                                      resetted_opts,
                                      )

    def _reset_cache_dyn_optiondescription(self,
                                           option_bag,
                                           resetted_opts,
                                           ):
        # reset cache for all chidren
        for doption_bag in option_bag.option.get_sub_children(option_bag.option,
                                                              option_bag.config_bag,
                                                              index=option_bag.index,
                                                              properties=None,
                                                              ):
            for coption in doption_bag.option.get_children_recursively(None,
                                                                       None,
                                                                       option_bag.config_bag,
                                                                       ):
                coption_bag = self.get_sub_option_bag(doption_bag,  # pylint: disable=no-member
                                                      coption.impl_getpath(),
                                                      None,
                                                      False,
                                                      )[-1]
                self.reset_one_option_cache(resetted_opts,
                                            coption_bag,
                                            )
        self._reset_cache_dyn_option(option_bag,
                                     resetted_opts,
                                     )

    def _reset_cache_dyn_option(self,
                                option_bag,
                                resetted_opts,
                                ):
        option = option_bag.option
        if isinstance(option, (DynOptionDescription, SubDynOptionDescription)):
            dynoption = option
        else:
            dynoption = option.getsubdyn()
        for doption_bag in dynoption.get_sub_children(option,
                                                      option_bag.config_bag,
                                                      index=option_bag.index,
                                                      properties=None
                                                      ):
            self.reset_one_option_cache(resetted_opts,
                                        doption_bag,
                                        )

    # =============================================================================
    # WALK
    def find(self,
             option_bag,
             bytype,
             byname,
             byvalue,
             raise_if_not_found=True,
             only_path=undefined,
             only_option=undefined,
             with_option=False,
             ):
        """
        convenience method for finding an option that lives only in the subtree

        :param first: return only one option if True, a list otherwise
        :return: find list or an exception if nothing has been found
        """
        # pylint: disable=too-many-arguments,too-many-locals
        def _filter_by_value(soption_bag):
            value = self.get_value(soption_bag)
            if isinstance(value, list):
                return byvalue in value
            return value == byvalue

        found = False
        if only_path is not undefined:
            def _fake_iter():
                yield only_option
            options = _fake_iter()
        else:
            options = option_bag.option.get_children_recursively(bytype,
                                                                 byname,
                                                                 option_bag.config_bag,
                                                                 )
        for option in options:
            path = option.impl_getpath()
            soption_bag = OptionBag(option,
                                    None,
                                    option_bag.config_bag,
                                    )
            if byvalue is not undefined and not _filter_by_value(soption_bag):
                continue
            if option_bag.config_bag.properties:
                #remove option with propertyerror, ...
                try:
                    self.get_sub_option_bag(option_bag,  # pylint: disable=no-member
                                            path,
                                            None,
                                            True,
                                            )[-1]
                except PropertiesOptionError:
                    continue
            found = True
            if not with_option:
                yield path
            else:
                yield path, option
        self._find_return_results(found,
                                  raise_if_not_found,
                                  )

    def _find_return_results(self,
                             found,
                             raise_if_not_found):
        if not found and raise_if_not_found:
            raise AttributeError(_("no option found in config"
                                   " with these criteria"))

    def _walk_valid_value(self,
                          option_bag,
                          types,
                          value=undefined,
                          ):
        if value is undefined:
            value = self.get_value(option_bag,
                                   need_help=False,
                                   )
        l_option_bag = option_bag.copy()
        l_option_bag.config_bag = option_bag.config_bag.copy()
        if 'mandatory' in types:
            l_option_bag.config_bag.properties |= {'mandatory', 'empty'}
        self.get_settings().validate_mandatory(value,
                                               l_option_bag,
                                               )
        return value

    def walk(self,
             option_bag: OptionBag,
             types: List[str]=('option',),
             group_type=None,
             recursive: bool=True,
             walked: bool=False,
             flatten_leadership: bool=False,
             ):
        """walk to tree
        """
        # pylint: disable=too-many-branches,too-many-locals,too-many-arguments,
        if option_bag.option.impl_is_optiondescription():
            # do not return root option
            if walked:
                if 'optiondescription' in types and (group_type is None or
                        option_bag.option.impl_get_group_type() == group_type):
                    yield option_bag
                if not recursive:
                    # it's not recursive, so stop to walk
                    return
            if not option_bag.option.impl_is_leadership() or flatten_leadership:
                for opt in option_bag.option.get_children(option_bag.config_bag):
                    try:
                        yield from self.walk(self.get_sub_option_bag(option_bag,  # pylint: disable=no-member
                                                                     opt.impl_getpath(),
                                                                     None,
                                                                     True,
                                                                     follower_not_apply_requires=flatten_leadership,
                                                                     )[-1],
                                             types=types,
                                             recursive=recursive,
                                             group_type=group_type,
                                             walked=True,
                                             )
                    except PropertiesOptionError as err:
                        if err.proptype in (['mandatory'], ['empty']):
                            raise err
            elif 'option' in types or 'mandatory' in types:
                # it's a leadership so walk to leader and followers
                # followers has specific length
                leader, *followers = option_bag.option.get_children(option_bag.config_bag)
                leader_option_bag = self.get_sub_option_bag(option_bag,  # pylint: disable=no-member
                                                            leader.impl_getpath(),
                                                            None,
                                                            True,
                                                            )[-1]
                followers_dict = {'leader': leader_option_bag}
                values = self.get_value(leader_option_bag,
                                        need_help=False,
                                        )
                ls_length = len(values)
                try:
                    self._walk_valid_value(leader_option_bag,
                                           types,
                                           value=values,
                                           )
                except PropertiesOptionError as err:
                    if err.proptype in (['mandatory'], ['empty']):
                        yield leader_option_bag
                for idx in range(ls_length):
                    followers_dict[idx] = []
                    for follower in followers:
                        follower_path = follower.impl_getpath()
                        try:
                            options_bag = self.get_sub_option_bag(option_bag,  # pylint: disable=no-member
                                                                  follower_path,
                                                                  idx,
                                                                  True,
                                                                  leadership_length=ls_length,
                                                                  )
                            for f_follower_bag in self.walk(options_bag[-1],
                                                            types=types,
                                                            recursive=recursive,
                                                            group_type=group_type,
                                                            walked=True,
                                                            ):
                                if 'mandatory' in types:
                                    yield f_follower_bag
                                followers_dict[idx].append(f_follower_bag)
                        except PropertiesOptionError as err:
                            continue
                if 'option' in types:
                    yield followers_dict
        else:
            if 'mandatory' in types and not option_bag.option.impl_is_symlinkoption():
                try:
                    self._walk_valid_value(option_bag,
                                           types,
                                           )
                except PropertiesOptionError as err:
                    if err.proptype in (['mandatory'], ['empty']):
                        yield option_bag
            if 'option' in types:
                yield option_bag

    def make_dict(self, option_bag):
        """exports the whole config into a `dict`
        :returns: dict of Option's name (or path) and values
        """
        ret = {}
        for data in self.walk(option_bag):
            if isinstance(data, OptionBag):
                option_bag = data
                ret[option_bag.path] = self.get_value(option_bag,
                                                      need_help=False,
                                                      )
            else:
                leader_ret = []
                leader_path = data['leader'].path
                for idx, value in enumerate(self.get_value(data['leader'],
                                                           need_help=False,
                                                           )):
                    leader_dict = {leader_path: value}
                    for follower in data.get(idx, []):
                        leader_dict[follower.path] = self.get_value(follower,
                                                                    need_help=False,
                                                                    )
                    leader_ret.append(leader_dict)
                ret[leader_path] = leader_ret

        return ret

    # =============================================================================
    # Manage value
    def set_value(self,
                  option_bag: OptionBag,
                  value: Any,
                  ) -> Any:
        """set value
        """
        self.get_settings().validate_properties(option_bag)
        return self.get_values().set_value(option_bag,
                                           value
                                           )

    def get_value(self,
                  option_bag,
                  parent_option_bag=None,
                  need_help=True,
                  ):
        """
        :return: option's value if name is an option name, OptionDescription
                 otherwise
        """
        option_bag = self._get(option_bag,
                               need_help,
                               )
        if isinstance(option_bag, list):
            value = []
            for opt_bag in option_bag:
                value.append(self.get_value(opt_bag,
                                            need_help=need_help,
                                            ))
        else:
            value = self.get_values().get_cached_value(option_bag)
            if parent_option_bag and option_bag.option.impl_is_follower() :
                length = self.get_length_leadership(parent_option_bag)
                follower_len = self.get_values().get_max_length(option_bag.path)
                if follower_len > length:
                    option_name = option_bag.option.impl_get_display_name()
                    raise LeadershipError(_(f'the follower option "{option_name}" '
                                            f'has greater length ({follower_len}) than the leader '
                                            f'length ({length})'))
            self.get_settings().validate_mandatory(value,
                                                   option_bag,
                                                   )
        return value

    def _get(self,
             option_bag: OptionBag,
             need_help: bool,
             ) -> OptionBag:
        # pylint: disable=too-many-locals
        option = option_bag.option
        if option.impl_is_symlinkoption():
            suboption = option.impl_getopt()
            if suboption.issubdyn():
                dynopt = suboption.getsubdyn()
                return list(dynopt.get_sub_children(suboption,
                                                    option_bag.config_bag,
                                                    index=option_bag.index,
                                                    ))
            if suboption.impl_is_follower():
                options_bag = self.get_sub_option_bag(option_bag.config_bag,  # pylint: disable=no-member
                                                      suboption.impl_getpath(),
                                                      None,
                                                      True,
                                                      )
                leadership_length = self.get_length_leadership(options_bag[-2])
                ret = []
                for idx in range(leadership_length):
                    f_option_bag = OptionBag(suboption,
                                             idx,
                                             option_bag.config_bag,
                                             )
                    ret.append(f_option_bag)
                return ret

            soption_bag = OptionBag(suboption,
                                    option_bag.index,
                                    option_bag.config_bag,
                                    ori_option=option,
                                    )
            return self._get(soption_bag,
                             need_help,
                             )
        return option_bag

    def get_owner(self, option_bag: OptionBag):
        """get owner
        """
        options_bag = self._get(option_bag,
                                need_help=True,
                                )
        if isinstance(options_bag, list):
            for opt_bag in options_bag:
                owner = self.get_owner(opt_bag)
                if owner != owners.default:
                    break
            else:
                owner = owners.default
        else:
            owner = self.get_values().getowner(options_bag)
        return owner


class _CommonConfig(_SubConfig):
    "abstract base class for the Config, KernelGroupConfig and the KernelMetaConfig"
    __slots__ = ('_impl_values',
                 '_impl_values_cache',
                 '_impl_settings',
                 'properties_cache',
                 '_impl_permissives_cache',
                 'parents',
                 'impl_type',
                 )

    def _impl_build_all_caches(self, descr):
        if not descr.impl_already_build_caches():
            descr._group_type = groups.root  # pylint: disable=protected-access
            descr._build_cache(display_name=self._display_name)  # pylint: disable=no-member,protected-access
        if not hasattr(descr, '_cache_force_store_values'):
            raise ConfigError(_('option description seems to be part of an other '
                                'config'))

    def get_parents(self):
        """get parents
        """
        for parent in self.parents:  # pylint: disable=no-member
            yield parent()

    # information
    def impl_set_information(self,
                             config_bag,
                             key,
                             value,
                             ):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        self._impl_values.set_information(None,  # pylint: disable=no-member
                                          key,
                                          value,
                                          )
        for option in self.get_description()._cache_dependencies_information.get(key, []):  # pylint: disable=protected-access
            option_bag = OptionBag(option,
                                   None,
                                   config_bag,
                                   properties=None,
                                   )
            self.reset_cache(option_bag)

    def impl_get_information(self,
                             key,
                             default,
                             ):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        return self._impl_values.get_information(None,  # pylint: disable=no-member
                                                 key,
                                                 default,
                                                 )

    def impl_del_information(self,
                             key,
                             raises=True,
                             ):
        """delete an information
        """
        self._impl_values.del_information(key,  # pylint: disable=no-member
                                          raises,
                                          )

    def impl_list_information(self):
        """list information keys for context
        """
        return self._impl_values.list_information()  # pylint: disable=no-member

    def gen_fake_values(self) -> 'KernelConfig':
        """generate a fake values to improve validation when assign a new value
        """
        export = deepcopy(self.get_values()._values)  # pylint: disable=protected-access
        fake_config = KernelConfig(self._impl_descr,
                                   force_values=export,
                                   force_settings=self.get_settings(),
                                   name=self._impl_name,  # pylint: disable=no-member
                                   )
        fake_config.parents = self.parents  # pylint: disable=no-member
        return fake_config

    def duplicate(self,
                  force_values=None,
                  force_settings=None,
                  metaconfig_prefix=None,
                  child=None,
                  deep=None,
                  name=None,
                  ):
        """duplication config
        """
        # pylint: disable=too-many-arguments
        if name is None:
            name = self._impl_name  # pylint: disable=no-member
        if isinstance(self, KernelConfig):
            duplicated_config = KernelConfig(self._impl_descr,
                                             _duplicate=True,
                                             force_values=force_values,
                                             force_settings=force_settings,
                                             name=name,
                                             )
        else:
            duplicated_config = KernelMetaConfig([],
                                                 _duplicate=True,
                                                 optiondescription=self._impl_descr,
                                                 name=name,
                                                 )
        duplicated_values = duplicated_config.get_values()
        duplicated_settings = duplicated_config.get_settings()
        duplicated_values._values = deepcopy(self.get_values()._values)  # pylint: disable=protected-access
        duplicated_values._informations = deepcopy(self.get_values()._informations)  # pylint: disable=protected-access
        duplicated_settings._properties = deepcopy(self.get_settings()._properties)  # pylint: disable=protected-access
        duplicated_settings._permissives = deepcopy(self.get_settings()._permissives)  # pylint: disable=protected-access
        duplicated_settings.ro_append = self.get_settings().ro_append
        duplicated_settings.rw_append = self.get_settings().rw_append
        duplicated_settings.ro_remove = self.get_settings().ro_remove
        duplicated_settings.rw_remove = self.get_settings().rw_remove
        duplicated_settings.default_properties = self.get_settings().default_properties
        duplicated_config.reset_cache(None, None)
        if child is not None:
            duplicated_config._impl_children.append(child)  # pylint: disable=protected-access
            child.parents.append(weakref.ref(duplicated_config))
        if self.parents:  # pylint: disable=no-member
            if deep is not None:
                for parent in self.parents:  # pylint: disable=no-member
                    wparent = parent()
                    if wparent not in deep:
                        deep.append(wparent)
                        subname = wparent.impl_getname()
                        if metaconfig_prefix:
                            subname = metaconfig_prefix + subname
                        duplicated_config = wparent.duplicate(deep=deep,
                                                              metaconfig_prefix=metaconfig_prefix,
                                                              child=duplicated_config,
                                                              name=subname,
                                                              )
            else:
                duplicated_config.parents = self.parents  # pylint: disable=no-member
                for parent in self.parents:  # pylint: disable=no-member
                    parent()._impl_children.append(duplicated_config)  # pylint: disable=protected-access
        return duplicated_config

    def get_config_path(self):
        """get config path
        """
        path = self.impl_getname()
        for parent in self.parents:  # pylint: disable=no-member
            wparent = parent()
            if wparent is None:  # pragma: no cover
                raise ConfigError(_(f'parent of {self._impl_name} not already exists'))  # pylint: disable=no-member
            path = parent().get_config_path() + '.' + path
        return path

    def get_sub_option_bag(self,
                           bag: Union[OptionBag, ConfigBag],
                           path: str,
                           index: Optional[int],
                           validate_properties: bool,
                           leadership_length: int=None,
                           *,
                           properties=undefined,
                           follower_not_apply_requires: bool=False,
                           allow_dynoption: bool=False,
                           ) -> List[OptionBag]:
        """Get the suboption for path and the name of the option
        :returns: option_bag
        """
        # pylint: disable=too-many-branches,too-many-locals,too-many-arguments
        if isinstance(bag, ConfigBag):
            option_bag = OptionBag(self.get_description(),
                                   None,
                                   bag,
                                   )
        else:
            option_bag = bag
            if option_bag.option != option_bag.config_bag.context.get_description():
                path = path[len(option_bag.path) + 1:]
        split_path = path.split('.')
        last_idx = len(split_path) - 1
        suboption = option_bag.option
        options_bag = []
        sub_option_bag = option_bag
        for idx, step in enumerate(split_path):
            if not suboption.impl_is_optiondescription():
                raise TypeError(f'{suboption.impl_getpath()} is not an optiondescription')

            if not idx and option_bag.option == self.get_description():
                subpath = None
            else:
                subpath = suboption.impl_getpath()
            option = suboption.get_child(step,
                                         option_bag.config_bag,
                                         subpath,
                                         allow_dynoption=allow_dynoption,
                                         )
            if idx == last_idx:
                option_index = index
                apply_requires = not follower_not_apply_requires or \
                        option.impl_is_optiondescription() or \
                        not option.impl_is_follower()
                if option_index is not None:
                    if option.impl_is_optiondescription() or \
                            option.impl_is_symlinkoption() or \
                            not option.impl_is_follower():
                        raise ConfigError('index must be set only with a follower option')
                    if leadership_length is not None:
                        length = leadership_length
                    else:
                        length = self.get_length_leadership(sub_option_bag)
                    if index >= length:
                        raise LeadershipError(_(f'index "{index}" is greater than the leadership '
                                                f'length "{length}" for option '
                                                f'"{option.impl_get_display_name()}"'))
                option_properties = properties
            else:
                option_index = None
                apply_requires = True
                option_properties = undefined
            sub_option_bag = OptionBag(option,
                                       option_index,
                                       option_bag.config_bag,
                                       properties=option_properties,
                                       apply_requires=apply_requires,
                                       )
            if validate_properties:
                self.get_settings().validate_properties(sub_option_bag)
            suboption = option
            options_bag.append(sub_option_bag)
        return options_bag

    def impl_getname(self):
        """get config name
        """
        return self._impl_name  # pylint: disable=no-member


# ____________________________________________________________
class KernelConfig(_CommonConfig):
    """main configuration management entry
    """
    # pylint: disable=too-many-instance-attributes
    __slots__ = ('__weakref__',
                 '_impl_name',
                 '_display_name',
                 '_impl_symlink',
                 '_storage',
                 )
    impl_type = 'config'

    def __init__(self,
                 descr,
                 force_values=None,
                 force_settings=None,
                 name=None,
                 display_name=None,
                 _duplicate=False,
                 ):
        """ Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        """
        # pylint: disable=too-many-arguments,too-many-arguments
        self._display_name = display_name
        self.parents = []
        self._impl_symlink = []
        self._impl_name = name
        if isinstance(descr, Leadership):
            raise ConfigError(_('cannot set leadership object has root optiondescription'))
        if isinstance(descr, DynOptionDescription):
            msg = _('cannot set dynoptiondescription object has root optiondescription')
            raise ConfigError(msg)
        if force_settings is not None and force_values is not None:
            self._impl_settings = force_settings
            self._impl_permissives_cache = Cache()
            self.properties_cache = Cache()
            self._impl_values = Values(force_values)
            self._impl_values_cache = Cache()
        else:
            self._impl_settings = Settings()
            self._impl_permissives_cache = Cache()
            self.properties_cache = Cache()
            self._impl_values = Values()
            self._impl_values_cache = Cache()
        self._impl_context = weakref.ref(self)
        if None in [force_settings, force_values]:
            self._impl_build_all_caches(descr)
        super().__init__(descr,
                         self._impl_context,
                         None,
                         )


class KernelGroupConfig(_CommonConfig):
    """Group a config with same optiondescription tree
    """
    __slots__ = ('__weakref__',
                 '_impl_children',
                 '_impl_name',
                 '_display_name',
                 )
    impl_type = 'group'

    def __init__(self,
                 children,
                 display_name=None,
                 name=None,
                 _descr=None,
                 ):
        # pylint: disable=super-init-not-called
        names = []
        for child in children:
            name_ = child._impl_name
            names.append(name_)
        if len(names) != len(set(names)):
            while range(1, len(names) + 1):
                name = names.pop(0)
                if name in names:
                    raise ConflictError(_('config name must be uniq in '
                                          'groupconfig for "{0}"').format(name))

        self._impl_children = children
        self.parents = []
        self._display_name = display_name
        if name:
            self._impl_name = name
        self._impl_context = weakref.ref(self)
        self._impl_descr = _descr
        self._impl_path = None

    def get_children(self):
        """get all children
        """
        return self._impl_children

    def reset_cache(self,
                    option_bag,
                    resetted_opts=None,
                    ):
        if resetted_opts is None:
            resetted_opts = []
        if isinstance(self, KernelMixConfig):
            super().reset_cache(option_bag,
                                resetted_opts=copy(resetted_opts),
                                )
        for child in self._impl_children:
            if option_bag is not None:
                coption_bag = option_bag.copy()
                cconfig_bag = coption_bag.config_bag.copy()
                cconfig_bag.context = child
                coption_bag.config_bag = cconfig_bag
            else:
                coption_bag = None
            child.reset_cache(coption_bag,
                              resetted_opts=copy(resetted_opts),
                              )

    def set_value(self,
                  option_bag,
                  value,
                  only_config=False,
                  ):
        """Setattr not in current KernelGroupConfig, but in each children
        """
        ret = []
        for child in self._impl_children:
            cconfig_bag = option_bag.config_bag.copy()
            cconfig_bag.context = child
            if isinstance(child, KernelGroupConfig):
                ret.extend(child.set_value(option_bag,
                                           value,
                                           only_config=only_config,
                                           ))
            else:
                settings = child.get_settings()
                properties = settings.get_context_properties(child.properties_cache)
                permissives = settings.get_context_permissives()
                cconfig_bag.properties = properties
                cconfig_bag.permissives = permissives
                try:
                    coption_bag = child.get_sub_option_bag(cconfig_bag,
                                                           option_bag.path,
                                                           option_bag.index,
                                                           False,
                                                           )[-1]
                    child.set_value(coption_bag,
                                    value,
                                    )
                except PropertiesOptionError as err:
                    # pylint: disable=protected-access
                    ret.append(PropertiesOptionError(err._option_bag,
                                                     err.proptype,
                                                     err._settings,
                                                     err._opt_type,
                                                     err._name,
                                                     err._orig_opt))
                except (ValueError, LeadershipError, AttributeError) as err:
                    ret.append(err)
        return ret


    def find_group(self,
                   config_bag,
                   byname=None,
                   bypath=undefined,
                   byoption=undefined,
                   byvalue=undefined,
                   raise_if_not_found=True,
                   _sub=False,
                   ):
        """Find first not in current KernelGroupConfig, but in each children
        """
        # pylint: disable=too-many-arguments
        # if KernelMetaConfig, all children have same OptionDescription in
        # context so search only one time the option for all children
        if bypath is undefined and byname is not None and \
                 self.impl_type == 'meta':
            root_option_bag = OptionBag(self.get_description(),
                                        None,
                                        config_bag,
                                        )
            next(self.find(root_option_bag,
                           bytype=None,
                           byname=byname,
                           byvalue=undefined,
                           raise_if_not_found=raise_if_not_found,
                           with_option=True,
                           ))
            byname = None

        ret = []
        for child in self._impl_children:
            if isinstance(child, KernelGroupConfig):
                ret.extend(child.find_group(byname=byname,
                                            bypath=bypath,
                                            byoption=byoption,
                                            byvalue=byvalue,
                                            config_bag=config_bag,
                                            raise_if_not_found=False,
                                            _sub=True))
            else:
                cconfig_bag = config_bag.copy()
                cconfig_bag.context = child
                if cconfig_bag.properties is None:
                    settings = child.get_settings()
                    properties = settings.get_context_properties(child.properties_cache)
                    permissives = settings.get_context_permissives()
                    cconfig_bag.properties = properties
                    cconfig_bag.permissives = permissives
                root_option_bag = OptionBag(child.get_description(),
                                            None,
                                            cconfig_bag,
                                            )
                try:
                    next(child.find(root_option_bag,
                                    None,
                                    byname,
                                    byvalue,
                                    raise_if_not_found=False,
                                    only_path=bypath,
                                    only_option=byoption,
                                    ))
                    ret.append(child)
                except StopIteration:
                    pass
        if not _sub:
            self._find_return_results(ret != [],  # pylint: disable=use-implicit-booleaness-not-comparison
                                      raise_if_not_found,
                                      )
        return ret

    def reset(self,
              path: str,
              config_bag: ConfigBag,
              ) -> None:
        """reset value for specified path
        """
        for child in self._impl_children:
            settings = child.get_settings()
            cconfig_bag = config_bag.copy()
            cconfig_bag.context = child
            settings = child.get_settings()
            properties = settings.get_context_properties(child.properties_cache)
            permissives = settings.get_context_permissives()
            cconfig_bag.properties = properties
            cconfig_bag.permissives = permissives
            cconfig_bag.remove_validation()
            option_bag = child.get_sub_option_bag(cconfig_bag,
                                                  path,
                                                  None,
                                                  False,
                                                  )[-1]
            child.get_values().reset(option_bag)

    def getconfig(self,
                  name: str,
                  ) -> KernelConfig:
        """get a child from a config name
        """
        for child in self._impl_children:
            if name == child.impl_getname():
                return child
        raise ConfigError(_('unknown config "{}"').format(name))


class KernelMixConfig(KernelGroupConfig):
    """Kernel mixconfig: this config can have differents optiondescription tree
    """
    # pylint: disable=too-many-instance-attributes
    __slots__ = ('_impl_symlink',
                 '_storage',
                 )
    impl_type = 'mix'

    def __init__(self,
                 optiondescription,
                 children,
                 name=None,
                 display_name=None,
                 _duplicate=False,
                 ):
        self._impl_name = name
        self._impl_symlink = []
        for child in children:
            if not isinstance(child, (KernelConfig, KernelMixConfig)):
                raise TypeError(_("child must be a Config, MixConfig or MetaConfig"))
            child.parents.append(weakref.ref(self))
        self._impl_settings = Settings()
        self._impl_settings._properties = deepcopy(self._impl_settings._properties)
        self._impl_settings._permissives = deepcopy(self._impl_settings._permissives)
        self._impl_permissives_cache = Cache()
        self.properties_cache = Cache()
        self._impl_values = Values()
        self._impl_values._values = deepcopy(self._impl_values._values)
        self._impl_values_cache = Cache()
        self._display_name = display_name
        self._impl_build_all_caches(optiondescription)
        super().__init__(children,
                         _descr=optiondescription,
                         display_name=display_name,
                         )

    def set_value(self,
                  option_bag,
                  value,
                  only_config=False,
                  force_default=False,
                  force_dont_change_value=False,
                  force_default_if_same=False,
                  ):
        """only_config: could be set if you want modify value in all Config included in
                        this KernelMetaConfig
        """
        # pylint: disable=too-many-branches,too-many-nested-blocks,too-many-locals,too-many-arguments
        ret = []
        if only_config:
            if force_default or force_default_if_same or force_dont_change_value:
                raise ValueError(_('force_default, force_default_if_same or '
                                   'force_dont_change_value cannot be set with'
                                   ' only_config'))
        else:
            if force_default or force_default_if_same or force_dont_change_value:
                if force_default and force_dont_change_value:
                    raise ValueError(_('force_default and force_dont_change_value'
                                       ' cannot be set together'))
                for child in self._impl_children:
                    cconfig_bag = option_bag.config_bag.copy()
                    cconfig_bag.context = child
                    settings = child.get_settings()
                    properties = settings.get_context_properties(child.properties_cache)
                    cconfig_bag.properties = properties
                    cconfig_bag.permissives = settings.get_context_permissives()
                    try:
                        if self.impl_type == 'meta':
                            obj = self
                        else:
                            obj = child
                        validate_properties = not force_default and not force_default_if_same
                        moption_bag = obj.get_sub_option_bag(cconfig_bag,
                                                             option_bag.path,
                                                             option_bag.index,
                                                             validate_properties,
                                                             )[-1]
                        if force_default_if_same:
                            if not child.get_values().hasvalue(option_bag.path):
                                child_value = undefined
                            else:
                                child_value = child.get_value(moption_bag)
                        if force_default or (force_default_if_same and value == child_value):
                            child.get_values().reset(moption_bag)
                            continue
                        if force_dont_change_value:
                            child_value = child.get_value(moption_bag)
                            if value != child_value:
                                child.set_value(moption_bag,
                                                     child_value,
                                                     )
                    except PropertiesOptionError as err:
                        # pylint: disable=protected-access
                        ret.append(PropertiesOptionError(err._option_bag,
                                                         err.proptype,
                                                         err._settings,
                                                         err._opt_type,
                                                         err._name,
                                                         err._orig_opt,
                                                         ))
                    except (ValueError, LeadershipError, AttributeError) as err:
                        ret.append(err)

        try:
            moption_bag = self.get_sub_option_bag(option_bag.config_bag,
                                                  option_bag.path,
                                                  option_bag.index,
                                                  not only_config,
                                                  )[-1]
            if only_config:
                ret = super().set_value(moption_bag,
                                        value,
                                        only_config=only_config,
                                        )
            else:
                _CommonConfig.set_value(self,
                                        moption_bag,
                                        value,
                                        )
        except (PropertiesOptionError, ValueError, LeadershipError) as err:
            ret.append(err)
        return ret

    def reset(self,
              path: str,
              only_children: bool,
              config_bag: ConfigBag,
              ) -> None:
        """reset value for a specified path
        """
        # pylint: disable=arguments-differ
        rconfig_bag = config_bag.copy()
        rconfig_bag.remove_validation()
        if self.impl_type == 'meta':
            option_bag = self.get_sub_option_bag(config_bag,
                                                 path,
                                                 None,
                                                 True,
                                                 )[-1]
        elif not only_children:
            try:
                option_bag = self.get_sub_option_bag(rconfig_bag,
                                                     path,
                                                     None,
                                                     True,
                                                     )[-1]
            except AttributeError:
                only_children = True
        for child in self._impl_children:
            rconfig_bag.context = child
            try:
                if self.impl_type == 'meta':
                    moption_bag = option_bag
                    moption_bag.config_bag = rconfig_bag
                else:
                    moption_bag = child.get_sub_option_bag(rconfig_bag,
                                                           path,
                                                           None,
                                                           True,
                                                           )[-1]
                child.get_values().reset(moption_bag)
            except AttributeError:
                pass
            if isinstance(child, KernelMixConfig):
                child.reset(path,
                            False,
                            rconfig_bag,
                            )
        if not only_children:
            option_bag.config_bag = config_bag
            self.get_values().reset(option_bag)

    def new_config(self,
                   name=None,
                   type_='config',
                   ):
        """Create a new config/metaconfig/mixconfig and add it to this MixConfig"""
        if name:
            for child in self._impl_children:
                if child.impl_getname() == name:
                    raise ConflictError(_('config name must be uniq in '
                                          'groupconfig for {0}').format(child))
        assert type_ in ('config', 'metaconfig', 'mixconfig'), _('unknown type {}').format(type_)
        if type_ == 'config':
            config = KernelConfig(self._impl_descr,
                                  name=name)
        elif type_ == 'metaconfig':
            config = KernelMetaConfig([],
                                      optiondescription=self._impl_descr,
                                      name=name,
                                      )
        elif type_ == 'mixconfig':
            config = KernelMixConfig(children=[],
                                     optiondescription=self._impl_descr,
                                     name=name,
                                     )
        # Copy context properties/permissives
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        settings.set_context_properties(properties,
                                        config,
                                        )
        settings.set_context_permissives(settings.get_context_permissives())
        settings.ro_append = settings.ro_append
        settings.rw_append = settings.rw_append
        settings.ro_remove = settings.ro_remove
        settings.rw_remove = settings.rw_remove
        settings.default_properties = settings.default_properties

        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        return config

    def add_config(self,
                   config,
                   ):
        """Add a child config to a mix config"""
        if not config.impl_getname():
            raise ConfigError(_('config added has no name, the name is mandatory'))
        if config.impl_getname() in [child.impl_getname() for child in self._impl_children]:
            raise ConflictError(_('config name "{0}" is not uniq in '
                                  'groupconfig "{1}"').format(config.impl_getname(),
                                                              self.impl_getname()),
                                )
        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        config.reset_cache(None, None)

    def remove_config(self,
                      name,
                      ):
        """Remove a child config to a mix config by it's name"""
        for current_index, child in enumerate(self._impl_children):
            if name == child.impl_getname():
                child.reset_cache(None, None)
                break
        else:
            raise ConfigError(_(f'cannot find the config {name}'))
        for child_index, parent in enumerate(child.parents):
            if parent() == self:
                break
        else:  # pragma: no cover
            raise ConfigError(_('cannot find the config {}').format(self.impl_getname()))
        self._impl_children.pop(current_index)
        child.parents.pop(child_index)
        return child


class KernelMetaConfig(KernelMixConfig):
    """Meta config
    """
    __slots__ = tuple()
    impl_type = 'meta'

    def __init__(self,
                 children,
                 optiondescription=None,
                 name=None,
                 display_name=None,
                 _duplicate=False,
                 ):
        descr = None
        if optiondescription is not None:
            if not _duplicate:
                new_children = []
                for child_name in children:
                    assert isinstance(child_name, str), _('MetaConfig with optiondescription'
                                                          ' must have string has child, '
                                                          'not {}').format(child_name)
                    new_children.append(KernelConfig(optiondescription, name=child_name))
                children = new_children
            descr = optiondescription
        for child in children:
            if __debug__ and not isinstance(child, (KernelConfig,
                                                    KernelMetaConfig)):
                raise TypeError(_("child must be a Config or MetaConfig"))
            if descr is None:
                descr = child.get_description()
            elif descr is not child.get_description():
                raise ValueError(_('all config in metaconfig must '
                                   'have the same optiondescription'))
        super().__init__(descr,
                         children,
                         name=name,
                         display_name=display_name,
                         )

    def add_config(self,
                   config,
                   ):
        if self._impl_descr is not config.get_description():
            raise ValueError(_('metaconfig must '
                               'have the same optiondescription'))
        super().add_config(config)
