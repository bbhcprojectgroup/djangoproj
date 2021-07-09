from login.models import Account
import logging


class MyAuthBackend(object):
    def authenticate(self, username, password):    
        try:
            user = Account.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Account.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " % login)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = Account.objects.get(sys_id=user_id)
            if user.is_active:
                return user
            return None
        except Account.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)% not found")
            return None
