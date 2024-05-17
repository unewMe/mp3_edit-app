import time
from dataclasses import dataclass


@dataclass
class Timer:
    """
    Class to measure time elapsed.
    """
    start_time: float | None = None  # time when timer started
    elapsed_time: float = 0  # time elapsed since timer started
    is_running: bool = False  # flag to check if timer is running

    def start(self):
        """Start timer"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def pause(self):
        """Pause timer"""
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def resume(self):
        """Resume timer"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        """Stop timer"""
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def get_time_seconds(self):
        """Return time in seconds"""
        if self.is_running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def get_time_minutes(self):
        """Return time in minutes"""
        return self.get_time_seconds() / 60

    def get_time_hours(self):
        """Return time in hours"""
        return self.get_time_minutes() / 60

    def get_time(self):
        """Return hours, minutes, seconds"""
        time = self.get_time_seconds()
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time % 60
        return hours, minutes, seconds

    def restart(self):
        """Restart timer"""
        self.start_time = time.time()
        self.elapsed_time = 0
        self.is_running = False
