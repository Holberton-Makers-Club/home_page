from models.base import Base


class Session(Base):
    """ Session class """
    exp_time = 3333
    sessions = {}

    def __init__(self, *args, **kwargs):
        """ init """
        from datetime import datetime
        super().__init__(*args, **kwargs)
        if kwargs.get('id'):
            self.id = kwargs.get('id')
        if kwargs.get('created_at'):
            self.created_at = kwargs.get('created_at')
        else:
            self.created_at = datetime.utcnow()
        self.user_id = kwargs.get('user_id')
        Session.sessions[self.id] = {
            'user_id': self.user_id,
            'created_at': self.created_at
        }
        self.save()

    @classmethod
    def expired(self, id, created_at):
        """
        check if session has expired. True if it has, False otherwise.
        """
        from datetime import datetime, timedelta
        import pytz
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if now > (created_at + timedelta(seconds=Session.exp_time)):
            return True
        return False
