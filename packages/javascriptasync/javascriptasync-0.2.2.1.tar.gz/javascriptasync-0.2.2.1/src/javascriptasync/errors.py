import re
import sys
import traceback
import asyncio
from .core.abc import BaseError
from .core.jslogging import logs, log_error
from typing import List, Optional, Tuple
from .util import haspackage


class JavaScriptError(Exception):
    """
    Custom exception class for JavaScript errors.
    """

    def __init__(self, call: str, jsStackTrace: List[str], *args, **kwargs):
        """
        Initialize a JavaScriptError object.

        Args:
            call (str): The failed JavaScript call.
            jsStackTrace (List[str]): JavaScript stack trace.
        """
        
        super().__init__(*args, **kwargs)  # Assuming BaseError is the base class of JavaScriptError
        self.call = call
        self.js = jsStackTrace


    def get_error_message(self):
        return getErrorMessage(self.call, self.js, traceback.format_tb( self.__traceback__))
    
    def __str__(self):
        return self.get_error_message()
    
    def __repr__(self):
        return str(self)
    


class NoAsyncLoop(BaseError):
    """
    Raised when calling @On when the passed in handler is an async function
    And no event loop was passed into the args
    """
    
class NoPyiAction(BaseError):
    """
    Raised when PYI does not have a given set action in PYI.
    
    """



class NoConfigInitalized(BaseError):
    """
    Raised if there was no JSConfig initalized.
    """


class InvalidNodeJS(BaseError):
    """
    Raised if node.js was either not installed or is unreachable.

    """

class InvalidNodeOp(BaseError):
    """
    Raised if a NodeOp is invalid

    """
class AsyncReminder(BaseError):
    """
    Raised if an syncrounous magic method was called in amode

    """


class BridgeTimeout(TimeoutError):
    """
    Raised if a request times out.
    """

    def __init__(self, message, action, ffid, attr):
        self.message = message
        self.action = action
        self.ffid = ffid
        self.attr = attr

class BridgeTimeoutAsync(asyncio.TimeoutError):
    """
    Raised if a request times out in async mode
    """

    def __init__(self, message, action, ffid, attr, *args, **kwargs):
        super.__init__(*args,**kwargs)
        self.message = message
        self.action = action
        self.ffid = ffid
        self.attr = attr
class Chalk:
    """
    Chalk class for text coloring.
    """

    def red(self, text):
        return "\033[91m" + text + "\033[0m"

    def blue(self, text):
        return "\033[94m" + text + "\033[0m"

    def green(self, text):
        return "\033[92m" + text + "\033[0m"

    def yellow(self, text):
        return "\033[93m" + text + "\033[0m"

    def bold(self, text):
        return "\033[1m" + text + "\033[0m"

    def italic(self, text):
        return "\033[3m" + text + "\033[0m"

    def underline(self, text):
        return "\033[4m" + text + "\033[0m"

    def gray(self, text):
        return "\033[2m" + text + "\033[0m"

    def bgred(self, text):
        return "\033[41m" + text + "\033[0m"

    def darkred(self, text):
        return "\033[31m" + text + "\033[0m"

    def lightgray(self, text):
        return "\033[37m" + text + "\033[0m"

    def white(self, text):
        return "\033[97m" + text + "\033[0m"


chalk = Chalk()


def format_line(line: str) -> str:
    """
    Format a line of code with appropriate colors.

    :param line: The code line to be formatted.
    :return: Formatted code line.
    """
    if line.startswith("<") or line.startswith("\\"):
        return line
    statements = [
        "const ",
        "await ",
        "import ",
        "let ",
        "var ",
        "async ",
        "self ",
        "def ",
        "return ",
        "from ",
        "for ",
        "raise ",
        "try ",
        "except ",
        "catch ",
        ":",
        "\\(",
        "\\)",
        "\\+",
        "\\-",
        "\\*",
        "=",
    ]
    secondary = ["{", "}", "'", " true", " false"]
    for statement in statements:
        exp = re.compile(statement, re.DOTALL)
        line = re.sub(exp, chalk.red(statement.replace("\\", "")) + "", line)
    for second in secondary:
        exp = re.compile(second, re.DOTALL)
        line = re.sub(exp, chalk.blue(second) + "", line)
    return line


