# -*- coding: utf-8 -*-
import functools
import sys

from colorama import Fore, Style


class tracetable_context_manager():
    def __init__(self, name, display_colors=True):
        self.name = name
        self.current_vars = {}
        self.display_colors = display_colors

    def __enter__(self):
        self.original_settrace = sys.settrace
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        sys.settrace = self.original_settrace

    @staticmethod
    def show_returned(return_value, display_colors):
        msg = '\t[RETURNED] {} ({})\n'.format(return_value, return_value.__class__.__name__)

        if display_colors:
            print(Fore.BLUE + msg)
            print(Style.RESET_ALL),
        else:
            print msg

    def show_added(self, added):
        for key, value in added.items():
            msg = '\t[ADDED]    {} ({}): {}'.format(key, value.__class__.__name__, value)

            if self.display_colors:
                print(Fore.GREEN + msg)
                print(Style.RESET_ALL),
            else:
                print msg

    def show_removed(self, removed):
        for item in removed:
            msg = '\t[REMOVED]  {}'.format(item)

            if self.display_colors:
                print(Fore.RED + msg)
                print(Style.RESET_ALL),
            else:
                print msg

    def show_changed(self, changed):
        for key, (old, new) in changed.items():
            msg = '\t[CHANGED]  {}: {} ({}) --> {} ({})'.format(key, old, old.__class__.__name__, new, new.__class__.__name__)

            if self.display_colors:
                print(Fore.YELLOW + msg)
                print(Style.RESET_ALL),
            else:
                print msg

    def trace_calls(self, frame, event, arg):
        if event != 'call' or frame.f_code.co_name != self.name:
            return
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        if event not in ['line', 'return']:
            return

        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        local_vars = frame.f_locals

        added = set(local_vars.keys()) - set(self.current_vars.keys())
        added = dict([[key, local_vars[key]] for key in added])

        removed = set(self.current_vars.keys()) - set(local_vars.keys())

        changed = {}
        for item in set(self.current_vars.keys()) & set(local_vars.keys()):
            if self.current_vars[item] != local_vars[item]:
                changed[item] = [self.current_vars[item], local_vars[item]]

        if any([added, removed, changed]):
            print '\n' + '-' * 50
            print 'At {}, line {}'.format(func_name, line_no)

        if added:
            self.show_added(added)

        if changed:
            self.show_changed(changed)

        if removed:
            self.show_removed(removed)

        self.current_vars = dict(local_vars)


def tracetable(display_colors=True):
    def inner(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            with tracetable_context_manager(func.__name__, display_colors=display_colors):
                return_value = func(*args, **kwargs)
                tracetable_context_manager.show_returned(return_value, display_colors=display_colors)

            return return_value
        return wrapper
    return inner
