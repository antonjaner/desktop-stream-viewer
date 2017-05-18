#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlink

from constants import HISTORY_FILE


class StreamModel:
    def __init__(self, grid):
        self.streamlink_session = streamlink.Streamlink()
        self.grid = grid
        self.stream_history = set()
        self.load_stream_history()

    def mute_all_streams(self, is_mute_checked):
        for video_frame in self.grid.videoframes:
            if is_mute_checked:
                video_frame.player.audio_set_mute(True)
            else:
                if not video_frame.is_muted:
                    video_frame.player.audio_set_mute(False)

    def export_streams_to_clipboard(self):
        return "\n".join([video_frame.stream.url for video_frame in self.grid.videoframes])

    def get_stream_options(self, *args):
        return self.streamlink_session.streams(*args)

    def add_new_videoframe(self, *args):
        self.grid.add_new_videoframe(*args)

    def add_widget(self, *args):
        self.grid.addWidget(*args)

    def remove_widget(self, *args):
        self.grid.removeWidget(*args)

    def save_stream_to_history(self, url):
        """Saves a stream to history file."""
        with open(HISTORY_FILE, 'a') as f:
            f.write(url + '\n')

    def load_stream_history(self):
        """Loads up all streams from last session."""
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.stream_history.add(line.strip("\n"))
        # Clear history file
        open(HISTORY_FILE, 'w').close()

    @staticmethod
    def streams(stream_url):
        streamlink.streams(stream_url)

    @staticmethod
    def new_stream(stream_url, stream_quality):
        return {"url": stream_url, "quality": stream_quality}
