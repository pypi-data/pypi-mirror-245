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
# the rough gus of pypy: pypy: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"enables us to carry out a calculation and return an option's value"
from typing import Any, Optional, Union, Callable, Dict, List
from itertools import chain

from .error import PropertiesOptionError, ConfigError, LeadershipError, ValueWarning
from .i18n import _
from .setting import undefined, ConfigBag, OptionBag, Undefined
from .function import FUNCTION_WAITING_FOR_DICT
# ____________________________________________________________


class Params:
    __slots__ = ('args', 'kwargs')
    def __init__(self, args=None, kwargs=None, **kwgs):
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}
        if kwgs:
            kwargs.update(kwgs)
        if isinstance(args, Param):
            args = (args,)
        else:
            if not isinstance(args, tuple):
                raise ValueError(_('args in params must be a tuple'))
            for arg in args:
                if not isinstance(arg, Param):
                    raise ValueError(_('arg in params must be a Param'))
        if not isinstance(kwargs, dict):
            raise ValueError(_('kwargs in params must be a dict'))
        for arg in kwargs.values():
            if not isinstance(arg, Param):
                raise ValueError(_('arg in params must be a Param'))
        self.args = args
        self.kwargs = kwargs


class Param:
    pass


class ParamOption(Param):
    __slots__ = ('option',
                 'notraisepropertyerror',
                 'raisepropertyerror',
                 )
    def __init__(self,
                 option: 'Option',
                 notraisepropertyerror: bool=False,
                 raisepropertyerror: bool=False,
                 ) -> None:
        if __debug__ and not hasattr(option, 'impl_is_symlinkoption'):
            raise ValueError(_('paramoption needs an option not {}').format(type(option)))
        if option.impl_is_symlinkoption():
            cur_opt = option.impl_getopt()
        else:
            cur_opt = option
        assert isinstance(notraisepropertyerror, bool), _('param must have a boolean not a {} for notraisepropertyerror').format(type(notraisepropertyerror))
        assert isinstance(raisepropertyerror, bool), _('param must have a boolean not a {} for raisepropertyerror').format(type(raisepropertyerror))
        self.option = cur_opt
        self.notraisepropertyerror = notraisepropertyerror
        self.raisepropertyerror = raisepropertyerror


class ParamDynOption(ParamOption):
    __slots__ = ('subpath',)
    def __init__(self,
                 option: 'Option',
                 subpath: str,
                 dynoptiondescription: 'DynOptionDescription',
                 notraisepropertyerror: bool=False,
                 raisepropertyerror: bool=False,
                 optional: bool=False,
                 ) -> None:
        super().__init__(option,
                         notraisepropertyerror,
                         raisepropertyerror,
                         )
        self.subpath = subpath
        self.dynoptiondescription = dynoptiondescription
        self.optional = optional


class ParamSelfOption(Param):
    __slots__ = ('whole')
    def __init__(self,
                 whole: bool=undefined,
                 ) -> None:
        """whole: send all value for a multi, not only indexed value"""
        if whole is not undefined:
            self.whole = whole


class ParamValue(Param):
    __slots__ = ('value',)
    def __init__(self, value):
        self.value = value


class ParamInformation(Param):
    __slots__ = ('information_name',
                 'default_value',
                 'option',
                 )
    def __init__(self,
                 information_name: str,
                 default_value: Any=undefined,
                 option: 'Option'=None
                 ) -> None:
        self.information_name = information_name
        self.default_value = default_value
        if option:
            if option.impl_is_symlinkoption():
                raise ValueError(_('option in ParamInformation cannot be a symlinkoption'))
            if option.impl_is_follower():
                raise ValueError(_('option in ParamInformation cannot be a follower'))
            if option.impl_is_dynsymlinkoption():
                raise ValueError(_('option in ParamInformation cannot be a dynamic option'))
        self.option = option


class ParamSelfInformation(ParamInformation):
    __slots__ = tuple()


class ParamIndex(Param):
    __slots__ = tuple()


class ParamSuffix(Param):
    __slots__ = tuple()