def print_error(
    failedCall: str,
    jsErrorline: str,
    jsStackTrace: List[str],
    jsErrorMessage: str,
    pyErrorline: str,
    pyStacktrace: List[Tuple[str, str]],
) -> List[str]:
    """
    Print JavaScript error details with formatted stack traces.

    :param failedCall: The failed JavaScript call.
    :param jsErrorline: JavaScript error line.
    :param jsStackTrace: JavaScript stack trace.
    :param jsErrorMessage: JavaScript error message.
    :param pyErrorline: Python error line.
    :param pyStacktrace: Formatted Python stack trace.
    :return: List of formatted lines to be printed.
    """
    lines = []
    log = lambda *s: lines.append(" ".join(s))
    log(
        "NodeJS",
        chalk.bold(chalk.bgred(" JavaScript Error ")),
        f"Call to '{failedCall.replace('~~', '')}' failed:",
    )

    log("[Context: Python]")
    for at, line in pyStacktrace:
        if "javascriptasync" in at or "IPython" in at:
            continue
        if not line:
            log(" ", chalk.gray(at))
        else:
            log(chalk.gray(">"), format_line(line))
            log(" ", chalk.gray(at))

    log(chalk.gray(">"), format_line(pyErrorline))

    log("\n[Context: NodeJS]\n")

    for traceline in reversed(jsStackTrace):
        log(" ", chalk.gray(traceline))

    log(chalk.gray(">"), format_line(jsErrorline))
    log("Bridge", chalk.bold(jsErrorMessage))

    return lines


def processPyStacktrace(stack):
    lines = []
    error_line = ""
    stacks = stack

    for lin in stacks:
        lin = lin.rstrip()
        if lin.startswith("  File"):
            tokens = lin.split("\n")
            lin = tokens[0]
            Code = tokens[1] if len(tokens) > 1 else chalk.italic("<via standard input>")
            fname = lin.split('"')[1]
            line = re.search(r"\, line (\d+)", lin).group(1)
            at = re.search(r"\, in (.*)", lin)
            if at:
                at = at.group(1)
            else:
                at = "^"
            lines.append([f"at {at} ({fname}:{line})", Code.strip()])
        elif lin.strip():
            error_line = lin.strip()

    return error_line, lines


INTERNAL_FILES = ["bridge.js", "pyi.js", "errors.js", "deps.js", "test.js"]


def isInternal(file):
    for f in INTERNAL_FILES:
        if f in file:
            return True
    return False


def processJsStacktrace(stack, allowInternal=False):
    lines = []
    message_line = ""
    error_line = ""
    found_main_line = False
    # print("Allow internal", allowInternal)
    stacks = stack if (type(stack) is list) else stack.split("\n")
    for line in stacks:
        if not message_line:
            message_line = line
        if allowInternal:
            lines.append(line.strip())
        elif (not isInternal(line)) and (not found_main_line):
            abs_path = re.search(r"\((.*):(\d+):(\d+)\)", line)
            file_path = re.search(r"(file:\/\/.*):(\d+):(\d+)", line)
            base_path = re.search(r"at (.*):(\d+):(\d+)$", line)
            if abs_path or file_path or base_path:
                path = abs_path or file_path or base_path
                fpath, errorline, char = path.groups()
                if fpath.startswith("node:"):
                    continue
                with open(fpath, "r") as f:
                    flines = f.readlines()
                    error_line = flines[int(errorline) - 1].strip()
                lines.append(line.strip())
                found_main_line = True
        elif found_main_line:
            lines.append(line.strip())

    if allowInternal and not error_line:
        error_line = "^"
    if error_line:
        return (error_line, message_line, lines)
    return None


def getErrorMessage(failed_call, jsStackTrace, pyStacktrace):
    try:
        tuple_a = processJsStacktrace(jsStackTrace)
        if tuple_a is None:
            tuple_a = processJsStacktrace(jsStackTrace, True)
        (jse, jsm, jss) = tuple_a
        pye, pys = processPyStacktrace(pyStacktrace)

        lines = print_error(failed_call, jse, jss, jsm, pye, pys)
        return "\n".join(lines)
    except Exception as e:
        print("Error in exception handler")
        import traceback

        print(e)
        pys = "\n".join(pyStacktrace)
        print(f"** JavaScript Stacktrace **\n{jsStackTrace}\n** Python Stacktrace **\n{pys}")
        return ""


# Custom exception logic

# Fix for IPython as it blocks the exception hook
# https://stackoverflow.com/a/28758396/11173996
# try:
#     # __IPYTHON__
#     if haspackage("IPython"):
#         import IPython

#         oldLogger = IPython.core.interactiveshell.InteractiveShell.showtraceback

#         def newLogger(*a, **kw):
#             ex_type, ex_inst, tb = sys.exc_info()
#             if ex_type is JavaScriptError:
#                 pyStacktrace = traceback.format_tb(tb)
#                 # The Python part of the stack trace is already printed by IPython
#                 print(getErrorMessage(ex_inst.call, ex_inst.js, pyStacktrace))
#             else:
#                 oldLogger(*a, **kw)

#         IPython.core.interactiveshell.InteractiveShell.showtraceback = newLogger
# except ImportError:
#     pass

# orig_excepthook = sys.excepthook


# def error_catcher(error_type, error, error_traceback):
#     """
#     Catches JavaScript exceptions and prints them to the console.
#     """
#     logs.error("ERROR.")
#     #print("TRACE:", traceback.format_exc())
#     #if error_type is JavaScriptError:        error.py=error_traceback
#     orig_excepthook(error_type, error, error_traceback)


#sys.excepthook = error_catcher
# ====
