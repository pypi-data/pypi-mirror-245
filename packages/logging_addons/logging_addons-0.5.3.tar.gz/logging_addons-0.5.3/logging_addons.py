"""Add-ons for the logging standard library"""


import dataclasses
import logging
import sys
import threading
import time


__version__ = "0.5.3"

_programlevel_lock = threading.Lock()
"""A program level lock so that only 1 logging can run at a time"""


_recommended_alts = (
    'alt_logger',
)
"""List of alt names that are the defaults, if none is stated for `apply`"""

_all_alts = (
    'alt_logger',
    'HandlerDebugged',
    'GlobalLockedLogger',
)
"""List of all alt names that are available"""

_alt_statuses = {name: dict(applied=False) for name in _all_alts}
"""List of alt(s) has/have been applied"""


def callHandlers(self, record):
    """Special call handler overloading the standard one in Logger

    This is used to modify the logger propagation.

    The modification is that ancestor loggers are checked the same way as the
    log record creating logger. I.e. disabled loggers or loggers with higher
    minimum log levels than the log record stop the propagation. Also, filters
    attached to the ancestor loggers are called and their result can stop the
    propagation, too.

    The code is the same outside of the modification, but more commented and
    verbose than the original.
    
    Args:
        record (logging.LogRecord): the LogRecord to be handled
    """
    # The currently checked logger in the tree, start from this
    currentlogger = self
    # Indicate that no handler has been found yet
    found = False
    
    # Loop on all loggers up in the logger tree
    while currentlogger:
        # Loop on all handlers of the current logger
        for hdlr in currentlogger.handlers:
            #Indicate that at least one handler found
            found = True
            
            # Level in the LogRecord at least the level of the handler?
            if record.levelno >= hdlr.level:
                hdlr.handle(record)
        
        # Propagation not allowed from this logger upward?
        if not currentlogger.propagate:
            break
        else:
            # Set the current logger to the parent of the one we just processed
            currentlogger = currentlogger.parent
            
            ######################################
            ## Here comes the modification
            ######################################
            # Propagation is now broken in the following situations:
            # 0) if there is no parent logger (same as standard, obviously)
            # 1) if the parent logger is disabled
            # 2) if the LogRecord level is lower than the parent logger level
            # 3) if any of the filters attached to the parent logger fails
            if (
                not currentlogger
                or
                currentlogger.disabled
                or
                record.levelno < currentlogger.level
                or
                not currentlogger.filter(record)
            ):
                break
            ######################################
            ## End of modification
            ######################################
    
    # No any handler found in the whole logger tree?
    if not found:
        # lastResort was introduced in Python 3.2
        lastResort = logging.lastResort if hasattr(logging, 'lastResort') else False
        # lastResort exist?
        if lastResort:
            if record.levelno >= lastResort.level:
                lastResort.handle(record)
        # Exceptions wanted and no warning issued yet?
        elif logging.raiseExceptions and not self.manager.emittedNoHandlerWarning:
            # Emit the warning to the stderr
            sys.stderr.write('No handlers could be found for logger "%s"\n' % self.name)
            # Indicate that warning issued, don't repeat it later
            self.manager.emittedNoHandlerWarning = True


class NullHandlerWithFilter(logging.Handler):
    """The standard logging.NullHandler ignores filters
    
    Let's say you want to use a handler just to manipulate the LogRecord. Since
    you do not want it to emit anything you use a null handler. You still can
    add a filter to it. However, the stock logging.NullHandler really does
    nothing, i.e. it does not even invoke the attached filters.

    This may be annoying, as other handlers (maybe of other loggers) still need
    to use the manipulated LogRecord.

    This NullHandlerWithFilter invokes all filters as a standard handler, it
    just does not emit anything.
    """
    ######################################
    ## Here comes the patch (difference, compared to NullHandler)
    ## We prevent overloading the standard handle method, so that the LogRecord 
    ##   is passed through to the filters. Since locking is needed for the time
    ##   of filter execution, we prevent createLock overloading too.
    ######################################
    # def handle(self, record):
    #     pass

    # def createLock(self):
    #     self.lock = None
    ######################################
    ## End of modification
    ######################################

    def emit(self, _record):
        pass


