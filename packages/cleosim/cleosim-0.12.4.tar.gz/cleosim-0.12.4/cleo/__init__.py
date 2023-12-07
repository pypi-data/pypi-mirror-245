"""Contains core classes and functions for the Cleo package."""
from __future__ import annotations

# auto-import submodules
import cleo.ephys
import cleo.opto
import cleo.coords
import cleo.stimulators
import cleo.recorders
import cleo.ioproc
import cleo.utilities
import cleo.viz
import cleo.imaging
import cleo.registry

from cleo.base import (
    CLSimulator,
    Recorder,
    Stimulator,
    InterfaceDevice,
    IOProcessor,
    SynapseDevice,
)
