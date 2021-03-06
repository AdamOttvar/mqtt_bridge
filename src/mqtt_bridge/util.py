#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib import import_module

from rosbridge_library.internal import message_conversion

def lookup_object(object_path, package='mqtt_bridge'):
    """ lookup object from a some.module:object_name specification. """
    module_name, obj_name = object_path.split(":")
    module = import_module(module_name, package)
    obj = getattr(module, obj_name)
    return obj

extract_values = message_conversion.extract_values
populate_instance = message_conversion.populate_instance

__all__ = ['lookup_object', 'extract_values', 'populate_instance']
