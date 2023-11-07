import time


class Log:

    def warn(self, message):
        self.print("WARN", message)

    def error(self, message):
        self.print("ERROR", message)

    def info(self, message):
        self.print("INFO", message)

    def format(self, level, message):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        return f"{timestamp} [{level}] {message}"

    def print(self, level, message):
        formatted_message = self.format(level, message)
        print(formatted_message)
