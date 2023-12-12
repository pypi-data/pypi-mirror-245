"""
Provides functions to translate and/or execute Hindent code.

>>> import hindent as h
>>> h.run_file('./your-file.hin')

or

>>> import hindent as h
>>> hindent_code = '''
... display
...   2
... '''
>>> h.run_string(hindent_code)

Provided functions
------------------

run_file(file_path: Path)
    Executes and retrieves the output of Lisp code from a specified file.

run_string(hindent_code: str)
    Executes and retrieves the output of Lisp code from a given string.

translate_file(file_path: Path)
    Translates Hindent code from a specified file.

translate_string(hindent_code: str)
    Translates Hindent code by adding appropriate parentheses based on indentation.

execute_lisp(lisp_code: str)
    Executes the given lisp code.

Using a custom Lisp executor
----------------------------

The default Lisp executor uses clojure. However, you can
use a custom Lisp executor by setting the `lisp_executor` variable to a function
that takes a filename as input, executes the Lisp code in the file, and returns the
output and error of the execution as a tuple.
"""

__version__ = "4.0.0"

from pathlib import Path
import os
import subprocess


_SAVED_FILE_TXT = "SAVED_FILE.txt"


# This class is just for type hinting for a function/callback
class LispExecutor:
    """
    A callback function type that executes Lisp code from a given filename.

    This is intended to be used as a function type for custom executors.

    The function should take a filename as input, execute the Lisp code in the file, and
    return the output and error of the execution as a tuple.

    Parameters
    ----------
    filename : str
        The name of the file to execute.

    Returns
    -------

    tuple
        The output and error of the execution.

    Examples
    --------

    >>> def _clojure_executor(filename):
    ...     process = subprocess.run(
    ...         ["clojure", filename], capture_output=True, text=True
    ...     )
    ...     return process.stdout, process.stderr
    """


def _scheme_executor(filename):
    """
    Default executor function for executing Scheme code using Chez Scheme.

    This function executes Scheme code from a specified file using Chez Scheme, capturing
    and returning the standard output and standard error.

    Parameters
    ----------
    filename : str
        The path to the Scheme file to be executed.

    Returns
    -------
    tuple
        A tuple containing two elements: the standard output and standard error from the executed Scheme code.

    Examples
    --------
    >>> stdout, stderr = _default_lisp_executor("example.scm")
    >>> print(stdout)
    """

    # For Chez Scheme, the command is typically 'scheme --script'
    process = subprocess.run(
        ["chez", "--script", filename], capture_output=True, text=True
    )
    return process.stdout, process.stderr


def _clojure_executor(filename):
    """
    Executor function for executing Clojure code using Clojure.

    This function executes Clojure code from a specified file using Clojure, capturing
    and returning the standard output and standard error.

    Parameters
    ----------
    filename : str
        The path to the Clojure file to be executed.

    Returns
    -------
    tuple
        A tuple containing two elements: the standard output and standard error from the executed Clojure code.

    Examples
    --------
    >>> stdout, stderr = _clojure_executor("example.clj")
    >>> print(stdout)
    """

    # For Clojure, the command is typically 'clojure'
    process = subprocess.run(
        ["clojure", "-M", filename], capture_output=True, text=True
    )
    return process.stdout, process.stderr


lisp_executor: LispExecutor = _clojure_executor


def run_file(file_path: Path) -> tuple:
    """
    Executes and retrieves the output of Lisp code from a specified file.

    This method allows the user to run Lisp code from a file of their choice,
    rather than the default file set during initialization.

    Parameters
    ----------
    file_path : Path
        The path to the file containing the Hindent code to be formatted and executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed Lisp code.

    >>> import hindent as h
    >>> h.run_file('./example_hindent_code.hin')
    some output
    """
    return run_string(
        _get_text_from_file_path(file_path),
    )


def run_string(hindent_code: str) -> tuple:
    """
    Executes and retrieves the output of Lisp code from a given string.

    This method allows the user to run Lisp code directly from a string,
    enabling on-the-fly execution without needing to write to a file.

    Parameters
    ----------
    hindent_code : str
        The string containing the Hindent code to be formatted and executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed Lisp code.

    Examples
    --------

    >>> import hindent as h
    >>> hindent_code = '''
    ... display
    ...   2
    ... '''
    >>> h.run_string(hindent_code)
    some output
    """

    # Add parentheses with the fixed function and return the result
    parenthesized_code_fixed = translate_string(hindent_code)

    # Example usage
    output, error = execute_lisp(parenthesized_code_fixed)

    return output, error



def translate_file(file_path: Path) -> str:
    """
    Translates Hindent code from a specified file.

    This method reads the Hindent code from the given file, translates it
    by adding parentheses based on indentation, and returns the translated
    code.

    Parameters
    ----------
    file_path : Path
        The path to the file containing the Hindent code to be translated.

    Returns
    -------
    str
        The translated code.

    Examples
    --------
    >>> lisp_code = h.translate_file('./examples/example.hin')
    >>> print(lisp_code)
    """
    return translate_string(
        _get_text_from_file_path(file_path),
    )


