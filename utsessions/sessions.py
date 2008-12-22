"""Session collector for managing sessions instances"""
from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout

SESSION_LIMIT_SECONDS = getattr(settings, 'SESSION_LIMIT_SECONDS', 0)
SESSION_TOKEN_LIMIT_SECONDS = getattr(settings, 'SESSION_TOKEN_LIMIT_SECONDS', 300)

class SessionCollector(object):
    """Collector of sessions for user"""
    def __init__(self):
        self._sessions = {}

    def register(self, request):
        """Register session by key with creation time"""
        if not request.session.session_key in self._sessions.keys():
            self._sessions[request.session.session_key] = (datetime.now(), request)

    @property
    def opened(self):
        """Return the number of sessions after a flush"""
        self.flush()
        return len(self._sessions)

    def flush(self):
        """Flush the cache of opened sessions and
        close expired session"""
        now = datetime.now()

        for session_key, values in self._sessions.items():
            creation_time, request = values
            delta = now - creation_time
            if SESSION_LIMIT_SECONDS and delta.seconds > SESSION_LIMIT_SECONDS:
                logout(request)
            if not request.session.exists(session_key):
                del self._sessions[session_key]

    def set_unique(self):
        """Choose the current session, and close the others"""
        current_session_key = self.get_current_session_key(user_key)

        for session_key, values in self._sessions.items():
            if session_key != most_recent_session_key:
                creation_time, request = values
                logout(request)

    def get_current_session_key(self):
        """Return the current session key, selected by his creation time
        and his limit before destruction"""
        most_recent = 0
        most_recent_key = ''

        for session_key, values in self._sessions.items():
            creation_time, request = values
            if creation_time.second > most_recent:
                if not SESSION_TOKEN_LIMIT_SECOND:
                    most_recent, most_recent_key = creation_time.second, session_key
                elif datetime_opened.second >= SESSION_TOKEN_LIMIT_SECONDS:
                    most_recent, most_recent_key = creation_time.second, session_key

        return most_recent_key
