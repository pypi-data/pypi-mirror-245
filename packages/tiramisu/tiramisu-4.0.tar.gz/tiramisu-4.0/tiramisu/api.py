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
# ____________________________________________________________
from inspect import getdoc
from typing import List, Set, Any, Optional, Callable, Dict
from warnings import catch_warnings, simplefilter
from functools import wraps
from copy import deepcopy


from .error import ConfigError, LeadershipError, ValueErrorWarning
from .i18n import _
from .setting import ConfigBag, OptionBag, owners, groups, undefined, \
                     FORBIDDEN_SET_PROPERTIES, SPECIAL_PROPERTIES
from .config import KernelConfig, KernelGroupConfig, KernelMetaConfig, KernelMixConfig
from .option import RegexpOption, OptionDescription, ChoiceOption, Leadership
from .todict import TiramisuDict
from .autolib import Calculation


TIRAMISU_VERSION = 4


class TiramisuHelp:
    _tmpl_help = '    {0}\t{1}'

    def help(self,
             _display: bool=True) -> List[str]:
        def display(doc=''):
            if _display: # pragma: no cover
                print(doc)
        all_modules = dir(self)
        modules = []
        max_len = 0
        force = False
        for module_name in all_modules:
            if module_name in ['forcepermissive', 'unrestraint', 'nowarnings']:
                force = True
                max_len = max(max_len, len('forcepermissive'))
            elif module_name != 'help' and not module_name.startswith('_'):
                modules.append(module_name)
                max_len = max(max_len, len(module_name))
        modules.sort()

        display(_(getdoc(self)))
        display()
        if force:
            display(_('Settings:'))
            display(self._tmpl_help.format('forcepermissive',
                                           _('Access to option without verifying permissive '
                                             'properties'),
                                           ).expandtabs(max_len + 10))
            display(self._tmpl_help.format('unrestraint',
                                           _('Access to option without property restriction')
                                           ).expandtabs(max_len + 10))
            display(self._tmpl_help.format('nowarnings',
                                           _('Do not warnings during validation')
                                           ).expandtabs(max_len + 10))
            display()
        if isinstance(self, TiramisuDispatcherOption):
            doc = _(getdoc(self.__call__))
            display(_('Call: {}').format(doc))
            display()
        display(_('Commands:'))
        for module_name in modules:
            module = getattr(self, module_name)
            doc = _(getdoc(module))
            display(self._tmpl_help.format(module_name, doc).expandtabs(max_len + 10))
        display()

    def __dir__(self):
        if '_registers' in super().__dir__():
            return list(self._registers.keys())
        return super().__dir__()


class CommonTiramisu(TiramisuHelp):
    _validate_properties = True

    def _get_options_bag(self,
                         follower_not_apply_requires: bool,
                         ) -> OptionBag:
        try:
            options_bag = self._config_bag.context.get_sub_option_bag(self._config_bag,
                                                                      self._path,
                                                                      self._index,
                                                                      self._validate_properties,
                                                                      follower_not_apply_requires=follower_not_apply_requires,
                                                                      )
        except AssertionError as err:
            raise ConfigError(str(err))
        except Exception as err:
            raise err
        return options_bag


def option_type(typ):
    if not isinstance(typ, list):
        types = [typ]
    else:
        types = typ

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            self = args[0]
            config_bag = self._config_bag
            if self._config_bag.context.impl_type == 'group' and 'group' in types:
                options_bag = [OptionBag(None,
                                         None,
                                         self._config_bag,
                                         path=self._path,
                                         )]
                kwargs['is_group'] = True
                return func(self, options_bag, *args[1:], **kwargs)
            options_bag = self._get_options_bag('with_index' not in types)
            option = options_bag[-1].option
            if option.impl_is_optiondescription() and 'optiondescription' in types or \
                    option.impl_is_optiondescription() and option.impl_is_leadership() and 'leadership' in types or \
                    not option.impl_is_optiondescription() and (
                        option.impl_is_symlinkoption() and 'symlink' in types or \
                        not option.impl_is_symlinkoption() and (
                            'option' in types or \
                            option.impl_is_leader() and 'leader' in types or \
                            option.impl_is_follower() and 'follower' in types or \
                            isinstance(option, ChoiceOption) and 'choice' in types)):
                if not option.impl_is_optiondescription() and \
                        not option.impl_is_symlinkoption() and \
                        option.impl_is_follower():
                    # default is "without_index"
                    if 'with_index' not in types and 'with_or_without_index' not in types and \
                            self._index is not None:
                        msg = _('please do not specify index '
                                f'({self.__class__.__name__}.{func.__name__})')
                        raise ConfigError(_(msg))
                    if self._index is None and 'with_index' in types:
                        msg = _('please specify index with a follower option '
                                f'({self.__class__.__name__}.{func.__name__})')
                        raise ConfigError(msg)
                return func(self, options_bag, *args[1:], **kwargs)
            msg = _('please specify a valid sub function '
                    f'({self.__class__.__name__}.{func.__name__})')
            raise ConfigError(msg)
        wrapped.func = func
        return wrapped
    return wrapper


class CommonTiramisuOption(CommonTiramisu):
    _validate_properties = False

    def __init__(self,
                 path: str,
                 index: Optional[int],
                 config_bag: ConfigBag,
                 ) -> None:
        self._path = path
        self._index = index
        self._config_bag = config_bag

    def __getattr__(self, subfunc):
        raise ConfigError(_(f'please specify a valid sub function ({self.__class__.__name__}.{subfunc})'))


