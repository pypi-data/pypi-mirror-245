from datetime import datetime
import utc_to_swedish_time

class LogLevel:
    NONE = 0
    INFO = 1
    ERROR = 2
    DEBUG = 3

class ConsoleColor:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

class Logger:
    def __init__(self, log_level: LogLevel = LogLevel.INFO):
        self.log_level = log_level

    def info(self, message):
        if not self.is_log_level(LogLevel.INFO):
            return
        self.print_with_color(f"{self.get_timestamp()} INFO: {message}")

    def error(self, message):
        if not self.is_log_level(LogLevel.ERROR):
            return
        self.print_with_color(f"{self.get_timestamp()} ERROR: {message}", ConsoleColor.RED)

    def debug(self, message):
        if not self.is_log_level(LogLevel.DEBUG):
            return
        self.print_with_color(f"{self.get_timestamp()} DEBUG: {message}", ConsoleColor.BLUE)

    def get_timestamp(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = utc_to_swedish_time.convert(timestamp)
        return f"[{timestamp}]"
    
    def print_with_color(self, message, color: ConsoleColor = ConsoleColor.RESET):
        print(f"{color}{message}{ConsoleColor.RESET}")
    
    def is_log_level(self, log_level):
        return self.log_level >= log_level