def translate_string(hindent_code: str) -> str:
    """
    Translates Hindent code to lisp code by adding appropriate parentheses based on indentation.

    This method processes Hindent code, which uses indentation to denote structure,
    and converts it to valid lisp code by adding parentheses according to the
    indentation levels.

    Parameters
    ----------
    code : str
        The Hindent code to be translated.

    Returns
    -------
    str
        The translated lisp code.

    Examples
    --------
    >>> hindent_code = (
    ...     "display\\n"
    ...     "  2\\n"
    ...     ""
    ... )
    >>> lisp_code = h.translate_string(hindent_code)
    >>> print(lisp_code)
    """

    # Split the code into lines
    lines = hindent_code.split("\n")

    validlines = []

    in_code_block = True

    # remove comment blocks and whole line comments.
    for i, line in enumerate(lines):

        # Handle code/comment blocks
        if line.rstrip() == ",":
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            continue

        # We want to remove the comments, so we don't want to add them to the
        # list of valid lines, so we simply skip them with a continue statement/guard clause
        if line.strip().find(";") == 0:
            continue

        validlines.append(line)

    validlines.append("\n")  # Add a newline to the end to ensure the final outdent is correct

    # Function to calculate the indentation level of a line
    def indentation_level(line):
        return (len(line) - len(line.lstrip())) // 2

    # Process each line
    processed_lines = []

    for i, line in enumerate(validlines[:-1]):

        next_line = validlines[i + 1]

        # Remove any end-of-line comments
        line = _remove_potential_end_of_line_comment(line)

        # Calculate the current and next line's indentation levels
        current_indent = indentation_level(line)
        next_indent = indentation_level(next_line)

        # if a line starts with `. ` (or, in the case that a period is
        # the only thing on the line... some examples of use cases are in
        # the examples) then remove the period
        # after the indentation is calculated. This lets the user
        # use the period to modify the indentation level of a line.
        # an example is given in `examples/example.hin`.  This is also
        # used to evaluate functions that have no arguments.
        if line.strip() == "." or line.lstrip().find(". ") == 0:
            line = line.lstrip()[1:]

        # Determine the required parentheses
        if (
            # current line is totally blank with no indentation
            # or period
            (current_indent == 0 and line.strip() == "") and
            # the next line is anything but blank
            not (next_indent == 0 and next_line.strip() == "")
        ):
            line = " ( "
        if (
            # current line is anything but blank
            not (current_indent == 0 and line.strip() == "") and
            # next line is blank
            (next_indent == 0 and next_line.strip() == "")
        ):
            line = line + " ) "

        if next_indent > current_indent:
            line = line + (" ( "  * (next_indent - current_indent)) 
        elif next_indent < current_indent:
            line = line + (" ) " * (current_indent - next_indent))


        processed_lines.append(line)

    # Join the processed lines
    return "\n".join(processed_lines)


def _save_code_to_file(code, filename):
    with open(filename, "w") as file:
        file.write(code)


def execute_lisp(lisp_code: str) -> tuple:
    """
    Executes the given lisp code.

    Parameters
    ----------
    parenthesized_code_fixed : str
        The lisp code to be executed.

    Returns
    -------
    tuple
        A tuple containing the standard output and standard error from the executed lisp code.
    """

    _save_code_to_file(lisp_code, _SAVED_FILE_TXT)
    output, error = lisp_executor(_SAVED_FILE_TXT)

    print(output)
    print(error)

    # delete file
    os.remove(_SAVED_FILE_TXT)
    return output, error


def _get_text_from_file_path(file_path: Path) -> str:
    """
    Reads text from a file specified by the given file path.

    This utility method reads and returns the contents of the file at the specified path.

    Parameters
    ----------
    file_path : Path
        The path of the file to be read.

    Returns
    -------
    str
        The content of the file as a string.

    Examples
    --------
    >>> content = h._get_text_from_file_path('./examples/example.hin')
    >>> print(content)
    """
    file_path = Path(file_path)

    input_code = file_path.read_text()
    return input_code


def _remove_potential_end_of_line_comment(line: str) -> str:
    """
    Removes any end-of-line comments from a line of code.

    This method removes any end-of-line comments from a line of code, returning the
    line without the comment.

    We need to make sure that we don't remove comments from within strings.

    Parameters
    ----------
    line : str
        The line of code to be processed.

    Returns
    -------
    str
        The line of code without any end-of-line comments.

    Examples
    --------
    >>> line = "display 2 ; this is a comment"
    >>> line_without_comment = h.remove_potential_end_of_line_comment(line)
    >>> print(line_without_comment)
    display 2
    """

    in_string = False

    for i, char in enumerate(line):
        if char == '"':
            in_string = not in_string

        if char == ";" and not in_string:
            return line[:i]
    
    return line

            