class _TiramisuOptionWalk:
    def _list(self,
              root_option_bag,
              type,
              group_type,
              recursive,
              ):
        assert type in ('all', 'option', 'optiondescription'), \
                _('unknown list type {}').format(type)
        assert group_type is None or isinstance(group_type, groups.GroupType), \
                _("unknown group_type: {0}").format(group_type)
        options = []
        types = {'option': ['option'],
                 'optiondescription': ['optiondescription'],
                 'all': ['option', 'optiondescription']}[type]
        for option_bag in self._config_bag.context.walk(root_option_bag,
                                                        recursive=recursive,
                                                        types=types,
                                                        group_type=group_type,
                                                        flatten_leadership=True,
                                                        ):
            if isinstance(option_bag, dict):
                for opts_bag in option_bag.values():
                    if isinstance(opts_bag, OptionBag):
                        options.append(TiramisuOption(opts_bag.path,
                                                      opts_bag.index,
                                                      self._config_bag,
                                                      ))
                    else:
                        for opt_bag in opts_bag:
                            options.append(TiramisuOption(opt_bag.path,
                                                          opt_bag.index,
                                                          self._config_bag,
                                                          ))
            else:
                options.append(TiramisuOption(option_bag.path,
                                              option_bag.index,
                                              self._config_bag,
                                              ))
        return options


class _TiramisuOptionOptionDescription:
    """Manage option"""
    _validate_properties = False

    @option_type(['optiondescription', 'option', 'with_or_without_index', 'symlink'])
    def get(self, options_bag: List[OptionBag]):
        """Get Tiramisu option"""
        option_bag = options_bag[-1]
        return option_bag.option

    @option_type(['optiondescription'])
    def isleadership(self, options_bag: List[OptionBag]):
        """Test if option is a leader or a follower"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_is_leadership()

    @option_type(['optiondescription', 'option', 'with_or_without_index'])
    def doc(self, options_bag: List[OptionBag]):
        """Get option document"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_get_display_name()

    @option_type(['optiondescription', 'option', 'with_or_without_index'])
    def description(self, options_bag: List[OptionBag]):
        """Get option description"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_get_information('doc', None)

    @option_type(['optiondescription', 'option', 'symlink', 'with_or_without_index'])
    def name(self, options_bag: List[OptionBag]) -> str:
        """Get option name"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_getname()

    @option_type(['optiondescription', 'option', 'with_or_without_index', 'symlink'])
    def path(self, options_bag: List[OptionBag]) -> str:
        """Get option path"""
        option_bag = options_bag[-1]
        return option_bag.path

    @option_type(['optiondescription', 'option', 'symlink', 'with_or_without_index'])
    def has_dependency(self,
                       options_bag: List[OptionBag],
                       self_is_dep=True,
                       ) -> bool:
        """Test if option has dependency"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_has_dependency(self_is_dep)

    @option_type(['optiondescription', 'option'])
    def dependencies(self, options_bag: List[OptionBag]):
        """Get dependencies from this option"""
        option_bag = options_bag[-1]
        options = []
        for option in option_bag.option.get_dependencies(self._config_bag.context):
            options.append(TiramisuOption(option().impl_getpath(),
                                          None,
                                          self._config_bag,
                                          ))
        return options

    @option_type(['optiondescription', 'option', 'with_or_without_index', 'symlink'])
    def isoptiondescription(self, options_bag: List[OptionBag]):
        """Test if option is an optiondescription"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_is_optiondescription()

    @option_type(['optiondescription', 'option', 'with_or_without_index', 'symlink'])
    def properties(self,
                   options_bag: List[OptionBag],
                   only_raises=False,
                   uncalculated=False,
                   ):
        """Get properties for an option"""
        option_bag = options_bag[-1]
        settings = self._config_bag.context.get_settings()
        if uncalculated:
            return settings.getproperties(option_bag,
                                          uncalculated=True,
                                          )
        if not only_raises:
            return settings.getproperties(option_bag,
                                          apply_requires=False,
                                          )
        return settings.calc_raises_properties(option_bag,
                                               apply_requires=False,
                                               uncalculated=uncalculated,
                                               )


class _TiramisuOptionOption(_TiramisuOptionOptionDescription):
    """Manage option"""
    @option_type(['option', 'symlink', 'with_or_without_index'])
    def ismulti(self, options_bag: List[OptionBag]):
        """Test if option could have multi value"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_is_multi()

    @option_type(['option', 'symlink', 'with_or_without_index'])
    def issubmulti(self, options_bag: List[OptionBag]):
        """Test if option could have submulti value"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_is_submulti()

    @option_type(['option', 'with_or_without_index'])
    def isleader(self, options_bag: List[OptionBag]):
        """Test if option is a leader"""
        return options_bag[-1].option.impl_is_leader()

    @option_type(['option', 'with_or_without_index', 'symlink'])
    def isfollower(self, options_bag: List[OptionBag]):
        """Test if option is a follower"""
        return options_bag[-1].option.impl_is_follower()

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def isdynamic(self, options_bag: List[OptionBag]):
        """Test if option is a dynamic optiondescription"""
        return options_bag[-1].option.impl_is_dynsymlinkoption()

    @option_type(['option', 'symlink', 'with_or_without_index'])
    def issymlinkoption(self, options_bag: List[OptionBag]) -> bool:
        """Test if option is a symlink option"""
        return options_bag[-1].option.impl_is_symlinkoption()

    @option_type(['option', 'with_or_without_index', 'symlink'])
    def default(self, options_bag: List[OptionBag]):
        """Get default value for an option (not for optiondescription)"""
        return options_bag[-1].option.impl_getdefault()

    @option_type(['option', 'with_or_without_index', 'symlink'])
    def defaultmulti(self, options_bag: List[OptionBag]):
        """Get default value when added a value for a multi option (not for optiondescription)"""
        if not options_bag[-1].option.impl_is_multi():
            raise ConfigError(_('only multi value has defaultmulti'))
        return options_bag[-1].option.impl_getdefault_multi()

    @option_type(['option', 'optiondescription', 'symlink', 'with_or_without_index'])
    def type(self, options_bag: List[OptionBag]):
        """Get de option type"""
        option_bag = options_bag[-1]
        if option_bag.option.impl_is_optiondescription():
            return 'optiondescription'
        return option_bag.option.get_type()

    @option_type(['option', 'with_or_without_index'])
    def pattern(self, options_bag: List[OptionBag]) -> str:
        """Get the option pattern"""
        option_bag = options_bag[-1]
        option = option_bag.option
        type = option.get_type()
        if isinstance(option, RegexpOption):
            return option._regexp.pattern
        if type == _('integer'):
            # FIXME negative too!
            return r'^[0-9]+$'
        if type == _('domain name'):
            return option.impl_get_extra('_domain_re').pattern
        if type in [_('ip'), _('network'), _('netmask')]:
            #FIXME only from 0.0.0.0 to 255.255.255.255
            return r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    @option_type(['option', 'leadership'])
    def leader(self, options_bag: List[OptionBag]):
        """Get the leader option for a follower option"""
        option = options_bag[-1].option
        leadership = options_bag[-1].option
        if not isinstance(option, Leadership):
            leadership = leadership.impl_get_leadership()
        path = leadership.get_leader().impl_getpath()
        return TiramisuOption(path,
                              None,
                              self._config_bag,
                              )

    @option_type(['option', 'with_or_without_index'])
    def index(self, options_bag: List[OptionBag]):
        """Get then index of option"""
        return options_bag[-1].index


