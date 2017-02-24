# -*- coding: utf-8 -*-
import ctypes

import callbacks as cb
import streamlink


class StreamContainer(object):
    """Contains all neccesary values for libVLC playback.

    Args:
        vlc_instance (libvlc_instance_t*): The vlc instance.
        stream_info (dict): Holds information about stream url and stream quality.

    Attributes:
        media (libvlc_media_t*): The media object that vlc uses, includes callbacks.
    """

    def __init__(self, vlc_instance, stream_info):
        # Get the stream from streamlink
        streams = streamlink.streams(stream_info["url"])
        self._stream = streams[stream_info["quality"]].open()
        # Cast this container to a c pointer to use in the callbacks
        self._opaque = ctypes.cast(ctypes.pointer(
            ctypes.py_object(self)), ctypes.c_void_p)
        # Create the vlc callbacks, these will in turn call this container
        self.media = vlc_instance.media_new_callbacks(
            cb.CALLBACKS["read"],
            cb.CALLBACKS["open"],
            cb.CALLBACKS["seek"],
            cb.CALLBACKS["close"],
            self._opaque
        )

    def open(self):
        """The open event is triggered after media_open_cb in libVLC
        """

        return 0

    def read(self, buf, length):
        """Read reads from the stream and writes this to the buf according to
        the length parameter.

        buf (LP_c_char):    char pointer to the video buffer.
        length:             amount that should be read from the buffer.
        """

        data = self._stream.read(length)

        for i, val in enumerate(data):
            buf[i] = val

        return len(data)

    def seek(self, offset):
        """Seeks in the stream according to the offset.

        offset: absolute byte offset to seek to in the media.
        """

        return 0

    def close(self):
        """Close calls all neccesary functions to close down the container.
        """

        self._stream.close()
