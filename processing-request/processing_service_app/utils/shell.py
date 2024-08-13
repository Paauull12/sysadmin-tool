"""
This module implements shell execution.
"""
import logging

from pathlib import Path
from subprocess import run as subprocess_run, list2cmdline, CompletedProcess, CalledProcessError, PIPE

logger = logging.getLogger(__name__)


def run(args, *, accepted_non_zero_exit_codes=None, **kwargs):
    """
    Run the command given by args.

    Like the :py:func:`subprocess.check_output` original function, if the return code was non-zero it raises a
    :py:class:`subprocess.CalledProcessError`. However, some non-zero return codes can be accepted by declaring them
    through the ``accepted_non_zero_exit_codes`` parameter.

    Standard :py:func:`subprocess.run` function parameters can also be passed to the function.

    If the ``stdout`` parameter is not redefined, the ``subprocess.PIPE`` value will be used.

    If the ``stderr`` parameter is not redefined, the ``subprocess.PIPE`` value will be used.

    >>> run(["ls", "/path/found"])
    CompletedProcess(args=['ls', '/path/found'], returncode=0, stdout=b'file.txt')

    >>> run(["ls", "/path/not/found"])
    subprocess.CalledProcessError: Command '['ls', '/path/not/found']' returned non-zero exit status 2.

    >>> run(["ls", "/path/not/found"], accepted_non_zero_exit_codes=[2]})
    CompletedProcess(args=['ls', '/path/not/found'], returncode=2, stdout=b'')

    :param list args: Arguments defining the command to run.
    :param list accepted_non_zero_exit_codes: List of accepted non-zero exit code.
    :param kwargs: Arguments defined by the :py:func:`subprocess.run`.
    :return: Command output.
    :rtype: CompletedProcess
    :raise CalledProcessError: If the return code is non-zero and not in the accepted returned code defined by the
        parameter ``accepted_non_zero_exit_codes``.
    """
    # Log arguments
    args_to_log = [str(arg) if isinstance(arg, Path) else arg for arg in args]
    logger.info("Shell run: %(args)s", {"args": list2cmdline(args_to_log)})
    # run the command
    if "stdout" not in kwargs:
        kwargs["stdout"] = PIPE
    if "stderr" not in kwargs:
        kwargs["stderr"] = PIPE
    if "check" not in kwargs:
        kwargs["check"] = False  # It's recommended to explicitly set the check argument of subprocess.run
    # pylint: disable=subprocess-run-check
    returned_process: CompletedProcess = subprocess_run(args, **kwargs)
    if (returned_process.returncode != 0 and
            (not accepted_non_zero_exit_codes or returned_process.returncode not in accepted_non_zero_exit_codes)):
        logger.error(
            "Command failed with return code: %(returncode)d\nstdout:\n%(stdout)s\nstderr:\n%(stderr)s",
            {"returncode": returned_process.returncode,
             "stdout": returned_process.stdout,
             "stderr": returned_process.stderr}
        )
        raise CalledProcessError(returned_process.returncode, returned_process.args,
                                 output=returned_process.stdout, stderr=returned_process.stderr)
    logger.debug("Shell return: %(stdout)s", {"stdout": returned_process.stdout})
    return returned_process