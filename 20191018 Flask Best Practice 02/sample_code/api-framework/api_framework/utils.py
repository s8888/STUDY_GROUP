import os
import time
import base64
import codecs
import logging
from datetime import date
from logging.handlers import BaseRotatingHandler
from flask import request, has_request_context


class MultiProcessSafeDailyRotatingFileHandler(BaseRotatingHandler):
    """Similar with `logging.TimedRotatingFileHandler`, while this one is
    - Multi process safe
    - Rotate at midnight only
    - Utc not supported
    """

    def __init__(self, filename, encoding=None, delay=False, utc=False, **kwargs):
        self.utc = utc
        self.suffix = "%Y-%m-%d"
        self.baseFilename = filename
        self.currentFileName = self._compute_fn()
        BaseRotatingHandler.__init__(self, filename, "a", encoding, delay)

    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.currentFileName = self._compute_fn()

    def _compute_fn(self):
        return self.baseFilename + "." + time.strftime(self.suffix, time.localtime())

    def _open(self):
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = codecs.open(self.currentFileName, self.mode, self.encoding)
        # simulate file name structure of `logging.TimedRotatingFileHandler`
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream


def log_file_handler(log_dir, log_file_name):
    """log file handler separate at midnight, compatible with multi thread

    Arguments:
        log_dir {str} -- log file directory
        log_file_name {str} -- log file prefix
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    filehandler = MultiProcessSafeDailyRotatingFileHandler(
        os.path.join(log_dir, log_file_name),
        when="midnight",
        interval=1,
        encoding="utf-8",
    )
    formatter = req_id_log_formatter()
    filehandler.setFormatter(formatter)
    return filehandler


def req_id_log_formatter():
    """logging formatter with req_id
    """
    log_format = "%(asctime)s [%(process)d] [%(levelname)s] [%(req_id)s] %(message)s"
    return logging.Formatter(fmt=log_format, datefmt="[%Y-%m-%d %H:%M:%S %z]")


class ContextualFilter(logging.Filter):
    """Append X-Request-Id from header as req_id"""

    def filter(self, log_record):
        if has_request_context():
            log_record.req_id = request.headers.get("X-Request-Id", "")
        else:
            log_record.req_id = ""
        return True


def allowed_file(filename, allowed_extensions):
    """For a given file, return whether it's an allowed type or not (case insensitive)

    Arguments:
        filename {str} -- filename
        allowed_extensions {list of str} -- allowed extensions list
    """
    try:
        extension = filename.rsplit(".", 1)[1].lower()
    except Exception:
        return False
    return "." in filename and extension in allowed_extensions


def month_dir(base_dir):
    current_dir = os.path.join(base_dir, date.today().strftime("%Y-%m"))
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)
    return current_dir


def today_dir(base_dir):
    current_dir = os.path.join(base_dir, date.today().strftime("%Y-%m-%d"))
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)
    return current_dir


def back_file(file, filename, back_file_dir):
    """back up upload file to {back_file_dir}/YYYY-mm/YYYY-mm-dd/{filename}

    Arguments:
        file {werkzeug.datastructures.FileStorage or base64 string} -- file
        filename {string} -- back file name
        back_file_dir {string} -- back file root dir

    Returns:
        string -- back file path
    """
    current_dir = month_dir(back_file_dir)
    current_dir = today_dir(current_dir)
    file_path = os.path.join(current_dir, filename)
    if hasattr(file, "save"):
        # werkzeug.datastructures.FileStorage instance
        file.save(file_path)
    else:
        with open(file_path, "wb") as f:
            if isinstance(file, str):
                # base64 string
                f.write(base64.decodebytes(file.encode()))
    return file_path


class AppError(Exception):
    """Raise this when already known exception in app"""

    def __init__(self, message):
        super().__init__(message)
