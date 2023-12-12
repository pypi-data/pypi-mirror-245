# -*- coding: utf-8 -*-
"takes care of the option's values and multi values"
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
from typing import Union, Optional, List, Any
from .error import ConfigError
from .setting import owners, undefined, forbidden_owners, OptionBag
from .autolib import Calculation
from .i18n import _


class Values:
    """This class manage value (default value, stored value or calculated value
    It's also responsible of a caching utility.
    """
    # pylint: disable=too-many-public-methods
    __slots__ = ('_values',
                 '_informations',
                 '__weakref__',
                 )

    def __init__(self,
                 default_values: Union[None, dict]=None,
                 ) -> None:
        """
        Initializes the values's dict.

        :param default_values: values stored by default for this object

        """
        self._informations = {}
        # set default owner
        if not default_values:
            default_values = {None: {None: [None, owners.user]}}
        self._values = default_values

    #______________________________________________________________________
    # get value
    def get_cached_value(self,
                         option_bag: OptionBag,
                         ) -> Any:
        """get value directly in cache if set
        otherwise calculated value and set it in cache

        :returns: value
        """
        # try to retrive value in cache
        setting_properties = option_bag.config_bag.properties
        cache = option_bag.config_bag.context.get_values_cache()
        is_cached, value, validated = cache.getcache(option_bag,
                                                     'values',
                                                     )
        # no cached value so get value
        if not is_cached:
            value, has_calculation = self.get_value(option_bag)
        # validates and warns value
        if not validated:
            validate = option_bag.option.impl_validate(value,
                                                       option_bag,
                                                       check_error=True,
                                                       )
        if 'warnings' in setting_properties:
            option_bag.option.impl_validate(value,
                                            option_bag,
                                            check_error=False,
                                            )
        # set value to cache
        if not is_cached and not has_calculation:
            cache.setcache(option_bag,
                           value,
                           validated=validate,
                           )
        if isinstance(value, list):
            # return a copy, so value cannot be modified
            value = value.copy()
        # and return it
        return value

    def get_value(self,
                  option_bag: OptionBag,
                  ) -> Any:
        """actually retrieves the stored value or the default value (value modified by user)

        :returns: value
        """
        # get owner and value from store
        default_value = [undefined, owners.default]
        value, owner = self._values.get(option_bag.path, {}).get(option_bag.index, default_value)
        if owner == owners.default or \
                ('frozen' in option_bag.properties and \
                 ('force_default_on_freeze' in option_bag.properties or \
                 self.check_force_to_metaconfig(option_bag))):
            # the value is a default value
            # get it
            value = self.get_default_value(option_bag)
        value, has_calculation = self.get_calculated_value(option_bag,
                                                           value,
                                                           )
        return value, has_calculation

    def get_default_value(self,
                          option_bag: OptionBag,
                          ) -> Any:
        """get default value:
        - get parents config value or
        - get calculated value or
        - get default value
        """
        moption_bag = self._get_modified_parent(option_bag)
        if moption_bag is not None:
            # retrieved value from parent config
            return moption_bag.config_bag.context.get_values().get_cached_value(moption_bag)

        # now try to get calculated value:
        value, _has_calculation = self.get_calculated_value(option_bag,
                                                            option_bag.option.impl_getdefault(),
                                                            )
        if option_bag.index is not None and isinstance(value, (list, tuple)) \
                and (not option_bag.option.impl_is_submulti() or \
                not value or isinstance(value[0], list)):
            # if index (so slave), must return good value for this index
            # for submulti, first index is a list, assume other data are list too
            if len(value) > option_bag.index:
                value = value[option_bag.index]
            else:
                # no value for this index, retrieve default multi value
                # default_multi is already a list for submulti
                value, _has_calculation = self.get_calculated_value(option_bag,
                                                                    option_bag.option.impl_getdefault_multi(),
                                                                    )
        return value

    def get_calculated_value(self,
                             option_bag,
                             value,
                             reset_cache=True,
                             ) -> Any:
        """value could be a calculation, in this case do calculation
        """
        has_calculation = False
        if isinstance(value, Calculation):
            try:
                value = value.execute(option_bag)
            except ConfigError as err:
                msg = _(f'error when calculating "{option_bag.option.impl_get_display_name()}": '
                        f'{err} : {option_bag.path}')
                raise ConfigError(msg) from err
            has_calculation = True
        elif isinstance(value, list):
            # if value is a list, do subcalculation
            for idx, val in enumerate(value):
                value[idx], _has_calculation = self.get_calculated_value(option_bag,
                                                                         val,
                                                                         reset_cache=False,
                                                                         )
                if _has_calculation:
                    has_calculation = True
        if reset_cache:
            self.reset_cache_after_calculation(option_bag,
                                               value,
                                               )
        return value, has_calculation

    #______________________________________________________________________
    def check_force_to_metaconfig(self,
                                  option_bag: OptionBag,
                                  ) -> bool:
        """Check if the value must be retrieve from parent metaconfig or not
        """
        # force_metaconfig_on_freeze is set to an option and context is a kernelconfig
        #   => to metaconfig
        # force_metaconfig_on_freeze is set *explicitly* to an option and context is a
        #   kernelmetaconfig => to sub metaconfig
        if 'force_metaconfig_on_freeze' in option_bag.properties:
            settings = option_bag.config_bag.context.get_settings()
            if option_bag.config_bag.context.impl_type == 'config':
                return True
            # it's a not a config, force to metaconfig only in *explicitly* set
            return 'force_metaconfig_on_freeze' in settings.get_stored_properties(option_bag.path,
                                                                                  option_bag.index,
                                                                                  frozenset(),
                                                                                  )
        return False

    def reset_cache_after_calculation(self,
                                      option_bag,
                                      value,
                                      ):
        """if value is modification after calculation, invalid cache
        """
        cache = option_bag.config_bag.context.get_values_cache()
        is_cache, cache_value, _ = cache.getcache(option_bag,
                                                  'values',
                                                  expiration=False,
                                                  )
        if not is_cache or cache_value == value:
            # calculation return same value as previous value,
            # so do not invalidate cache
            return
        # calculated value is a new value, so reset cache
        option_bag.config_bag.context.reset_cache(option_bag)
        # and manage force_store_value
        self._set_force_value_suffix(option_bag)

    def isempty(self,
                option_bag: OptionBag,
                value: Any,
                force_allow_empty_list: bool,
                ) -> bool:
        """convenience method to know if an option is empty
        """
        if option_bag.index is None and option_bag.option.impl_is_submulti():
            # index is not set
            isempty = True
            for val in value:
                isempty = self._isempty_multi(val, force_allow_empty_list)
                if isempty:
                    break
        elif (option_bag.index is None or \
                (option_bag.index is not None and option_bag.option.impl_is_submulti())) and \
                option_bag.option.impl_is_multi():
            # it's a single list
            isempty = self._isempty_multi(value, force_allow_empty_list)
        else:
            isempty = value is None or value == ''
        return isempty

    def _isempty_multi(self,
                       value: Any,
                       force_allow_empty_list: bool,
                       ) -> bool:
        if not isinstance(value, list):
            return False
        return (not force_allow_empty_list and value == []) or None in value or '' in value

    #______________________________________________________________________
    # set value
    def set_value(self,
                  option_bag: OptionBag,
                  value: Any,
                  ) -> None:
        """set value to option
        """
        owner = self.get_context_owner()
        setting_properties = option_bag.config_bag.properties
        ori_value = value
        if 'validator' in setting_properties:
            value, has_calculation = self.setvalue_validation(value,
                                                              option_bag,
                                                              )

        elif isinstance(value, list):
            # copy
            value = value.copy()
        self._setvalue(option_bag,
                       ori_value,
                       owner,
                       )
        validator = 'validator' in setting_properties and \
                'demoting_error_warning' not in setting_properties
        if validator and not has_calculation:
            cache = option_bag.config_bag.context.get_values_cache()
            cache.setcache(option_bag,
                           value,
                           validated=validator,
                           )
        elif 'validator' in setting_properties and has_calculation:
            cache = option_bag.config_bag.context.get_values_cache()
            cache.delcache(option_bag.path)
        if 'force_store_value' in setting_properties and option_bag.option.impl_is_leader():
            leader = option_bag.option.impl_get_leadership()
            leader.follower_force_store_value(value,
                                              option_bag.config_bag,
                                              owners.forced,
                                              )

    def setvalue_validation(self,
                            value,
                            option_bag,
                            ):
        """validate value before set value
        """
        settings = option_bag.config_bag.context.get_settings()
        # First validate properties with this value
        opt = option_bag.option
        settings.validate_frozen(option_bag)
        val, has_calculation = self.get_calculated_value(option_bag,
                                                         value,
                                                         False,
                                                         )
        settings.validate_mandatory(val,
                                    option_bag,
                                    )
        # Value must be valid for option
        opt.impl_validate(val,
                          option_bag,
                          check_error=True,
                          )
        if 'warnings' in option_bag.config_bag.properties:
            # No error found so emit warnings
            opt.impl_validate(val,
                              option_bag,
                              check_error=False,
                              )
        return val, has_calculation

    def _setvalue(self,
                  option_bag: OptionBag,
                  value: Any,
                  owner: str,
                  ) -> None:
        option_bag.config_bag.context.reset_cache(option_bag)
        self.set_storage_value(option_bag.path,
                               option_bag.index,
                               value,
                               owner,
                               )
        self._set_force_value_suffix(option_bag)

    def set_storage_value(self,
                          path,
                          index,
                          value,
                          owner,
                          ):
        """set a value
        """
        self._values.setdefault(path, {})[index] = [value, owner]

    def _set_force_value_suffix(self, option_bag: OptionBag) -> None:
        """ force store value for an option for suffixes
        """
        # pylint: disable=too-many-locals
        if 'force_store_value' not in option_bag.config_bag.properties:
            return

        for woption in option_bag.option._get_suffixes_dependencies():  # pylint: disable=protected-access
            # options from dependencies are weakref
            option = woption()
            force_store_options = []
            for coption in option.get_children_recursively(None,
                                                           None,
                                                           option_bag.config_bag,
                                                           ):
                if 'force_store_value' in coption.impl_getproperties():
                    force_store_options.append(coption)
            if not force_store_options:
                continue
            for coption in force_store_options:
                if coption.impl_is_follower():
                    leader = coption.impl_get_leadership().get_leader()
                    loption_bag = OptionBag(leader,
                                            None,
                                            option_bag.config_bag,
                                            properties=frozenset(),
                                            )
                    indexes = range(len(self.get_value(loption_bag)[0]))
                else:
                    indexes = [None]
                for index in indexes:
                    for coption_bag in option.get_sub_children(coption,
                                                               option_bag.config_bag,
                                                               index=index,
                                                               properties=frozenset(),
                                                               ):
                        default_value = [self.get_value(coption_bag)[0], owners.forced]
                        self._values.setdefault(coption_bag.path, {})[index] = default_value

    def _get_modified_parent(self,
                             option_bag: OptionBag,
                             ) -> Optional[OptionBag]:
        """ Search in differents parents a Config with a modified value
        If not found, return None
        For follower option, return the Config where leader is modified
        """
        def build_option_bag(option_bag, parent):
            doption_bag = option_bag.copy()
            config_bag = option_bag.config_bag.copy()
            config_bag.context = parent
            config_bag.unrestraint()
            doption_bag.config_bag = config_bag
            return doption_bag

        for parent in option_bag.config_bag.context.get_parents():
            doption_bag = build_option_bag(option_bag, parent)
            if 'force_metaconfig_on_freeze' in option_bag.properties:
                # remove force_metaconfig_on_freeze only if option in metaconfig
                # hasn't force_metaconfig_on_freeze properties
                ori_properties = doption_bag.properties
                settings = doption_bag.config_bag.context.get_settings()
                doption_bag.properties = settings.getproperties(doption_bag)
                if not self.check_force_to_metaconfig(doption_bag):
                    doption_bag.properties = ori_properties - {'force_metaconfig_on_freeze'}
                else:
                    doption_bag.properties = ori_properties
            parent_owner = parent.get_values().getowner(doption_bag,
                                                        only_default=True,
                                                        )
            if parent_owner != owners.default:
                return doption_bag

        return None


    #______________________________________________________________________
    # owner

    def is_default_owner(self,
                         option_bag: OptionBag,
                         validate_meta: bool=True,
                         ) -> bool:
        """is default owner for an option
        """
        return self.getowner(option_bag,
                             validate_meta=validate_meta,
                             only_default=True,
                             ) == owners.default

    def hasvalue(self,
                 path,
                 index=None,
                 ):
        """if path has a value
        return: boolean
        """
        has_path = path in self._values
        if index is None:
            return has_path
        if has_path:
            return index in self._values[path]
        return False

    def getowner(self,
                 option_bag,
                 validate_meta=True,
                 only_default=False,
                 ):
        """
        retrieves the option's owner

        :param opt: the `option.Option` object
        :param force_permissive: behaves as if the permissive property
                                 was present
        :returns: a `setting.owners.Owner` object
        """
        context = option_bag.config_bag.context
        opt = option_bag.option
        if opt.impl_is_symlinkoption():
            option_bag.ori_option = opt
            opt = opt.impl_getopt()
            option_bag.option = opt
            option_bag.path = opt.impl_getpath()
        settings = context.get_settings()
        settings.validate_properties(option_bag)
        if 'frozen' in option_bag.properties and \
                'force_default_on_freeze' in option_bag.properties:
            return owners.default
        if only_default:
            if self.hasvalue(option_bag.path,
                             index=option_bag.index,
                             ):
                owner = 'not_default'
            else:
                owner = owners.default
        else:
            owner = self._values.get(option_bag.path, {}).get(option_bag.index,
                                                              [undefined, owners.default],
                                                              )[1]
        if validate_meta is not False and (owner is owners.default or
                                           'frozen' in option_bag.properties and
                                           'force_metaconfig_on_freeze' in option_bag.properties):
            moption_bag = self._get_modified_parent(option_bag)
            if moption_bag is not None:
                values = moption_bag.config_bag.context.get_values()
                owner = values.getowner(moption_bag,
                                        only_default=only_default,
                                        )
            elif 'force_metaconfig_on_freeze' in option_bag.properties:
                return owners.default
        return owner

    def set_owner(self,
                  option_bag,
                  owner,
                  ):
        """
        sets a owner to an option

        :param option_bag: the `OptionBag` object
        :param owner: a valid owner, that is a `setting.owners.Owner` object
        """
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))

        if not self.hasvalue(option_bag.path,
                             index=option_bag.index,
                             ):
            raise ConfigError(_(f'no value for {option_bag.path} cannot change owner to {owner}'))
        option_bag.config_bag.context.get_settings().validate_frozen(option_bag)
        self._values[option_bag.path][option_bag.index][1] = owner
    #______________________________________________________________________
    # reset

    def reset(self, option_bag: OptionBag) -> None:
        """reset value for an option
        """
        context = option_bag.config_bag.context
        hasvalue = self.hasvalue(option_bag.path)
        setting_properties = option_bag.config_bag.properties

        if hasvalue and 'validator' in option_bag.config_bag.properties:
            fake_context = context.gen_fake_values()
            config_bag = option_bag.config_bag.copy()
            config_bag.remove_validation()
            config_bag.context = fake_context
            soption_bag = option_bag.copy()
            soption_bag.config_bag = config_bag
            fake_value = fake_context.get_values()
            fake_value.reset(soption_bag)
            soption_bag.config_bag.properties = option_bag.config_bag.properties
            value = fake_value.get_default_value(soption_bag)
            fake_value.setvalue_validation(value,
                                           soption_bag,
                                           )
        opt = option_bag.option
        if opt.impl_is_leader():
            opt.impl_get_leadership().reset(option_bag.config_bag)
        if hasvalue:
            if 'force_store_value' in option_bag.config_bag.properties and \
                    'force_store_value' in option_bag.properties:
                value = self.get_default_value(option_bag)

                self._setvalue(option_bag,
                               value,
                               owners.forced,
                               )
            else:
                # for leader only
                value = None
                if option_bag.path in self._values:
                    del self._values[option_bag.path]
            context.reset_cache(option_bag)
            if 'force_store_value' in setting_properties and option_bag.option.impl_is_leader():
                if value is None:
                    value = self.get_default_value(option_bag)
                leader = option_bag.option.impl_get_leadership()
                leader.follower_force_store_value(value,
                                                  option_bag.config_bag,
                                                  owners.forced,
                                                  )
    #______________________________________________________________________
    # Follower

    def get_max_length(self, path: str) -> int:
        """get max index for a follower and determine the length of the follower
        """
        values = self._values.get(path, {})
        if values:
            return max(values) + 1
        return 0

    def reset_follower(self,
                       option_bag: OptionBag,
                       ) -> None:
        """reset value for a follower
        """
        if not self.hasvalue(option_bag.path,
                             index=option_bag.index,
                             ):
            return
        context = option_bag.config_bag.context
        setting_properties = option_bag.config_bag.properties
        if 'validator' in setting_properties:
            fake_context = context.gen_fake_values()
            fake_value = fake_context.get_values()
            config_bag = option_bag.config_bag.copy()
            config_bag.remove_validation()
            config_bag.context = fake_context
            soption_bag = option_bag.copy()
            soption_bag.config_bag = config_bag
            fake_value.reset_follower(soption_bag)
            value = fake_value.get_default_value(soption_bag)
            fake_value.setvalue_validation(value,
                                           soption_bag)
        if 'force_store_value' in setting_properties and \
                'force_store_value' in option_bag.properties:
            value = self.get_default_value(option_bag)

            self._setvalue(option_bag,
                           value,
                           owners.forced,
                           )
        else:
            self.resetvalue_index(option_bag)
        context.reset_cache(option_bag)

    def resetvalue_index(self, option_bag: OptionBag) -> None:
        """reset a value for a follower at an index
        """
        if option_bag.path in self._values and option_bag.index in self._values[option_bag.path]:
            del self._values[option_bag.path][option_bag.index]

    def reduce_index(self, option_bag: OptionBag) -> None:
        """reduce follower's value from a specified index
        """
        self.resetvalue_index(option_bag)
        for index in range(option_bag.index + 1, self.get_max_length(option_bag.path)):
            if self.hasvalue(option_bag.path,
                             index=index,
                             ):
                self._values[option_bag.path][index - 1] = self._values[option_bag.path].pop(index)

    def reset_leadership(self,
                         option_bag: OptionBag,
                         leadership_option_bag: OptionBag,
                         index: int,
                         ) -> None:
        """reset leadershop from an index
        """
        current_value = self.get_cached_value(option_bag)
        length = len(current_value)
        if index >= length:
            raise IndexError(_('index {index} is greater than the length {length} '
                               'for option "{option_bag.option.impl_get_display_name()}"'))
        current_value.pop(index)
        leadership_option_bag.option.pop(index,
                                         option_bag.config_bag,
                                         )
        self.set_value(option_bag,
                       current_value,
                       )

    #______________________________________________________________________
    # information

    def set_information(self,
                        option_bag,
                        key,
                        value,
                        ):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        if option_bag is None:
            path = None
        else:
            path = option_bag.path
        self._informations.setdefault(path, {})[key] = value
        if path is None:
            return
        for key, options in option_bag.option.get_dependencies_information().items():
            for option in options:
                cache_option_bag = OptionBag(option,
                                             None,
                                             option_bag.config_bag,
                                             properties=None,
                                             )
                cache_option_bag.config_bag.context.reset_cache(cache_option_bag)

    def get_information(self,
                        option_bag,
                        name,
                        default,
                        ):
        """retrieves one information's item

        :param name: the item string (ex: "help")
        """
        if option_bag is None:
            path = None
        else:
            path = option_bag.path
        try:
            return self._informations[path][name]
        except KeyError as err:
            if option_bag:
                return option_bag.option.impl_get_information(name, default)
            if default is not undefined:
                return default
            raise ValueError(_("information's item not found: {0}").format(name)) from err

    def del_information(self,
                        key: Any,
                        raises: bool=True,
                        path: str=None,
                        ):
        """delete information for a specified key
        """
        if path in self._informations and key in self._informations[path]:
            del self._informations[path][key]
        elif raises:
            raise ValueError(_(f"information's item not found \"{key}\""))

    def list_information(self,
                         path: str=None,
                         ) -> List[str]:
        """list all informations keys for a specified path
        """
        return list(self._informations.get(path, {}).keys())

    #____________________________________________________________
    # default owner methods
    def set_context_owner(self, owner: str) -> None:
        """set the context owner
        """
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))
        self._values[None][None][1] = owner

    def get_context_owner(self) -> str:
        """get the context owner
        """
        return self._values[None][None][1]
