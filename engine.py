from lib.bruter import Bruter
from lib.const import credentials
from lib.display import Display


class Engine(object):
    def __init__(self, service, username, threads, passlist_path, is_color):
        self.bruter = None
        self.resume = False
        self.is_alive = True
        self.threads = threads
        self.service = service
        self.username = username
        self.passlist_path = passlist_path
        self.display = Display(is_color=is_color)

    def get_user_resp(self):
        return self.display.prompt('Would you like to resume the attack? [y/n]: ')

    def write_to_file(self, password):
        with open(credentials, 'at') as f:
            data = 'Service: {}\nUsername: {}\nPassword: {}\n\n'.format(self.service, self.username, password)
            f.write(data)

    def start(self):
        if not self.is_alive: return

        self.bruter = Bruter(
            self.service,
            self.username,
            self.threads,
            self.passlist_path
        )

        while self.is_alive and not self.bruter.password_manager.session: pass
        if not self.is_alive: return

        if self.bruter.password_manager.session.exists:
            try:
                resp = self.get_user_resp()
            except:
                self.is_alive = False

            if self.is_alive and resp.strip().lower() == 'y':
                self.bruter.password_manager.resume = True

        try:
            self.bruter.start()
        except KeyboardInterrupt:
            self.bruter.stop()
            self.bruter.display.shutdown(self.bruter.last_password,
                                         self.bruter.password_manager.attempts, len(self.bruter.browsers))
        finally:
            self.stop()

    def stop(self):
        if not self.is_alive: return

        self.bruter.stop()
        self.is_alive = False

        if self.bruter.password_manager.is_read and not self.bruter.is_found and not self.bruter.password_manager.list_size:
            self.bruter.display.stats_not_found(self.bruter.last_password, self.bruter.password_manager.attempts,
                                                len(self.bruter.browsers))

        if self.bruter.is_found:
            self.write_to_file(self.bruter.password)
            self.bruter.display.stats_found(self.bruter.password, self.bruter.password_manager.attempts,
                                            len(self.bruter.browsers))