class Calculation:
    __slots__ = ('function',
                 'params',
                 'help_function',
                 '_has_index',
                 'warnings_only',
                 )
    def __init__(self,
                 function: Callable,
                 params: Params=Params(),
                 help_function: Optional[Callable]=None,
                 warnings_only: bool=False,
                 ):
        assert isinstance(function, Callable), _('first argument ({0}) must be a function').format(function)
        if help_function:
            assert isinstance(help_function, Callable), _('help_function ({0}) must be a function').format(help_function)
            self.help_function = help_function
        else:
            self.help_function = None
        self.function = function
        self.params = params
        for arg in chain(self.params.args, self.params.kwargs.values()):
            if isinstance(arg, ParamIndex):
                self._has_index = True
                break
        if warnings_only is True:
            self.warnings_only = warnings_only

    def execute(self,
                option_bag: OptionBag,
                orig_value: Any=undefined,
                allow_value_error: bool=False,
                force_value_warning: bool=False,
                for_settings: bool=False,
                ) -> Any:
        return carry_out_calculation(option_bag.option,
                                     callback=self.function,
                                     callback_params=self.params,
                                     index=option_bag.index,
                                     config_bag=option_bag.config_bag,
                                     orig_value=orig_value,
                                     allow_value_error=allow_value_error,
                                     force_value_warning=force_value_warning,
                                     for_settings=for_settings,
                                     )

    def help(self,
             option_bag: OptionBag,
             for_settings: bool=False,
             ) -> str:
        if not self.help_function:
            return self.execute(option_bag,
                                for_settings=for_settings,
                                )
        return carry_out_calculation(option_bag.option,
                                     callback=self.help_function,
                                     callback_params=self.params,
                                     index=option_bag.index,
                                     config_bag=option_bag.config_bag,
                                     for_settings=for_settings,
                                     )

    def __deepcopy__(x, memo):
        return x


