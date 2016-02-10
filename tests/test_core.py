# -*- coding: utf-8 -*-
import unittest

import mock

from pytracetable.core import tracetable, tracetable_context_manager


@tracetable()
def weird_sum_function(var_parameter_1, var_parameter_2=42):
    ''' Helper function in order to show tracetable decorators in action '''
    var_added_inside_function = 101
    var_added_inside_function += 1
    var_added_inside_function += var_parameter_1
    var_added_inside_function += var_parameter_2

    del var_parameter_1
    del var_parameter_2

    return var_added_inside_function


class WeirdSumStaticMethod(object):
    @staticmethod
    @tracetable()
    def do_it(var_parameter_1, var_parameter_2=42):
        ''' Helper method in order to show tracetable decorators in action '''
        var_added_inside_function = 101
        var_added_inside_function += 1
        var_added_inside_function += var_parameter_1
        var_added_inside_function += var_parameter_2

        del var_parameter_1
        del var_parameter_2

        return var_added_inside_function


class WeirdSumMethod(object):
    @tracetable()
    def do_it(self, var_parameter_1, var_parameter_2=42):
        ''' Helper method in order to show tracetable decorators in action '''
        var_added_inside_function = 101
        var_added_inside_function += 1
        var_added_inside_function += var_parameter_1
        var_added_inside_function += var_parameter_2

        del var_parameter_1
        del var_parameter_2

        return var_added_inside_function