class TiramisuOptionOption(CommonTiramisuOption):
    def __call__(self,
                 name: str,
                 index: Optional[int]=None,
                 ) -> 'TiramisuOption':
        """Select an option by path"""
        return TiramisuOption(self._path + '.' + name,
                              index,
                              self._config_bag,
                              )


class TiramisuOptionOwner(CommonTiramisuOption):
    #FIXME optiondescription must not have Owner!
    """Manage option's owner"""

    @option_type(['symlink', 'option', 'with_index'])
    def get(self, options_bag: List[OptionBag]):
        """Get owner for a specified option"""
        option_bag = options_bag[-1]
        if len(options_bag) > 1:
            parent_option_bag = options_bag[-2]
        else:
            parent_option_bag = None
        return self._config_bag.context.get_owner(option_bag)

    @option_type(['symlink', 'option', 'with_index'])
    def isdefault(self, options_bag: List[OptionBag]):
        """Is option has defaut value"""
        option_bag = options_bag[-1]
        return self._config_bag.context.get_values().is_default_owner(option_bag)

    @option_type(['option', 'with_index'])
    def set(self,
            options_bag: List[OptionBag],
            owner: str,
            ) -> None:
        """Get owner for a specified option"""
        option_bag = options_bag[-1]
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        self._config_bag.context.get_values().set_owner(option_bag,
                                                        obj_owner,
                                                        )


class TiramisuOptionProperty(CommonTiramisuOption):
    """Manage option's property"""
    _validate_properties = False

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def get(self,
            options_bag: List[OptionBag],
            only_raises=False,
            uncalculated=False,
            ):
        """Get properties for an option"""
        option_bag = options_bag[-1]
        if not only_raises:
            return option_bag.properties
        settings = self._config_bag.context.get_settings()
        ret = settings.calc_raises_properties(option_bag,
                                              uncalculated=uncalculated,
                                              )
        return ret

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def add(self,
            options_bag: List[OptionBag],
            prop,):
        """Add new property for an option"""
        option_bag = options_bag[-1]
        if prop in FORBIDDEN_SET_PROPERTIES:
            raise ConfigError(_('cannot add this property: "{0}"').format(
                ' '.join(prop)))
        settings = self._config_bag.context.get_settings()
        props = settings.get_stored_properties(option_bag.path,
                                               option_bag.index,
                                               option_bag.option.impl_getproperties(),
                                               )
        settings.setproperties(option_bag,
                               props | {prop},
                               )

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def remove(self,
               options_bag: List[OptionBag],
               prop,
               ):
        """Remove new property for an option"""
        option_bag = options_bag[-1]
        props = option_bag.properties
        self._config_bag.context.get_settings().setproperties(option_bag,
                                                              props - {prop},
                                                              )

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def reset(self, options_bag: List[OptionBag]):
        """Reset all personalised properties"""
        option_bag = options_bag[-1]
        self._config_bag.context.get_settings().reset(option_bag)


class TiramisuOptionPermissive(CommonTiramisuOption):
    """Manage option's permissive"""

    @option_type(['option', 'optiondescription', 'symlink', 'with_or_without_index'])
    def get(self, options_bag: List[OptionBag]):
        """Get permissives value"""
        return self._config_bag.context.get_settings().getpermissives(options_bag[-1])

    @option_type(['option', 'optiondescription', 'with_or_without_index'])
    def set(self,
            options_bag: List[OptionBag],
            permissives,
            ):
        """Set permissives value"""
        option_bag = options_bag[-1]
        self._config_bag.context.get_settings().setpermissives(option_bag,
                                                               permissives=permissives,
                                                               )

    @option_type(['option', 'optiondescription', 'with_index'])
    def reset(self, options_bag: List[OptionBag]):
        """Reset all personalised permissive"""
        option_bag = options_bag[-1]
        self._config_bag.context.get_settings().reset_permissives(option_bag)


