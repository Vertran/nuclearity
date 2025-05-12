import time

log_path = r"c:\Games\nuclearity\nuclearity\sys\log.txt"

class Warn:
    amount = 0
    max = 20

def make_log(level="DEBUG", message="Debug", description=None, timestamp=None):
    if timestamp == None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"[{timestamp}] [{level}] {message}."
    if level in ['WARN', 'ERROR', 'FATAL']:
        if Warn.amount >= Warn.max:
            make_log('EXIT', f'Total error number reached: {Warn.amount}')
        Warn.amount += 1
    if description:
        log_entry += f" - {description}"
    log_entry += "\n"
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def search_errors():
    try:
        # Placeholder for code that might raise an error
        pass
    except Exception as e:
        make_log("ERROR", "An error occurred", description=str(e))
    

make_log("INFO", "LoggerSystem started successfully")