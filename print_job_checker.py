import win32print


def print_job_checker(printer_name=None):
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


if __name__ == "__main__":
    if print_job_checker("Canon SELPHY CP1500"):
        print("Still something in printer queue")
    else:
        print("Nothing in queue")