class TiramisuOptionInformation(CommonTiramisuOption):
    """Manage option's informations"""

    @option_type(['option', 'optiondescription', 'with_or_without_index', 'symlink'])
    def get(self,
            options_bag: List[OptionBag],
            name: str,
            default=undefined,
            ) -> Any:
        """Get information"""
        option_bag = options_bag[-1]
        try:
            return self._config_bag.context.get_values().get_information(option_bag,
                                                                         name,
                                                                         undefined,
                                                                         )
        except ValueError:
            return option_bag.option.impl_get_information(name, default)

    @option_type(['option', 'optiondescription'])
    def set(self,
            options_bag: List[OptionBag],
            key: str,
            value: Any) -> None:
        """Set information"""
        option_bag = options_bag[-1]
        self._config_bag.context.get_values().set_information(option_bag,
                                                              key,
                                                              value,
                                                              )

    @option_type(['option', 'optiondescription'])
    def reset(self,
              options_bag: List[OptionBag],
              key: str,
              ) -> None:
        """Remove information"""
        option_bag = options_bag[-1]
        self._config_bag.context.get_values().del_information(key,
                                                              path=option_bag.path,
                                                              )

    @option_type(['option', 'optiondescription', 'with_or_without_index', 'symlink'])
    def list(self,
             options_bag: List[OptionBag],
             ) -> list:
        """List information's keys"""
        option_bag = options_bag[-1]
        lst1 = set(option_bag.option.impl_list_information())
        lst2 = set(self._config_bag.context.get_values().list_information(option_bag.path))
        return lst1 | lst2


class TiramisuOptionValue(CommonTiramisuOption):
    """Manage option's value"""
    _validate_properties = True

    @option_type('optiondescription')
    def dict(self, options_bag: List[OptionBag]):
        """Obsolete: dict with path as key and value"""
        return self._config_bag.context.make_dict(options_bag[-1])

    @option_type(['option', 'symlink', 'with_index', 'optiondescription'])
    def get(self,
            options_bag: List[OptionBag],
            ):
        """Get value"""
        if options_bag[-1].option.impl_is_optiondescription():
            return self._config_bag.context.make_dict(options_bag[-1])
        return self._get(options_bag)

    def _get(self,
             options_bag: OptionBag,
             ):
        """Get option's value"""
        option_bag = options_bag[-1]
        if len(options_bag) > 1:
            parent_option_bag = options_bag[-2]
        else:
            parent_option_bag = None
        return self._config_bag.context.get_value(option_bag,
                                                  parent_option_bag,
                                                  )

    @option_type(['option', 'with_index'])
    def set(self,
            options_bag: List[OptionBag],
            value,
            ):
        """Change option's value"""
        option_bag = options_bag[-1]
        values = option_bag.config_bag.context.get_values()
        if not isinstance(value, Calculation) and option_bag.option.impl_is_leader() and \
                len(value) < self._config_bag.context.get_length_leadership(options_bag[-2]):
            raise LeadershipError(_('cannot reduce length of the leader "{}"'
                                    '').format(option_bag.option.impl_get_display_name()))
        return option_bag.config_bag.context.set_value(option_bag,
                                                       value,
                                                       )

    @option_type(['group', 'option', 'with_index'])
    def reset(self,
              options_bag: List[OptionBag],
              is_group: bool=False,
              ) -> None:
        """Reset value for an option"""
        option_bag = options_bag[-1]
        if is_group:
            self._config_bag.context.reset(option_bag.path,
                                           self._config_bag,
                                           )
        else:
            values = self._config_bag.context.get_values()
            if option_bag.index is not None:
                values.reset_follower(option_bag)
            else:
                values.reset(option_bag)

    @option_type(['option', 'with_index', 'symlink'])
    def default(self, options_bag: List[OptionBag]):
        """Get default value (default of option or calculated value)"""
        return self._config_bag.context.get_values().get_default_value(options_bag[-1])

    @option_type(['option', 'with_index'])
    def valid(self, options_bag: List[OptionBag]):
        """The if the option's value is valid"""
        option_bag = options_bag[-1]
        try:
            with catch_warnings(record=True) as warns:
                simplefilter("always", ValueErrorWarning)
                self._get(options_bag)
                for warn in warns:
                    if isinstance(warn.message, ValueErrorWarning):
                        return False
        except ValueError:
            return False
        return True

    @option_type(['choice', 'with_or_without_index'])
    def list(self, options_bag: List[OptionBag]):
        """All values available for a ChoiceOption"""
        option_bag = options_bag[-1]
        return option_bag.option.impl_get_values(option_bag)

    @option_type('leader')
    def pop(self,
            options_bag: List[OptionBag],
            index: int,
            ):
        """Pop a value"""
        self._config_bag.context.get_values().reset_leadership(options_bag[-1],
                                                               options_bag[-2],
                                                               index,
                                                               )

    @option_type(['leader', 'follower', 'with_or_without_index'])
    def len(self, options_bag: List[OptionBag]):
        """Length for a follower option"""
        return self._config_bag.context.get_length_leadership(options_bag[-2])


def _registers(_registers: Dict[str, type],
               prefix: str,
               ):
    for module_name in globals().keys():
        if module_name != prefix and module_name.startswith(prefix):
            module = globals()[module_name]
            func_name = module_name[len(prefix):].lower()
            _registers[func_name] = module
#__________________________________________________________________________________________________
#


class TiramisuConfig(TiramisuHelp, _TiramisuOptionWalk):
    def __init__(self,
            config_bag: ConfigBag,
            orig_config_bags: Optional[List[OptionBag]],
            ) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags

    def _return_config(self, config):
        if isinstance(config, KernelConfig):
            return Config(config)
        if isinstance(config, KernelMetaConfig):
            return MetaConfig(config)
        if isinstance(config, KernelMixConfig):
            return MixConfig([], config)
        if isinstance(config, KernelGroupConfig):
            return GroupConfig(config)

    def _reset_config_properties(self):
        config = self._config_bag.context
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        permissives = settings.get_context_permissives()
        self._config_bag.properties = properties
        self._config_bag.permissives = permissives
        if self._orig_config_bags:
            for config_bag in self._orig_config_bags:
                config_bag.properties = properties
                config_bag.permissives = permissives

    def name(self):
        """get the name"""
        return self._config_bag.context.impl_getname()