def manager_callback(callback: Callable,
                     param: Param,
                     option,
                     index: Optional[int],
                     orig_value,
                     config_bag: ConfigBag,
                     for_settings: bool,
                     ) -> Any:
    """replace Param by true value"""
    def calc_index(param, index, same_leadership):
        if index is not None:
            if hasattr(param, 'whole'):
                whole = param.whole
            else:
                # if value is same_leadership, follower are isolate by default
                # otherwise option is a whole option
                whole = not same_leadership
            if not whole:
                return index
        return None

    def calc_self(param,
                  option,
                  index,
                  value,
                  config_bag,
                  ):
        # index must be apply only if follower
        is_follower = option.impl_is_follower()
        apply_index = calc_index(param, index, is_follower)
        if value is undefined or (apply_index is None and is_follower):
            path = option.impl_getpath()
            option_bag = OptionBag(option,
                                   None,
                                   config_bag,
                                   properties=None,
                                   )
            properties = config_bag.context.get_settings().getproperties(option_bag,
                                                                         uncalculated=True,
                                                                         )
            new_value = get_value(config_bag,
                                  option,
                                  param,
                                  apply_index,
                                  True,
                                  properties,
                                  )
            if apply_index is None and is_follower:
                new_value[index] = value
            value = new_value
        elif apply_index is not None and not is_follower:
            value = value[apply_index]
        return value

    def get_value(config_bag,
                  option,
                  param,
                  index,
                  self_calc,
                  properties=undefined,
                  ):
        parent_option_bag, option_bag = get_option_bag(config_bag,
                                                       option,
                                                       param,
                                                       index,
                                                       self_calc,
                                                       properties=properties,
                                                       )
        if option.impl_is_follower() and index is None:
            value = []
            for idx in range(config_bag.context.get_length_leadership(parent_option_bag)):
                parent_option_bag, option_bag = get_option_bag(config_bag,
                                                               option,
                                                               param,
                                                               idx,
                                                               self_calc,
                                                               properties=properties,
                                                               )
                value.append(_get_value(param,
                                        option_bag,
                                        ))
        else:
            value = _get_value(param,
                               option_bag,
                               )
        return value

    def _get_value(param: Params,
                   option_bag: OptionBag,
                   ) -> Any:
        try:
            # get value
            value = config_bag.context.get_value(option_bag)
        except PropertiesOptionError as err:
            # raise PropertiesOptionError (which is catched) because must not add value None in carry_out_calculation
            if param.notraisepropertyerror or param.raisepropertyerror:
                raise err from err
            raise ConfigError(_('unable to carry out a calculation for "{}"'
                                ', {}').format(option.impl_get_display_name(), err), err) from err
        except ValueError as err:
            raise ValueError(_('the option "{0}" is used in a calculation but is invalid ({1})').format(option_bag.option.impl_get_display_name(), err)) from err
        except AttributeError as err:
            if isinstance(param, ParamDynOption) and param.optional:
                # cannot acces, simulate a propertyerror
                raise PropertiesOptionError(option_bag,
                                            ['configerror'],
                                            config_bag.context.get_settings(),
                                            )
            raise ConfigError(_(f'unable to get value for calculating "{option_bag.option.impl_get_display_name()}", {err}')) from err
        return value

    def get_option_bag(config_bag,
                       opt,
                       param,
                       index_,
                       self_calc,
                       properties=undefined,
                       ):
        # don't validate if option is option that we tried to validate
        config_bag = config_bag.copy()
        if for_settings:
            config_bag.properties = config_bag.true_properties - {'warnings'}
        config_bag.set_permissive()
        if not for_settings:
            config_bag.properties -= {'warnings'}
        if self_calc:
            config_bag.unrestraint()
            config_bag.remove_validation()
        root_option_bag = OptionBag(config_bag.context.get_description(),
                                    None,
                                    config_bag,
                                    )
        try:
            options_bag = config_bag.context.get_sub_option_bag(root_option_bag,
                                                                opt.impl_getpath(),
                                                                index_,
                                                                validate_properties=not self_calc,
                                                                properties=properties,
                                                                )
        except PropertiesOptionError as err:
            # raise PropertiesOptionError (which is catched) because must not add value None in carry_out_calculation
            if param.notraisepropertyerror or param.raisepropertyerror:
                raise err from err
            raise ConfigError(_('unable to carry out a calculation for "{}"'
                                ', {}').format(option.impl_get_display_name(), err), err) from err
        except ValueError as err:
            raise ValueError(_('the option "{0}" is used in a calculation but is invalid ({1})').format(option.impl_get_display_name(), err)) from err
        except AttributeError as err:
            if isinstance(param, ParamDynOption) and param.optional:
                # cannot acces, simulate a propertyerror
                raise PropertiesOptionError(param,
                                            ['configerror'],
                                            config_bag.context.get_settings(),
                                            )
            raise ConfigError(_(f'unable to get value for calculating "{option.impl_get_display_name()}", {err}')) from err
        if len(options_bag) > 1:
            parent_option_bag = options_bag[-2]
        else:
            parent_option_bag = None
        return parent_option_bag, options_bag[-1]

    if isinstance(param, ParamValue):
        return param.value

    if isinstance(param, ParamInformation):
        if isinstance(param, ParamSelfInformation):
            option_bag = OptionBag(option,
                                   index,
                                   config_bag,
                                   )
        elif param.option:
            option_bag = OptionBag(param.option,
                                   None,
                                   config_bag,
                                   )
        else:
            option_bag = None
        try:
            return config_bag.context.get_values().get_information(option_bag,
                                                                   param.information_name,
                                                                   param.default_value,
                                                                   )
        except ValueError as err:
            raise ConfigError(_('option "{}" cannot be calculated: {}').format(option.impl_get_display_name(),
                                                                               str(err),
                                                                               ))

    if isinstance(param, ParamIndex):
        return index

    if isinstance(param, ParamSuffix):
        if not option.issubdyn():
            raise ConfigError(_('option "{}" is not in a dynoptiondescription').format(option.impl_get_display_name()))
        return option.impl_getsuffix()

    if isinstance(param, ParamSelfOption):
        value = calc_self(param,
                          option,
                          index,
                          orig_value,
                          config_bag,
                          )
        if callback.__name__ not in FUNCTION_WAITING_FOR_DICT:
            return value
        return {'name': option.impl_get_display_name(),
                'value': value,
                }

    if isinstance(param, ParamOption):
        callbk_option = param.option
        callbk_options = None
        if callbk_option.issubdyn():
            found = False
            if isinstance(param, ParamDynOption):
                od_path = param.dynoptiondescription.impl_getpath()
                if "." in od_path:
                    rootpath = od_path.rsplit('.', 1)[0] + '.'
                else:
                    rootpath = ''
                full_path = rootpath + param.subpath
                root_option_bag = OptionBag(config_bag.context.get_description(),
                                            None,
                                            config_bag,
                                            )
                try:
                    soptions_bag = config_bag.context.get_sub_option_bag(root_option_bag,
                                                                         full_path,
                                                                         #FIXME index?
                                                                         index=None,
                                                                         validate_properties=True,
                                                                         properties=None,
                                                                         )
                except AttributeError as err:
                    raise ConfigError(_(f'option "{option.impl_get_display_name()}" is not in a dynoptiondescription: {err}'))
                callbk_option = soptions_bag[-1].option
                found = True
            elif option.impl_is_sub_dyn_optiondescription():
                if option.getsubdyn() == callbk_option.getsubdyn():
                    root_path = option.impl_getpath().rsplit('.', 1)[0]
                    len_path = root_path.count('.')
                    full_path = root_path + '.' + callbk_option.impl_getpath().split('.', len_path + 1)[-1]
                    root_option_bag = OptionBag(config_bag.context.get_description(),
                                                None,
                                                config_bag,
                                                )
                    try:
                        soptions_bag = config_bag.context.get_sub_option_bag(root_option_bag,
                                                                             full_path,
                                                                             #FIXME index?
                                                                             index=None,
                                                                             validate_properties=True,
                                                                             properties=None,
                                                                             )
                    except AttributeError as err:
                        raise ConfigError(_(f'option "{option.impl_get_display_name()}" is not in a dynoptiondescription: {err}'))
                    callbk_option = soptions_bag[-1].option
                    found = True
            elif option.impl_is_dynsymlinkoption():
                rootpath = option.rootpath
                call_path = callbk_option.impl_getpath()
                if option.opt.issubdyn() and callbk_option.getsubdyn() == option.getsubdyn() or \
                        not option.opt.issubdyn() and callbk_option.getsubdyn() == option.opt:
                    # in same dynoption
                    suffix = option.impl_getsuffix()
                    subdyn = callbk_option.getsubdyn()
                    root_path, sub_path = subdyn.split_path(subdyn,
                                                            option,
                                                            )
                    if root_path:
                        parent_path = root_path + subdyn.impl_getname(suffix) + sub_path
                    else:
                        parent_path = subdyn.impl_getname(suffix) + sub_path
                    callbk_option = callbk_option.to_dynoption(parent_path,
                                                               suffix,
                                                               subdyn,
                                                               )
                    found = True
            if not found:
                callbk_options = []
                for doption_bag in callbk_option.getsubdyn().get_sub_children(callbk_option,
                                                                              config_bag,
                                                                              index=None,
                                                                              ):
                    callbk_options.append(doption_bag.option)
        if callbk_options is None:
            callbk_options = [callbk_option]
            values = None
        else:
            values = []
        for callbk_option in callbk_options:
            if index is not None and callbk_option.impl_get_leadership() and \
                    callbk_option.impl_get_leadership().in_same_leadership(option):
                if not callbk_option.impl_is_follower():
                    # leader
                    index_ = None
                    with_index = True
                else:
                    # follower
                    index_ = index
                    with_index = False
            else:
                index_ = None
                with_index = False
            if callbk_option.impl_getpath() == 'od.dodval1.st.boolean':
                raise Exception('pfff')
            value = get_value(config_bag,
                              callbk_option,
                              param,
                              index_,
                              False,
                              )
            if with_index:
                value = value[index]
            if values is not None:
                values.append(value)
        if values is not None:
            value = values
        if callback.__name__ not in FUNCTION_WAITING_FOR_DICT:
            return value
        return {'name': callbk_option.impl_get_display_name(),
                'value': value}


