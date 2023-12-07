# pylint: disable=redefined-builtin
import sounddevice as sd
SAMPLE_RATE = 44100
sd.default.samplerate = SAMPLE_RATE  # type: ignore
sd.default.channels = 1  # type: ignore

__all__ = ('tone', 'sample', 'envelope', 'filter', 'instrument', 'notes', 'note', 'asyncplayer')
__version__ = "1.1.0"
released_version = "1.1.0"

from . import tone, sample, envelope, filter, instrument, notes, note, asyncplayer