class TiramisuOption(CommonTiramisu, _TiramisuOptionOption, TiramisuConfig):
    """Manage selected option"""
    _validate_properties = False
    _registers = {}
    def __init__(self,
                 path: Optional[str]=None,
                 index: Optional[int]=None,
                 config_bag: Optional[ConfigBag]=None,
                 ) -> None:
        self._path = path
        self._index = index
        self._config_bag = config_bag
        self._tiramisu_dict = None
        if not self._registers:
            _registers(self._registers, 'TiramisuOption')

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc in self._registers:
            return self._registers[subfunc](self._path,
                                            self._index,
                                            self._config_bag,
                                            )
        raise ConfigError(_(f'please specify a valid sub function ({self.__class__.__name__}.{subfunc})'))

    @option_type('optiondescription')
    def find(self,
             options_bag: List[OptionBag],
             name: str,
             value=undefined,
             type=None,
             first: bool=False):
        """Find an option by name (only for optiondescription)"""
        option_bag = options_bag[-1]
        if not first:
            ret = []
        for path in self._config_bag.context.find(option_bag=option_bag,
                                                  byname=name,
                                                  byvalue=value,
                                                  bytype=type,
                                                  ):
            t_option = TiramisuOption(path,
                                      None,  # index for a follower ?
                                      self._config_bag,
                                      )
            if first:
                return t_option
            ret.append(t_option)
        return ret

    @option_type('optiondescription')
    def group_type(self, options_bag: List[OptionBag]):
        """Get type for an optiondescription (only for optiondescription)"""
        return options_bag[-1].option.impl_get_group_type()

    @option_type('optiondescription')
    def list(self,
             options_bag: List[OptionBag],
             type='option',
             recursive=False,
             group_type=None,
             ):
        """List options inside an option description (by default list only option)"""
        return self._list(options_bag[-1],
                          type,
                          group_type,
                          recursive,
                          )

    def _load_dict(self,
                   clearable: str="all",
                   remotable: str="minimum",
                   ):
        config = self._config_bag.context
        self._tiramisu_dict = TiramisuDict(self._return_config(config),
                                           root=self._path,
                                           clearable=clearable,
                                           remotable=remotable)

    @option_type('optiondescription')
    def dict(self,
             options_bag: List[OptionBag],
             clearable: str="all",
             remotable: str="minimum",
             form: List=[],
             force: bool=False,
             ) -> Dict:
        """Convert config and option to tiramisu format"""
        if force or self._tiramisu_dict is None:
            self._load_dict(clearable, remotable)
        return self._tiramisu_dict.todict(form)

    @option_type('optiondescription')
    def updates(self,
                options_bag: List[OptionBag],
                body: List,
                ) -> Dict:
        """Updates value with tiramisu format"""
        if self._tiramisu_dict is None:  # pragma: no cover
            self._load_dict()
        return self._tiramisu_dict.set_updates(body)


class TiramisuContextInformation(TiramisuConfig):
    """Manage config informations"""
    def get(self,
            name,
            default=undefined,
            ):
        """Get an information"""
        values = self._config_bag.context.get_values()
        try:
            return values.get_information(None,
                                          name,
                                          undefined,
                                          )
        except ValueError:
            return self._config_bag.context.get_description().impl_get_information(name, default)

    def set(self,
            name,
            value,
            ):
        """Set an information"""
        self._config_bag.context.impl_set_information(self._config_bag,
                                                      name,
                                                      value,
                                                      )

    def reset(self,
              name,
              ):
        """Remove an information"""
        self._config_bag.context.impl_del_information(name)

    def list(self):
        """List information's keys"""
        lst1 = set(self._config_bag.context.get_description().impl_list_information())
        lst2 = set(self._config_bag.context.impl_list_information())
        return lst1 | lst2

    def exportation(self):
        """Export all informations"""
        return deepcopy(self._config_bag.context.get_values()._informations)

    def importation(self, informations):
        """Import informations"""
        self._config_bag.context.get_values()._informations = deepcopy(informations)


class TiramisuContextValue(TiramisuConfig):
    """Manage config value"""
    def mandatory(self):
        """Return path of options with mandatory property without any value"""
        config_bag = self._config_bag.copy()
        config_bag.properties -= {'mandatory', 'empty', 'warnings'}
        config_bag.set_permissive()
        root_option_bag = OptionBag(self._config_bag.context.get_description(),
                                    None,
                                    config_bag,
                                    )
        options = []
        for option_bag in self._config_bag.context.walk(root_option_bag,
                                                        recursive=True,
                                                        types=['mandatory'],
                                                        ):
            options.append(TiramisuOption(option_bag.path,
                                          option_bag.index,
                                          self._config_bag,
                                          ))
        return options

    # FIXME should be only for group/meta
    def set(self,
            path: str,
            value: Any,
            only_config=undefined,
            force_default=undefined,
            force_default_if_same=undefined,
            force_dont_change_value=undefined,
            ):
        """Set a value in config or children for a path"""
        kwargs = {}
        if only_config is not undefined:
            kwargs['only_config'] = only_config
        if force_default is not undefined:
            kwargs['force_default'] = force_default
        if force_default_if_same is not undefined:
            kwargs['force_default_if_same'] = force_default_if_same
        if force_dont_change_value is not undefined:
            kwargs['force_dont_change_value'] = force_dont_change_value
        option_bag = OptionBag(None,
                               None,
                               self._config_bag,
                               path=path,
                               )
        return self._config_bag.context.set_value(option_bag,
                                                  value,
                                                  **kwargs,
                                                  )

    # FIXME should be only for group/meta
    def reset(self,
              path: str,
              only_children: bool=False):
        """Reset value"""
        self._config_bag.context.reset(path,
                                       only_children,
                                       self._config_bag,
                                       )

    def dict(self):
        """Obsolete: dict with path as key and value"""
        option_bag = OptionBag(self._config_bag.context.get_description(),
                               None,
                               self._config_bag,
                               )
        return self._config_bag.context.make_dict(option_bag)

    def get(self):
        """Dict with path as key and value"""
        option_bag = OptionBag(self._config_bag.context.get_description(),
                               None,
                               self._config_bag,
                               )
        return self._config_bag.context.make_dict(option_bag)

    def exportation(self,
                    with_default_owner: bool=False,
                    ):
        """Export all values"""
        exportation = deepcopy(self._config_bag.context.get_values()._values)
        if not with_default_owner:
            del exportation[None]
        return exportation

    def importation(self, values):
        """Import values"""
        cvalues = self._config_bag.context.get_values()
        if None not in values:
            current_owner = cvalues.get_context_owner()
        cvalues._values = deepcopy(values)
        self._config_bag.context.reset_cache(None, None)
        if None not in values:
            cvalues._values[None] = {None: [None, current_owner]}


