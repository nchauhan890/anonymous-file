"""Create an anonymous file for testing code."""

import sublime
import sublime_plugin

import os
import random
import string
import sys
import functools

token_chars = string.ascii_letters + string.digits
file_names = set()


def catch_settings_exception(func):
    """Catch exceptions in setting changes."""
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            r = func(*args, **kw)
        except Exception as e:
            sublime.status_message('{} error in '
                                   'AnonymousFile.sublime-settings:  {}'
                                   .format(type(e).__name__, e))
            print('AnonymousFile:', e.__class__.__name__, e)
            raise
            sys.exit(1)
        else:
            return r
    return wrapper


@catch_settings_exception
def change_dir():
    """Update 'dir' setting."""
    global dir_, variables
    dir_ = os.path.normpath(
        sublime.expand_variables(settings.get('dir'), variables)
    )
    if not os.path.isdir(dir_):
        raise TypeError('"dir" must be an existing directory')


@catch_settings_exception
def change_recent():
    """Update 'recently_closed' setting."""
    global recent, variables
    recent = os.path.normpath(
        sublime.expand_variables(settings.get('recently_closed'), variables)
    )
    if not os.path.isdir(dir_):
        raise TypeError('"recently_closed" must be an existing directory')


@catch_settings_exception
def change_keep():
    """Update 'keep' setting."""
    global keep
    keep = int(settings.get('keep'))
    if keep < 1:
        raise TypeError('"keep" must be greater than or equal to 0')
    if keep > 100:
        raise TypeError('"keep" cannot be more than 100')


@catch_settings_exception
def change_extension():
    """Update 'file_extension' setting."""
    global extension
    extension = settings.get('file_extension')
    if extension is None:
        raise TypeError('must give a file extension')


@catch_settings_exception
def plugin_loaded():
    """Set global variables upon loading."""
    global settings, dir_, recent, keep, extension
    global recent_file_names, variables
    settings = sublime.load_settings(
        'AnonymousFile.sublime-settings'
    )
    dir_ = settings.get('dir')
    recent = settings.get('recently_closed')
    keep = int(settings.get('keep'))
    extension = settings.get('file_extension')

    settings.add_on_change('dir', change_dir)
    settings.add_on_change('recently_closed', change_recent)
    settings.add_on_change('keep', change_keep)
    settings.add_on_change('file_extension', change_extension)

    variables = sublime.active_window().extract_variables()
    dir_ = os.path.normpath(sublime.expand_variables(dir_, variables))
    recent = os.path.normpath(sublime.expand_variables(recent, variables))

    with open(os.path.join(dir_, 'recent_files.txt'), 'r+') as f:
        recent_file_names = [line.strip() for line in f]


class AnonymousFileCommand(sublime_plugin.TextCommand):
    """Create anonymousfile."""

    def run(self, edit):
        """Run anonymous_file command."""
        global file_names
        window = self.view.window()
        view = self.view

        file_token = ''.join([random.choice(token_chars)
                              for _ in range(3)])

        file_name = 'af_' + file_token + extension
        file_path = os.path.normpath(dir_) + os.path.sep + file_name
        file = open(file_path, 'x')
        file_names.add(file_name)
        print('AnonymousFile: created', file_name)
        print('AnonymousFile: recently closed files:')
        print('\n'.join(recent_file_names))

        file_view = window.open_file(file_path)
        file.close()
        window.focus_view(file_view)
        view.run_command('new_dir')


class CloseFileCommand(sublime_plugin.EventListener):
    """Handle file closing/saving."""

    def on_close(self, view):
        """Close anonymous files."""
        path = view.file_name()
        file_path, file = os.path.split(path)

        if file in file_names and dir_ == file_path:
            try:
                os.rename(path, os.path.join(recent, file))
                while len(os.listdir(recent)) > keep and recent_file_names:
                    try:
                        os.remove(os.path.join(
                                  recent, recent_file_names.pop(0)))
                    except FileNotFoundError:
                        pass

                file_names.remove(file)
                recent_file_names.append(file)
                print('AnonymousFile: closed', file)
                print('AnonymousFile: recently closed files:')
                print('\n'.join(recent_file_names))
                with open(os.path.join(dir_, 'recent_files.txt'), 'w+') as f:
                    for i in recent_file_names:
                        f.write(i + '\n')

            except Exception as e:
                print('AnonymousFile:', type(e), e)


class SaveAnonymousFileCommand(sublime_plugin.TextCommand):
    """Save anonymous file in a new directory."""

    def run(self, edit):
        """Save file elsewhere instead of deleting upon closure."""
        path = self.view.file_name()
        file_path, file = os.path.split(path)
        if file in file_names and dir_ == file_path:
            self.view.run_command('prompt_save_as')
            file_names.remove(file)
