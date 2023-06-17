import sys 
import logging 
import json

class JsonFormatter(logging.Formatter):
    def __init__(self,fmt_dict: dict = None,task_index=0,time_format: str = "%Y-%m-%dT%H:%M:%S",msec_format: str = "%s:%03dZ"):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message":"message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None
        self.task_index = task_index
    
    def usesTime(self) -> bool:
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self,record) -> dict:
        return {fmt_key: record.__dict__[fmt_val] for fmt_key,fmt_val in self.fmt_dict.items()}
    
    def format(self,record) -> str:
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record,self.datefmt)
        message_dict = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            
        if record.exc_text:
            message_dict["exc_info"] = record.exc_text
        
        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        message_dict["task_index"] = self.task_index
        return json.dumps(message_dict,default=str)


def set_logger(level,task_index):
    _LEVELS_={
        "DEBUG":logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR":logging.ERROR
    }

    logging_formattor = JsonFormatter(fmt_dict={
        "level":"levelname",
        "message":"message",
        "path":"pathname",
        "lineno":"lineno"
    },task_index=task_index)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARN)

    stdout_handler.setFormatter(logging_formattor)
    stderr_handler.setFormatter(logging_formattor)

    logger = logging.getLogger()
    logger.setLevel(_LEVELS_[level])
    logging.addHandler(stdout_handler)
    loggin.addHandler(stderr_handler)