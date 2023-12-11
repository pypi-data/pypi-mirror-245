# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Functions related to object identification
"""

from copy import deepcopy
import time

from qat.test_settings import Settings
from qat.internal.application_context import ApplicationContext
from qat.internal.qt_object import QtObject


def object_to_definition(object_or_def) -> dict:
    """
    Return the definition dictionary of the given object
    """
    if isinstance(object_or_def, QtObject):
        definition = object_or_def.get_definition()
    else:
        definition = object_or_def
    for key in definition:
        if isinstance(definition[key], QtObject):
            definition[key] = object_to_definition(definition[key])

    return definition


def list_top_windows(
        app_context: ApplicationContext) -> list:
    """
    Return all the top windows of the application.
    """
    command = {}
    command['command'] = 'list'
    command['attribute'] = 'topWindows'

    result = app_context.send_command(command)

    objects = []
    if result['object']:
        for obj in result['object']:
            objects.append(QtObject(app_context, obj))
    return objects


def find_all_objects(
        app_context: ApplicationContext,
        definition: dict) -> list:
    """
    Return all objects matching the given definition.
    """
    definition = deepcopy(object_to_definition(definition))
    command = {}
    command['command'] = 'list'
    command['attribute'] = 'object'
    command['object'] = definition

    result = app_context.send_command(command)

    objects = []
    if result['object']:
        for obj in result['object']:
            objects.append(QtObject(app_context, obj))
    return objects


def wait_for_object_exists(
        app_context: ApplicationContext,
        definition: dict,
        timeout=Settings.wait_for_object_timeout) -> QtObject:
    """
    Wait for the given object to exist in the AUT.
    """
    start_time = round(1000 * time.time())
    definition = deepcopy(object_to_definition(definition))
    command = {}
    command['command'] = 'find'
    command['object'] = definition

    last_error = None
    while (round(1000 * time.time()) - start_time) < timeout:
        try:
            app_context.send_command(command, timeout)
            return QtObject(app_context, definition)
        except LookupError as error:
            last_error = error
            time.sleep(0.2)

    if last_error is not None:
        raise last_error
    return None


def wait_for_object(
        app_context: ApplicationContext,
        definition: dict,
        timeout=Settings.wait_for_object_timeout) -> QtObject:
    """
    Wait for the given object to be accessible (i.e visible and enabled) in the AUT.
    """
    definition = object_to_definition(definition)
    modified_def = deepcopy(definition)
    modified_def['visible'] = True
    modified_def['enabled'] = True
    return wait_for_object_exists(app_context, modified_def, timeout)
