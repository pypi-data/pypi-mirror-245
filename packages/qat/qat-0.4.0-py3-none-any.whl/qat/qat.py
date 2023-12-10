# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Public Qat API
"""

# Some imports are only to make types accessible with qat.Type without using 'internal' namespace
# pylint: disable=unused-import

# Mouse events require many arguments
# pylint: disable = too-many-arguments


from dataclasses import dataclass
from pathlib import Path
import json
import os
import time

from qat.internal import app_launcher
from qat.internal.application_context import ApplicationContext
from qat.internal.qt_custom_object import QtCustomObject
from qat.internal.qt_object import QtObject
import qat.internal.communication_operations as comm
import qat.internal.debug_operations as debug
import qat.internal.find_object as find
import qat.internal.mouse_operations as mouse
import qat.internal.gesture_operations as gesture
import qat.internal.keyboard_operations as keyboard
import qat.internal.screenshot_operations as screenshot

from qat.internal.mouse_operations import Button, Modifier
from qat.internal.xml_report import XmlReport
from qat.internal.binding import Binding

from qat.test_settings import Settings

@dataclass
class Globals:
    """
    Holds the global state of the API
    """
    current_report = None
    current_app_context = None


def register_application(name: str, path: str, args='', shared = False) -> None:
    """
    Add the given application to the configuration file
    """
    config_file = get_config_file(shared)
    applications = {}
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            applications = json.load(file)
    except: # pylint: disable=bare-except
        print("Invalid configuration file. Content will be overwritten.")
    applications[name] = {
        "path": path,
        "args": args
    }
    if not config_file.is_file():
        os.makedirs(config_file.parent, exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as file:
            file.write("{}")
            file.close()
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(applications, file, indent=3)


def unregister_application(name: str, shared = False) -> None:
    """
    Remove the given application from the configuration file
    """
    config_file = get_config_file(shared)
    applications = {}
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as file:
            applications = json.load(file)

    if name in applications:
        del applications[name]
        if len(applications) > 0:
            with open(config_file, 'w', encoding='utf-8') as file:
                json.dump(applications, file, indent=3)
        else:
            os.remove(config_file)


def list_applications() -> dict:
    """
    List all registered applications (shared and local)
    """
    return app_launcher.list_applications()


def get_config_file(shared = None) -> Path:
    """
    Return the current configuration file
    """
    return app_launcher.get_config_file(shared)


def get_application_path(name: str) -> str:
    """
    Return the path of the given application from the configuration file
    """
    applications = list_applications()
    return applications[name]['path']


def start_application(app_name: str, args=None, detached=False) -> ApplicationContext:
    """
    Start the given application, inject the server library (except if detached is True)
    and return the corresponding application context
    """
    Globals.current_app_context = None
    Globals.current_app_context = app_launcher.start_application(app_name, args, detached)
    return Globals.current_app_context


def attach_to_application(name_or_pid) -> ApplicationContext:
    """
    Attach to the given application by name or process ID.
    If a name is given, it must correspond to a registered application.
    """
    Globals.current_app_context = app_launcher.attach_to(name_or_pid)
    return Globals.current_app_context


def current_application_context() -> ApplicationContext:
    """
    Return the current application context.
    All calls are using this context.
    """
    return Globals.current_app_context


def set_current_application_context(app_context: ApplicationContext):
    """
    Change the current application context.
    All subsequent calls will use this context until this function is called again.
    """
    Globals.current_app_context = app_context


def close_application(app_context = None) -> int:
    """
    Terminate the application associated to the given context
    and returns the exit code
    """
    if app_context is None:
        app_context = current_application_context()
    if app_context:
        app_context.kill()
        exit_code = app_context.get_exit_code()
        Globals.current_app_context = None
        return exit_code
    raise ProcessLookupError("Cannot close application: process does not exist")


def lock_application():
    """
    Lock application by filtering external/user events
    """
    return debug.lock_application(current_application_context())


def unlock_application():
    """
    Unlock application GUI by allowing external/user events
    """
    return debug.unlock_application(current_application_context())


def list_top_windows() -> list:
    """
    Return all the top windows of the application.
    """
    return find.list_top_windows(Globals.current_app_context)


def find_all_objects(definition: dict) -> list:
    """
    Return all objects matching the given definition.
    """
    return find.find_all_objects(Globals.current_app_context, definition)


def wait_for_object_exists(definition: dict, timeout=None) -> QtObject:
    """
    Wait for the given object to exist in the AUT.
    """
    if timeout is None:
        timeout = Settings.wait_for_object_timeout
    return find.wait_for_object_exists(Globals.current_app_context, definition, timeout)


def wait_for_object(definition: dict, timeout=None) -> QtObject:
    """
    Wait for the given object to be accessible (i.e visible and enabled) in the AUT.
    """
    if timeout is None:
        timeout = Settings.wait_for_object_timeout
    return find.wait_for_object(Globals.current_app_context, definition, timeout)


def wait_for(condition, timeout=None) -> bool:
    """
    Wait for the given condition to be reached.
    Return True if the condition was reached before timeout, False otherwise
    """
    if timeout is None:
        timeout = Settings.wait_for_object_timeout
    start_time = round(1000 * time.time())
    reached = False
    while not reached and (round(1000 * time.time()) - start_time) < timeout:
        reached = condition()
        if reached:
            break
        time.sleep(0.2)

    return reached


def mouse_press(
        definition: dict,
        x=None,
        y=None,
        modifier=Modifier.NONE,
        button=Button.LEFT,
        check=False):
    """
    Click on the given widget using the given parameters.
    """
    mouse.click(Globals.current_app_context, definition,
                "press", x, y, modifier, button, check)


def mouse_release(
        definition: dict,
        x=None,
        y=None,
        modifier=Modifier.NONE,
        button=Button.LEFT,
        check=False):
    """
    Click on the given widget using the given parameters.
    """
    mouse.click(Globals.current_app_context, definition,
                "release", x, y, modifier, button, check)


def mouse_click(
        definition: dict,
        x=None,
        y=None,
        modifier=Modifier.NONE,
        button=Button.LEFT,
        check=False):
    """
    Click on the given widget using the given parameters.
    """
    mouse.click(Globals.current_app_context, definition,
                "click", x, y, modifier, button, check)


def double_click(
        definition: dict,
        x=None,
        y=None,
        modifier=Modifier.NONE,
        button=Button.LEFT,
        check=False):
    """
    Double-click on the given widget using the given parameters.
    """
    mouse.click(Globals.current_app_context, definition,
                "doubleClick", x, y, modifier, button, check)


def mouse_move(
        definition: dict,
        x=None,
        y=None,
        modifier=Modifier.NONE,
        button=Button.LEFT):
    """
    Move the mouse using the given parameters.
    """
    mouse.click(Globals.current_app_context, definition,
                "move", x, y, modifier, button)


def mouse_drag(
        definition: dict,
        x=None,
        y=None,
        dx=None,
        dy=None,
        modifier=Modifier.NONE,
        button=Button.LEFT,
        check=False):
    """
    Drag the mouse using the given parameters.
    """
    mouse.drag(Globals.current_app_context, definition, 'drag', x,
               y, dx, dy, modifier, button, check=check)


def mouse_wheel(
        definition: dict,
        x=None,
        y=None,
        x_degrees=0,
        y_degrees=0,
        modifier=Modifier.NONE,
        check=False):
    """
    Scroll the mouse by x/y degrees at x/y position.
    Default degree increment should be 15 to represent one physical rotation increment.
    """
    mouse.drag(Globals.current_app_context, definition, 'scroll', x, y, 8 * x_degrees,
               8 * y_degrees, modifier=modifier, button=Button.MIDDLE, check=check)


def flick(
        definition: dict,
        dx=0,
        dy=0):
    """
    Move the given Flickable by the given horizontal and vertical distances in pixels.
    """
    gesture.flick(Globals.current_app_context, definition, dx, dy)


def type_in(
        definition: dict,
        text: str):
    """
    Type the given text in the given object.
    The following special keys are supported:
    <Backspace>, <Delete>, <Enter>, <Escape>, <Return>, <Tab>, <Control>, <Shift>, <Alt>
    """
    keyboard.type_in(Globals.current_app_context, definition, text)


def shortcut(
        definition: dict,
        key_combination: str):
    """
    Trigger the given shortcut on the given object.
    Shortcut string must follow the Qt syntax, e.g:
    'Ctrl+Z, Alt+O, Alt+Shift+R, ...'
    """

    keyboard.shortcut(Globals.current_app_context, definition, key_combination)


def press_key(
        definition: dict,
        key: str):
    """
    Press the given key on the given object.
    The following special keys are supported:
    <Backspace>, <Delete>, <Enter>, <Escape>, <Return>, <Tab>, <Control>, <Shift>, <Alt>
    """
    keyboard.press_key(Globals.current_app_context, definition, key)


def release_key(
        definition: dict,
        key: str):
    """
    Release the given key on the given object.
    The following special keys are supported:
    <Backspace>, <Delete>, <Enter>, <Escape>, <Return>, <Tab>, <Control>, <Shift>, <Alt>
    """
    keyboard.release_key(Globals.current_app_context, definition, key)


def take_screenshot(path=None):
    """
    Take a screenshot of each current main window and save 
    them to the given path. If no path is provided, screenshots will be
    saved to the 'screenshots' subfolder of the current directory
    """
    screenshot.take_screenshot(Globals.current_app_context, path)


def grab_screenshot(definition, delay=0, timeout=None):
    """
    Take a screenshot of the given widget after an optional delay in ms
    """
    if timeout is None:
        timeout = Settings.wait_for_object_timeout
    return screenshot.grab_screenshot(Globals.current_app_context, definition, delay, timeout)


def activate_picker():
    """
    Activate the object picker
    """
    debug.activate_picker(Globals.current_app_context)


def deactivate_picker():
    """
    Deactivate the object picker
    """
    debug.deactivate_picker(Globals.current_app_context)


def connect(
        object_def: dict,
        object_property: str,
        callback) -> str:
    """
    Connect a signal from the application to the given callback.
    If 'object_property' is a signal name, the given callback will be called without argument.
    If 'object_property' is a Qt property name, the given callback will be called with
    one argument containing the new value of the property.
    Return a unique identifier for the newly created connection
    """
    return comm.connect(Globals.current_app_context, object_def, object_property, callback)


def disconnect(conn_id: str):
    """
    Disconnect a signal from its callback.
    The conn_id argument must be a connection identifier, as returned by connect()
    """
    return comm.disconnect(Globals.current_app_context, conn_id)


def bind(
        remote_object: dict,
        remote_property: str,
        local_object,
        local_property: str) -> Binding:
    """
    Automatically establish a connection between the given object's property and the given receiver.
    The returned Binding object can be used to manage the connection.
    Note: this is equivalent to create a Binding object with the same arguments.
    """
    return Binding(remote_object, remote_property, local_object, local_property)
