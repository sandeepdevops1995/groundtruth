from datetime import datetime, timezone
import time
from sqlalchemy.types import TypeDecorator, DateTime


class IntegerDateTime(TypeDecorator):
    """a type that decorates DateTime, converts to unix time on
    the way in and to datetime.datetime objects on the way out."""
    impl = DateTime
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo
    def process_bind_param(self, value, engine):
        # print("int(value)--------------",int(value))
        value = datetime.fromtimestamp(int(value)/1000)
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(timezone.utc)
    # def process_result_value(self, value, engine):
    #     """Assumes a datetime.datetime"""
    #     assert isinstance(value, datetime)
    #     return int(time.mktime(value.timetuple()))
    # def copy(self):
    #     return IntegerDateTime(timezone=self.timezone)