class HandlerDebugged(logging.Handler):
    """Handler class to print debug info while handling a log record
    
    This can be useful for developers who use threads and want to see the sequence
    of logging actions, e.g. why log emitting is interleaved.
    
    Debug messages are printed to the STDOUT stating
    
    - the time stamp
    - the thread ID
    - the logger name
    - the handler class name
    - the action, i.e. whether the lock is being acquired, released or the log is being
        emitted or skipped
    - the log message itself
    """
    def handle(self, record):
        """Overloading the standard handle() method"""
        #do the filtering
        rv = self.filter(record)
        
        if rv:
            self._debug_printing('acquiring', record)  ##patch
            self.acquire()
            try:
                ##patch start
                self._debug_printing('emitting', record)
                if 'DumpHandler' in self.__class__.__name__ and record.levelno>=logging.INFO:
                    import time
                    #make the dump handler wait so that logging collision can be reproduced
                    time.sleep(2)
                ##patch end
                self.emit(record)
            finally:
                self._debug_printing('releasing', record)  ##patch
                self.release()

        else:  ##patch
            self._debug_printing('skipped', record)  ##patch
        
        return rv


    def _debug_printing(self, action, record):
        """Private method for HandlerDebugged"""
        import threading
        import time
        print(
            f'{time.time():.6f} {threading.get_ident():06d}'
                f' {record.name}/{self.__class__.__name__}/{action} "{record.msg}"'[:78],
            flush=True
        )


class SimpleFilter(logging.Filter):
    """Conveniency class for defining logging filters in config
    
    With SimpleFilter, you can provide the filtering in a one-liner or inside
    logging config files without the need of defining own filter classes.

    The filtering functionality is defined by providing the Python code body
    of either a lambda (filter_lambda) or a function (filter_func). This string
    is not to containing the lambda or function definition section, just the
    pure body. Any (e.g. syntax error) exception bubbles up to the caller
    (usually during logging configuration). The body code can suppose that the
    logging.LogRecord is available in the "record" variable.

    `filter_lambda` must be a single expression that resolves to a bool-like.
    E.g. the usage example below allows logging messages that contain the
    string "this". Other messages are filtered out.

    `filter_func` can be used for more complex filtering, even modifying the
    LogRecord content. NB, the relative indentation inside the code matters,
    so if it has more lines, the 1st line provides the base identation. Do not
    forget the "return", as the default "return None" filters out everything.
    The usage example below appends "-extra" to the logging messages.

    Usage in the main code:
        logger.addFilter(SimpleFilter(filter_lambda='"this" in record.msg'))
        logger.addFilter(SimpleFilter(filter_func='''
            record.msg += "-extra"
            return True
        '''))

    Or the same with YAML logging config:
        filters:
            only_if_this_in_msg:
                (): logging_alt.SimpleFilter
                filter_lambda: "this" in record.msg
            extend_with_extra:
                (): logging_alt.SimpleFilter
                filter_func: |-
                    record.msg += "-extra"
                    return True

    The usage examples above equal to the following more verbose code:
        class LambdaFilter(logging.Filter):
            def __init__(self):
                self.filter =  lambda record: "this" in record.msg
        class FuncFilter(logging.Filter):
            def filter(self, record):
                record.msg += "-extra"
                return True
        logger.addFilter(LambdaFilter())
        logger.addFilter(FuncFilter())
    
    Actually, the Logger.addFilter can accept a callable, i.e. we could pass a
    lambda, like logger.addFilter(lambda record: "this" in record.msg). The
    SimpleFilter is useful when the (body of) lambda is defined in a JSON, YAML
    or whatever config.
    """
    def __init__(self, filter_lambda = None, filter_func = None):
        if filter_lambda and filter_func:
            raise ValueError("Either filter_lambda or filter_func to be defined, not both")
        if not filter_lambda and not filter_func:
            raise ValueError("Either filter_lambda or filter_func to be defined")
        if filter_lambda:
            to_execute = f"self.filter=lambda record: {filter_lambda}"
        else:
            # Indent the function body
            filter_func_indented = "\n".join([" "+line for line in filter_func.split("\n")])
            to_execute = f"def filter(record):\n{filter_func_indented}\nself.filter = filter"
        try:
            exec(to_execute, globals(), locals())
        except Exception as e:
            raise Exception(f"{e}\nIn code:\n{to_execute}")
    
    def filter(self, record):
        raise NotImplementedError()