class TiramisuContextOwner(TiramisuConfig):
    """Global owner"""
    def get(self):
        """Get owner"""
        return self._config_bag.context.get_values().get_context_owner()

    def set(self, owner):
        """Set owner"""
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        values = self._config_bag.context.get_values()
        values.set_context_owner(obj_owner)


class TiramisuContextProperty(TiramisuConfig):
    """Manage config properties"""
    def read_only(self):
        """Set config to read only mode"""
        old_props = self._config_bag.properties
        settings = self._config_bag.context.get_settings()
        settings.read_only(self._config_bag)
        self._reset_config_properties()
        if 'force_store_value' not in old_props and \
                'force_store_value' in self._config_bag.properties:
            self._force_store_value()

    def read_write(self):
        """Set config to read and write mode"""
        old_props = self._config_bag.properties
        settings = self._config_bag.context.get_settings()
        settings.read_write(self._config_bag)
        or_properties = settings.rw_append - settings.ro_append - SPECIAL_PROPERTIES
        permissives = frozenset(settings.get_context_permissives() | or_properties)
        settings.set_context_permissives(permissives)
        self._reset_config_properties()
        if 'force_store_value' not in old_props and \
                'force_store_value' in self._config_bag.properties:
            self._force_store_value()

    def add(self, prop):
        """Add a config property"""
        props = set(self.get())
        if prop not in props:
            props.add(prop)
            self._set(frozenset(props))

    def remove(self, prop):
        """Remove a config property"""
        props = set(self.get())
        if prop in props:
            props.remove(prop)
            self._set(frozenset(props))

    def get(self):
        """Get all config properties"""
        return self._config_bag.properties

    def _set(self,
             props,
             ):
        """Personalise config properties"""
        if 'force_store_value' in props:
            force_store_value = 'force_store_value' not in self._config_bag.properties
        else:
            force_store_value = False
        context = self._config_bag.context
        context.get_settings().set_context_properties(props,
                                                      self._config_bag.context,
                                                      )
        self._reset_config_properties()
        if force_store_value:
            self._force_store_value()

    def reset(self):
        """Remove config properties"""
        context = self._config_bag.context
        context.get_settings().reset(self._config_bag)
        self._reset_config_properties()

    def exportation(self):
        """Export config properties"""
        return deepcopy(self._config_bag.context.get_settings()._properties)

    def importation(self, properties):
        """Import config properties"""
        if 'force_store_value' in properties.get(None, {}).get(None, []):
            force_store_value = 'force_store_value' not in self._config_bag.properties
        else:
            force_store_value = False
        self._config_bag.context.get_settings()._properties = deepcopy(properties)
        self._config_bag.context.reset_cache(None, None)
        self._reset_config_properties()
        if force_store_value:
            self._force_store_value()

    def _force_store_value(self):
        descr = self._config_bag.context.get_description()
        descr.impl_build_force_store_values(self._config_bag)

    def setdefault(self,
                   properties: Set[str],
                   type: Optional[str]=None,
                   when: Optional[str]=None) -> None:
        if not isinstance(properties, frozenset):
            raise TypeError(_('properties must be a frozenset'))
        setting = self._config_bag.context.get_settings()
        if type is None and when is None:
            setting.default_properties = properties
        else:
            if when not in ['append', 'remove']:
                raise ValueError(_('unknown when {} (must be in append or remove)').format(when))
            if type == 'read_only':
                if when == 'append':
                    setting.ro_append = properties
                else:
                    setting.ro_remove = properties
            elif type == 'read_write':
                if when == 'append':
                    setting.rw_append = properties
                else:
                    setting.rw_remove = properties
            else:
                raise ValueError(_('unknown type {}').format(type))

    def default(self,
                type: Optional[str]=None,
                when: Optional[str]=None,
                ) -> Set[str]:
        setting = self._config_bag.context.get_settings()
        if type is None and when is None:
            return setting.default_properties
        if type == 'current':
            return setting.get_context_properties(self._config_bag.context.properties_cache)
        if when not in ['append', 'remove']:
            raise ValueError(_('unknown when {} (must be in append or remove)').format(when))
        if type == 'read_only':
            if when == 'append':
                return setting.ro_append
            return setting.ro_remove
        if type == 'read_write':
            if when == 'append':
                return setting.rw_append
            return setting.rw_remove
        raise ValueError(_('unknown type {}').format(type))


