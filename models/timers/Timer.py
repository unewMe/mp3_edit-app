import time
from dataclasses import dataclass


@dataclass
class Timer:
    """
    Class to measure time elapsed.
    """
    _start_time: float | None = None  # time when timer started
    _elapsed_time: float = 0  # time elapsed since timer started
    _is_running: bool = False  # flag to check if timer is running

    def start(self) -> None:
        """Start timer"""
        if not self._is_running:
            self._start_time = time.time()
            self._is_running = True

    def pause(self) -> None:
        """Pause timer"""
        if self._is_running:
            self._elapsed_time += time.time() - self._start_time
            self._is_running = False

    def resume(self) -> None:
        """Resume timer"""
        if not self._is_running:
            self._start_time = time.time()
            self._is_running = True

    def stop(self) -> None:
        """Stop timer"""
        if self._is_running:
            self._elapsed_time += time.time() - self._start_time
            self._is_running = False

    def get_time_seconds(self) -> float:
        """Return time in seconds"""
        if self._is_running:
            return self._elapsed_time + (time.time() - self._start_time)
        return self._elapsed_time

    def get_time_minutes(self) -> float:
        """Return time in minutes"""
        return self.get_time_seconds() / 60

    def get_time_hours(self) -> float:
        """Return time in hours"""
        return self.get_time_minutes() / 60

    def get_time(self) -> tuple[float, float, float]:
        """Return hours, minutes, seconds"""
        time = self.get_time_seconds()
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time % 60
        return hours, minutes, seconds

    def restart(self) -> None:
        """Restart timer"""
        self._start_time = time.time()
        self._elapsed_time = 0
        self._is_running = False

    def set_time(self, times: float) -> None:
        """Set time"""
        self._elapsed_time = times
        self._start_time = time.time()
        self._is_running = True
