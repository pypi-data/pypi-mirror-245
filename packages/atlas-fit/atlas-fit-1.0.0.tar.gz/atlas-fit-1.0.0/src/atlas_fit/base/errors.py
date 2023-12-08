#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module provides custom errors

@author: hoelken
"""


class IllegalStateError(RuntimeError):
    """Error to be raised if something is in an undefined state"""
    pass
