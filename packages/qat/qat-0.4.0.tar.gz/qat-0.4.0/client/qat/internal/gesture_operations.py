# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Functions related to gestures
"""

from qat.internal.application_context import ApplicationContext
from qat.internal import find_object


def flick(
        app_context: ApplicationContext,
        definition: dict,
        dx=0,
        dy=0):
    """
    Move the given Flickable by the given horizontal and vertical distances in pixels.
    """
    definition = find_object.object_to_definition(definition)
    find_object.wait_for_object(app_context, definition)

    args = {
        'dx': dx,
        'dy': dy
    }

    command = {}
    command['command'] = 'gesture'
    command['object'] = definition
    command['attribute'] = 'flick'
    command['args'] = args

    app_context.send_command(command)