class tracetableTestCase(unittest.TestCase):
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    @mock.patch.object(tracetable_context_manager, 'show_added')
    def test_vars_added(self, show_added_mocked, *mocks):
        return_value = weird_sum_function(12)
        self.assertEquals(return_value, 12 + 42 + 101 + 1)

        self.assertEquals(show_added_mocked.call_count, 2)
        self.assertEquals(show_added_mocked.call_args_list[0][0][0], {'var_parameter_1': 12, 'var_parameter_2': 42})
        self.assertEquals(show_added_mocked.call_args_list[1][0][0], {'var_added_inside_function': 101})

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    def test_vars_changed(self, show_changed_mocked, *mocks):
        return_value = weird_sum_function(12)
        self.assertEquals(return_value, 12 + 42 + 101 + 1)

        self.assertEquals(show_changed_mocked.call_count, 3)
        self.assertEquals(show_changed_mocked.call_args_list[0][0][0], {'var_added_inside_function': [101, 102]})
        self.assertEquals(show_changed_mocked.call_args_list[1][0][0], {'var_added_inside_function': [102, 114]})
        self.assertEquals(show_changed_mocked.call_args_list[2][0][0], {'var_added_inside_function': [114, 156]})

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    def test_vars_deleted(self, show_removed_mocked, *mocks):
        return_value = weird_sum_function(12)
        self.assertEquals(return_value, 12 + 42 + 101 + 1)

        self.assertEquals(show_removed_mocked.call_count, 2)
        self.assertEquals(show_removed_mocked.call_args_list[0][0][0], set(['var_parameter_1']))
        self.assertEquals(show_removed_mocked.call_args_list[1][0][0], set(['var_parameter_2']))

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    def test_value_returned(self, show_returned_mocked, *mocks):
        return_value = weird_sum_function(12)
        self.assertEquals(return_value, 12 + 42 + 101 + 1)

        self.assertEquals(show_returned_mocked.call_count, 1)
        self.assertEquals(show_returned_mocked.call_args_list[0][0][0], 12 + 42 + 101 + 1)

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    def test_full_lifecycle(self, show_returned_mocked, show_removed_mocked, show_changed_mocked, show_added_mocked):
        ''' This test does the same as the other ones, but on an e2e approach.
            Given other ones have passed, this test could be considered useless.
            I'm just letting it survive in order to show all interaction on tracetable and tracetable_context_manager
        '''
        return_value = weird_sum_function(12)
        self.assertEquals(return_value, 12 + 42 + 101 + 1)

        self.assertEquals(show_added_mocked.call_args_list[0][0][0], {'var_parameter_1': 12, 'var_parameter_2': 42})
        self.assertEquals(show_added_mocked.call_args_list[1][0][0], {'var_added_inside_function': 101})
        self.assertEquals(show_changed_mocked.call_args_list[0][0][0], {'var_added_inside_function': [101, 102]})
        self.assertEquals(show_changed_mocked.call_args_list[1][0][0], {'var_added_inside_function': [102, 114]})
        self.assertEquals(show_changed_mocked.call_args_list[2][0][0], {'var_added_inside_function': [114, 156]})
        self.assertEquals(show_removed_mocked.call_args_list[0][0][0], set(['var_parameter_1']))
        self.assertEquals(show_removed_mocked.call_args_list[1][0][0], set(['var_parameter_2']))
        self.assertEquals(show_returned_mocked.call_args_list[0][0][0], 12 + 42 + 101 + 1)

    def test_function_attributes_are_kept(self):
        ''' Decorating a function with `tracetable` must not changes its identity '''
        self.assertEquals(weird_sum_function.__name__, 'weird_sum_function')
        self.assertEquals(weird_sum_function.__doc__, ' Helper function in order to show tracetable decorators in action ')

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    def test_staticmethod_behavior_is_the_same(self, show_returned_mocked, show_removed_mocked, show_changed_mocked,
                                               show_added_mocked):
        weird_sum_method = WeirdSumStaticMethod()
        weird_sum_method.do_it(12)

        self.assertEquals(show_added_mocked.call_args_list[0][0][0], {'var_parameter_1': 12, 'var_parameter_2': 42})
        self.assertEquals(show_added_mocked.call_args_list[1][0][0], {'var_added_inside_function': 101})
        self.assertEquals(show_changed_mocked.call_args_list[0][0][0], {'var_added_inside_function': [101, 102]})
        self.assertEquals(show_changed_mocked.call_args_list[1][0][0], {'var_added_inside_function': [102, 114]})
        self.assertEquals(show_changed_mocked.call_args_list[2][0][0], {'var_added_inside_function': [114, 156]})
        self.assertEquals(show_removed_mocked.call_args_list[0][0][0], set(['var_parameter_1']))
        self.assertEquals(show_removed_mocked.call_args_list[1][0][0], set(['var_parameter_2']))
        self.assertEquals(show_returned_mocked.call_args_list[0][0][0], 12 + 42 + 101 + 1)

        self.assertEquals(weird_sum_method.do_it.__name__, 'do_it')
        self.assertEquals(weird_sum_method.do_it.__doc__, ' Helper method in order to show tracetable decorators in action ')

    @mock.patch.object(tracetable_context_manager, 'show_added')
    @mock.patch.object(tracetable_context_manager, 'show_changed')
    @mock.patch.object(tracetable_context_manager, 'show_removed')
    @mock.patch.object(tracetable_context_manager, 'show_returned')
    def test_method_behavior_is_the_same(self, show_returned_mocked, show_removed_mocked, show_changed_mocked, show_added_mocked):
        weird_sum_method = WeirdSumMethod()
        weird_sum_method.do_it(12)

        # there's a `self` here which I dont have a proper value (since it varies its id)
        self.assertEquals(set(['var_parameter_1', 'var_parameter_2', 'self']),
                          set(show_added_mocked.call_args_list[0][0][0].keys()))
        self.assertDictContainsSubset({'var_parameter_1': 12, 'var_parameter_2': 42}, show_added_mocked.call_args_list[0][0][0])

        self.assertEquals(show_added_mocked.call_args_list[1][0][0], {'var_added_inside_function': 101})
        self.assertEquals(show_changed_mocked.call_args_list[0][0][0], {'var_added_inside_function': [101, 102]})
        self.assertEquals(show_changed_mocked.call_args_list[1][0][0], {'var_added_inside_function': [102, 114]})
        self.assertEquals(show_changed_mocked.call_args_list[2][0][0], {'var_added_inside_function': [114, 156]})
        self.assertEquals(show_removed_mocked.call_args_list[0][0][0], set(['var_parameter_1']))
        self.assertEquals(show_removed_mocked.call_args_list[1][0][0], set(['var_parameter_2']))
        self.assertEquals(show_returned_mocked.call_args_list[0][0][0], 12 + 42 + 101 + 1)

        self.assertEquals(weird_sum_method.do_it.__name__, 'do_it')
        self.assertEquals(weird_sum_method.do_it.__doc__, ' Helper method in order to show tracetable decorators in action ')
