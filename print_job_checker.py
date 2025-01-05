import subprocess
import logging
from utils import is_windows
if is_windows():
    import win32print

def print_job_checker(printer_name=None):
    if is_windows():
        return print_job_checker_windows(printer_name)    
    else:
        return print_job_checker_linux(printer_name)    

def print_job_checker_windows(printer_name):
    """
    Returns True if there is still a print job in queue.
    If a printer name is specified, all other printer queues are skipped.
    """

    jobs = []
    for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
        flags, desc, name, comment = p
        if printer_name is not None:
            if name != printer_name:
                continue  # Skip printer queue if printer name does not match with given one
        phandle = win32print.OpenPrinter(name)
        print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
        if print_jobs:
            jobs.extend(list(print_jobs))
        for job in print_jobs:
            print(f"printer name => {name}")
            document = job["pDocument"]
            print(f"Document name => {document}")
        win32print.ClosePrinter(phandle)
    if jobs:
        return True
    else:
        return False

def print_job_checker_linux(printer_name):
    """
    Returns True if there is still a print job in queue.
    If a printer name is specified, all other printer queues are skipped.
    """
    if printer_name:
        print_queue_cmd = ['lpstat', '-o', printer_name]
    else: 
        print_queue_cmd = ['lpstat', '-o']
    
    result = subprocess.run(print_queue_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

    if "invalid" in result:
        logging.error(f"Given printer name is invalid or other error: {result}")
    
    if result == "":
        return False
    
    print(f"print queue not empty: {result}")
    return True




if __name__ == "__main__":
    if print_job_checker("Canon_SELPHY_CP1500"):
        print("Still something in printer queue")
    else:
        print("Nothing in queue")
