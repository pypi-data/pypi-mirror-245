"""Top-level package for esgtoolkit."""

__author__ = """T. Moudiki"""
__email__ = 'thierry.moudiki@gmail.com'
__version__ = '1.0.0'

from .calculatereturns import calculatereturns
from .simdiff import simdiff

__all__ = ["calculatereturns", "simdiff"]