class GlobalLockedLogger(logging.Logger):
    """Wrap the LogRecord creation and handling into a lock"""
    def _log(self, *args, **kwargs):
        """Overload the low level log() method and only let one run at a time"""
        loggername = self.name
        with _programlevel_lock:
            print(
                f'{time.time():.6f} {threading.get_ident():06d} {loggername} log in'[:78],
                flush=True
            )
            time.sleep(2)
            super()._log(*args, **kwargs)
            time.sleep(2)
            print(
                f'{time.time():.6f} {threading.get_ident():06d} {loggername} log out'[:78],
                flush=True
            )


class RootLoggerGlobalLocked(GlobalLockedLogger):
    """RootLogger inherits the GlobalLockedLogger class instead of the hard-wired logging.Logger"""
    def __init__(self, level):
        super().__init__("root", level)
    def __reduce__(self):
        return logging.getLogger, ()


def _validate_patchlist(patchlist):
    if patchlist=="recommended":
        patchlist = _recommended_alts
    elif patchlist=="all":
        patchlist = _all_alts
    elif isinstance(patchlist, str):
        patchlist = patchlist.split(',')
    elif not isinstance(patchlist, (list, tuple)):
        raise TypeError(
            f'Argument must be str, list or tuple, but it is {type(patchlist)}'
        )
    return patchlist


@dataclasses.dataclass
class LoggingAlternative:
    patchlist: str = "recommended"
    def __enter__(self):
        enable(self.patchlist)
    def __exit__(self, t,e,b):
        disable()


def enable(patchlist="recommended"):
    """Enable the patch or alts
    
    Args:
        patchlist (optional list): the list of patch names to be enabled. By
            default, the recommended alts.
    """
    patchlist = _validate_patchlist(patchlist)

    # Loop on all the possible alts
    for patchname in patchlist:
        # Patch has alredy been enabled?
        if _alt_statuses[patchname]['enabled']:
            continue

        if patchname == 'alt_logger':
            # Get the active logger class, most probably the Logger
            active_logger_class = logging.getLoggerClass()
            # Save the originame method of the active logger class
            _alt_statuses[patchname]['saved_callHandlers'] = active_logger_class.callHandlers
            # Overwrite the method of the active logger class
            active_logger_class.callHandlers = callHandlers

        elif patchname == 'HandlerDebugged':
            # Overwrite the standard Handler class with HandlerDebugged
            logging.Handler = HandlerDebugged

        elif patchname == 'GlobalLockedLogger':
            # Overwrite the current Logger class with GlobalLockedLogger
            logging.setLoggerClass(GlobalLockedLogger)
            # Note that setLoggerClass() has no effect on the root logger because it was already
            # created when logging package was imported. We have to recreate the root logger,
            # now from the overloaded Logger class.
            root = logging.root = RootLoggerGlobalLocked(logging.WARNING)
            logging.Logger.root = root
            logging.Logger.manager = logging.Manager(root)

        else:
            raise ValueError(f'Unknown patch name: {patchname}')

        # Mark this patch enabled
        _alt_statuses[patchname]['enabled'] = True

def disable():
    """Disable all patch or alts, i.e. restore original behaviour"""
    for patchname, patchinfo in _alt_statuses.items():
        # not enabled?
        if not patchinfo['enabled']:
            continue

        if patchname == 'alt_logger':
            # Get the active logger class, most probably the Logger
            active_logger_class = logging.getLoggerClass()
            # Restore the original method of the active logger class
            active_logger_class.callHandlers = patchinfo['saved_callHandlers']
            # Mark this patch disabled
            patchinfo['enabled'] = False

        if patchname == 'NullHandlerWithFilter':
            # Coming ...
            raise NotImplementedError()

        if patchname == 'HandlerDebugged':
            # Coming ...
            raise NotImplementedError()

        if patchname == 'GlobalLockedLogger':
            # Coming ...
            raise NotImplementedError()