class TiramisuContextPermissive(TiramisuConfig):
    """Manage config permissives"""
    def get(self):
        """Get config permissives"""
        return self._get()

    def _get(self):
        return self._config_bag.context.get_settings().get_context_permissives()

    def _set(self,
             permissives,
             ):
        """Set config permissives"""
        self._config_bag.context.get_settings().set_context_permissives(permissives)
        self._reset_config_properties()

    def exportation(self):
        """Export config permissives"""
        return deepcopy(self._config_bag.context.get_settings()._permissives)

    def importation(self, permissives):
        """Import config permissives"""
        settings = self._config_bag.context.get_settings()
        self._config_bag.context.get_settings()._permissives = deepcopy(permissives)
        self._config_bag.context.reset_cache(None,
                                             None,
                                             )
        self._reset_config_properties()

    def reset(self):
        """Remove config permissives"""
        context = self._config_bag.context
        settings = context.get_settings()
        settings.reset_permissives(self._config_bag)
        self._reset_config_properties()

    def add(self, prop):
        """Add a config permissive"""
        props = set(self._get())
        props.add(prop)
        self._set(frozenset(props))

    def remove(self, prop):
        """Remove a config permissive"""
        props = set(self._get())
        if prop in props:
            props.remove(prop)
            self._set(frozenset(props))


class TiramisuContextOption(TiramisuConfig, _TiramisuOptionWalk):
    def __init__(self,
                 *args,
                 **kwargs) -> None:
        self._tiramisu_dict = None
        super().__init__(*args, **kwargs)

    def find(self,
             name,
             value=undefined,
             type=None,
             first=False):
        """Find an or a list of options"""
        options = []
        option_bag = OptionBag(self._config_bag.context.get_description(),
                               None,
                               self._config_bag,
                               )
        for path in self._config_bag.context.find(option_bag,
                                                  byname=name,
                                                  byvalue=value,
                                                  bytype=type,
                                                  ):
            option = TiramisuOption(path,
                                    None,
                                    self._config_bag,
                                    )
            if first:
                return option
            options.append(option)
        return options

    def list(self,
             type='option',
             group_type=None,
             recursive=False,
             ):
        """List options (by default list only option)"""
        root_option_bag = OptionBag(self._config_bag.context.get_description(),
                                    None,
                                    self._config_bag,
                                    )
        return self._list(root_option_bag,
                          type,
                          group_type,
                          recursive,
                          )

    def _load_dict(self,
                   clearable="all",
                   remotable="minimum"):
        self._tiramisu_dict = TiramisuDict(self._return_config(self._config_bag.context),
                                           root=None,
                                           clearable=clearable,
                                           remotable=remotable,
                                           )

    def dict(self,
             clearable="all",
             remotable="minimum",
             form=None,
             force=False,
             ):
        """Convert config and option to tiramisu format"""
        if form is None:
            form = []
        if force or self._tiramisu_dict is None:
            self._load_dict(clearable, remotable)
        return self._tiramisu_dict.todict(form)

    def updates(self,
                body: List) -> Dict:
        """Updates value with tiramisu format"""
        if self._tiramisu_dict is None:  # pragma: no cover
            self._load_dict()
        return self._tiramisu_dict.set_updates(body)


class _TiramisuContextConfigReset():
    def reset(self):
        """Remove all datas to current config (informations, values, properties, ...)"""
        # Option's values
        context_owner = self._config_bag.context.get_values().get_context_owner()
        self._config_bag.context.get_values()._values = {None: {None: [None, context_owner]}}
        # Option's informations
        self._config_bag.context.get_values()._informations = {}
        # Option's properties
        self._config_bag.context.get_settings()._properties = {}
        # Option's permissives
        self._config_bag.context.get_settings()._permissives = {}
        # Remove cache
        self._config_bag.context.reset_cache(None, None)


class _TiramisuContextConfig(TiramisuConfig, _TiramisuContextConfigReset):
    """Actions to Config"""
    def type(self):
        """Type a Config"""
        return 'config'

    def copy(self, name=None):
        """Copy current config"""
        config = self._config_bag.context.duplicate(name=name)
        return self._return_config(config)

    def deepcopy(self, metaconfig_prefix=None, name=None):
        """Copy current config with all parents"""
        config = self._config_bag.context.duplicate(metaconfig_prefix=metaconfig_prefix,
                                                    deep=[],
                                                    name=name,
                                                    )
        return self._return_config(config)

    def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(self._return_config(parent))
        return ret

    def path(self):
        """Get path from config (all parents name)"""
        return self._config_bag.context.get_config_path()


class _TiramisuContextGroupConfig(TiramisuConfig):
    """Actions to GroupConfig"""
    def type(self):
        """Type a Config"""
        return 'groupconfig'

    def list(self):
        """List children's config"""
        ret = []
        for child in self._config_bag.context.get_children():
            ret.append(self._return_config(child))
        return ret

    def find(self,
             name: str,
             value=undefined,
             ):
        """Find an or a list of config with finding option"""
        return GroupConfig(self._config_bag.context.find_group(byname=name,
                                                               byvalue=value,
                                                               config_bag=self._config_bag,
                                                               ))

    def __call__(self,
                 path: Optional[str]):
        """Select a child Tiramisu config"""
        spaths = path.split('.')
        config = self._config_bag.context
        for spath in spaths:
            config = config.getconfig(spath)
        if isinstance(config, KernelGroupConfig):
            return self._return_config(config)
        return self._return_config(config)


    def copy(self, name=None):
        config = self._config_bag.context.duplicate(name=name)
        return self._return_config(config)

    def deepcopy(self, name=None, metaconfig_prefix=None):
        config = self._config_bag.context.duplicate(metaconfig_prefix=metaconfig_prefix,
                                                    deep=[],
                                                    name=name,
                                                    )
        return self._return_config(config)

    def path(self):
        return self._config_bag.context.get_config_path()