def carry_out_calculation(option,
                          callback: Callable,
                          callback_params: Optional[Params],
                          index: Optional[int],
                          config_bag: Optional[ConfigBag],
                          orig_value=undefined,
                          allow_value_error: bool=False,
                          force_value_warning: bool=False,
                          for_settings: bool=False,
                          ):
    """a function that carries out a calculation for an option's value

    :param option: the option
    :param callback: the name of the callback function
    :param callback_params: the callback's parameters
                            (only keyword parameters are allowed)
    :param index: if an option is multi, only calculates the nth value
    :param allow_value_error: to know if carry_out_calculation can return ValueError or ValueWarning (for example if it's a validation)
    :param force_value_warning: transform valueError to ValueWarning object

    The callback_params is a dict. Key is used to build args (if key is '')
    and kwargs (otherwise). Values are tuple of:
    - values
    - tuple with option and boolean's force_permissive (True when don't raise
    if PropertiesOptionError)
    Values could have multiple values only when key is ''."""
    if not option.impl_is_optiondescription() and option.impl_is_follower() and index is None:
        raise Exception('follower must have index in carry_out_calculation!')
    def fake_items(iterator):
        return ((None, i) for i in iterator)
    args = []
    kwargs = {}
    if callback_params:
        for key, param in chain(fake_items(callback_params.args), callback_params.kwargs.items()):
            try:
                value = manager_callback(callback,
                                         param,
                                         option,
                                         index,
                                         orig_value,
                                         config_bag,
                                         for_settings,
                                         )
                if key is None:
                    args.append(value)
                else:
                    kwargs[key] = value
            except PropertiesOptionError as err:
                if param.raisepropertyerror:
                    raise err
                if callback.__name__ in FUNCTION_WAITING_FOR_DICT:
                    if key is None:
                        args.append({'propertyerror': str(err), 'name': option.impl_get_display_name()})
                    else:
                        kwargs[key] = {'propertyerror': str(err), 'name': option.impl_get_display_name()}
    ret = calculate(option,
                    callback,
                    allow_value_error,
                    force_value_warning,
                    args,
                    kwargs,
                    )
    if isinstance(ret, list) and not option.impl_is_dynoptiondescription() and \
            option.impl_is_follower() and not option.impl_is_submulti():
        if args or kwargs:
            raise LeadershipError(_('the "{}" function with positional arguments "{}" '
                                    'and keyword arguments "{}" must not return '
                                    'a list ("{}") for the follower option "{}"'
                                    '').format(callback.__name__,
                                               args,
                                               kwargs,
                                               ret,
                                               option.impl_get_display_name()))
        else:
            raise LeadershipError(_('the "{}" function must not return a list ("{}") '
                                    'for the follower option "{}"'
                                    '').format(callback.__name__,
                                               ret,
                                               option.impl_get_display_name()))
    return ret


def calculate(option,
              callback: Callable,
              allow_value_error: bool,
              force_value_warning: bool,
              args,
              kwargs,
              ):
    """wrapper that launches the 'callback'

    :param callback: callback function
    :param args: in the callback's arity, the unnamed parameters
    :param kwargs: in the callback's arity, the named parameters

    """
    try:
        return callback(*args, **kwargs)
    except (ValueError, ValueWarning) as err:
        if allow_value_error:
            if force_value_warning:
                raise ValueWarning(str(err))
            raise err
        error = err
    except Exception as err:
        error = err
    if args or kwargs:
        msg = _('unexpected error "{0}" in function "{1}" with arguments "{3}" and "{4}" '
                'for option "{2}"').format(str(error),
                                           callback.__name__,
                                           option.impl_get_display_name(),
                                           args,
                                           kwargs)
    else:
        msg = _('unexpected error "{0}" in function "{1}" for option "{2}"'
                '').format(str(error),
                           callback.__name__,
                           option.impl_get_display_name())
    raise ConfigError(msg) from error
