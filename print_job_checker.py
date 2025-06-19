import subprocess
import logging
from utils import is_windows
if is_windows():
    import win32print

def print_job_checker(printer_name=None):
    """
    Returns True if there is still a print job in queue.
    If a printer name is specified, all other printer queues are skipped.
    """
    if is_windows():
        return print_job_checker_windows(printer_name)    
    else:
        return print_job_checker_linux(printer_name)


def is_printer_out_of_paper(printer_name=None):
    if is_windows():
        return False  # TODO implement
    else:
        return is_printer_out_of_paper_linux(printer_name)


def enable_printer(printer_name):
    if is_windows():
        return True  # TODO implement
    else:
        return enable_printer_linux(printer_name)


def is_printer_out_of_paper_linux(printer_name):
    if printer_name:
        printer_status_cmd = ['lpstat', '-p', printer_name]  # get status of printer
    else:
        printer_status_cmd = ['lpstat', '-p']

    result = subprocess.run(printer_status_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

    if "invalid" in result:
        logging.error(f"Given printer name is invalid or other error: {result}")

    if "No Paper" in result:
        return True

    return False


def enable_printer_linux(printer_name):
    if printer_name is None:
        logging.error(f"Printer cannot be enabled due to printer name is None")
        return False

    enable_printer_cmd = ['cupsenable', printer_name]

    result = subprocess.run(enable_printer_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

    if "failed" in result:
        logging.error(f"Given printer name {printer_name} is invalid or other error: {result}")
        return False

    if result == "":
        return True

    logging.error(f"Unhandled response while trying to enable printer {printer_name}: {result}")
    return False




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