class _TiramisuContextMixConfig(_TiramisuContextGroupConfig, _TiramisuContextConfigReset):
    """Actions to MixConfig"""
    def type(self):
        """Type a Config"""
        return 'mixconfig'

    def new(self, name=None, type='config'):
        """Create and add a new config"""
        config = self._config_bag.context
        new_config = config.new_config(type_=type, name=name)
        return self._return_config(new_config)

    def remove(self, name):
        """Remove config from MetaConfig"""
        config = self._config_bag.context.remove_config(name)
        return self._return_config(config)

    def add(self,
            config):
        """Add config from MetaConfig"""
        # pylint: disable=protected-access
        self._config_bag.context.add_config(config._config_bag.context)

    def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(self._return_config(parent))
        return ret


class _TiramisuContextMetaConfig(_TiramisuContextMixConfig):
    """Actions to MetaConfig"""
    def type(self):
        """Type a Config"""
        return 'metaconfig'


class TiramisuContextCache(TiramisuConfig):
    """Manage config cache"""

    def reset(self):
        """Reset cache"""
        self._config_bag.context.reset_cache(None, None)

    def set_expiration_time(self,
                            time: int,
                            ) -> None:
        """Change expiration time value"""
        self._config_bag.expiration_time = time

    def get_expiration_time(self) -> int:
        """Get expiration time value"""
        return self._config_bag.expiration_time


class TiramisuAPI(TiramisuHelp):
    """TiramisuAPI common class
    """
    _registers = {}

    def __init__(self,
                 config_bag,
                 orig_config_bags=None) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags
        if not self._registers:
            _registers(self._registers, 'TiramisuContext')

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc == 'option':
            config_bag = self._config_bag
            return TiramisuDispatcherOption(config_bag,
                                            self._orig_config_bags,
                                            )
        if subfunc in ['forcepermissive', 'unrestraint', 'nowarnings']:
            if self._orig_config_bags:
                msg = _('do not use unrestraint, nowarnings or forcepermissive together')
                raise ConfigError(msg)
            config_bag = self._config_bag.copy()
            if subfunc == 'unrestraint':
                config_bag.unrestraint()
            elif subfunc == 'nowarnings':
                config_bag.nowarnings()
            else:
                config_bag.set_permissive()
            return TiramisuAPI(config_bag, [self._config_bag])
        if subfunc == 'config':
            config_type = self._config_bag.context.impl_type
            if config_type == 'group':
                config = _TiramisuContextGroupConfig
            elif config_type == 'meta':
                config = _TiramisuContextMetaConfig
            elif config_type == 'mix':
                config = _TiramisuContextMixConfig
            else:
                config = _TiramisuContextConfig
            return config(self._config_bag,
                          self._orig_config_bags)
        if subfunc in self._registers:
            config_bag = self._config_bag
            # del config_bag.permissives
            return self._registers[subfunc](config_bag,
                                            self._orig_config_bags)
        raise ConfigError(_(f'please specify a valid sub function ({self.__class__.__name__}.{subfunc})'))

    def __dir__(self):
        return list(self._registers.keys()) + \
                ['unrestraint', 'forcepermissive', 'nowarnings', 'config']


class TiramisuDispatcherOption(TiramisuContextOption):
    """Select an option"""
    def __call__(self,
                 path: str,
                 index: Optional[int]=None,
                 ) -> TiramisuOption:
        """Select an option by path"""
        return TiramisuOption(path,
                              index,
                              self._config_bag,
                              )


class Config(TiramisuAPI):
    """Root config object that enables us to handle the configuration options"""
    def __init__(self,
                 descr: OptionDescription,
                 name=None,
                 display_name=None,
                 ) -> None:
        if isinstance(descr, KernelConfig):
            config = descr
        else:
            config = KernelConfig(descr,
                                  name=name,
                                  display_name=display_name,
                                  )
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives,
                               )
        super().__init__(config_bag)

    def __del__(self):
        try:
            del self._config_bag.context
            del self._config_bag
            del self._orig_config_bags
        except ConfigError:
            pass


class MetaConfig(TiramisuAPI):
    """MetaConfig object that enables us to handle the sub configuration's options
    with common root optiondescription
    """
    # pylint: disable=too-few-public-methods
    def __init__(self,
                 children: 'Config'=None,
                 name=None,
                 optiondescription: Optional[OptionDescription]=None,
                 display_name=None
                 ) -> None:
        if children is None:
            children = []
        if isinstance(children, KernelMetaConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelMetaConfig(_children,
                                      optiondescription=optiondescription,
                                      name=name,
                                      display_name=display_name,
                                      )
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives)
        super().__init__(config_bag)


class MixConfig(TiramisuAPI):
    """MixConfig object that enables us to handle the sub configuration's options
    with differents root optiondescription
    """
    # pylint: disable=too-few-public-methods
    def __init__(self,
                 optiondescription: OptionDescription,
                 children: List[Config],
                 name: Callable=None,
                 display_name=None
                 ) -> None:
        if isinstance(children, KernelMixConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelMixConfig(optiondescription,
                                     _children,
                                     name=name,
                                     display_name=display_name,
                                     )
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(config,
                               properties=properties,
                               permissives=permissives,
                               )
        super().__init__(config_bag)


class GroupConfig(TiramisuAPI):
    """GroupConfig that enables us to access the sub configuration's options"""
    # pylint: disable=too-few-public-methods
    def __init__(self,
                 children,
                 name=None,
                 ) -> None:
        if isinstance(children, KernelGroupConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelGroupConfig(_children, name=name)
        config_bag = ConfigBag(config,
                               properties=None,
                               permissives=None)
        super().__init__(config_bag)
