"""
Contains the class `Hindent`. Import and use this class to format and execute Scheme code.

Usage:
    >>> from hindent import Hindent
    >>> Hindent.initialize(
    ...     # args here
    ... )
    >>> output, error = Hindent.run()
    >>> print(output)
"""

__version__ = "2.0.0"

from pathlib import Path
import os
import subprocess


_SAVED_FILE_SCM = "SAVED_FILE.scm"


# This class is just for type hinting for a function/callback
class LispExecutor:
    """
    A callback function type that executes Lisp (Scheme) code from a given filename.

    This is intended to be used as a function type for custom executors, with a default
    implementation using Chez Scheme.

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

    >>> def execute_scheme_code(filename):
    ...     # For Chez Scheme, the command is typically 'scheme --script'
    ...     process = subprocess.run(['chez', '--script', filename], capture_output=True, text=True)
    ...     return process.stdout, process.stderr
    """


def _default_lisp_executor(filename):
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


class Hindent:
    """
    A class for handling Hindent syntax for Lisp code. Provides methods to initialize the
    environment, run Lisp code from a file or a string, and to transpile Hindent syntax to Lisp.

    Use `Hindent.initialize` to configure the environment, and then use `Hindent.run`,
    `Hindent.run_file`, or `Hindent.run_string` to execute Hindent code.

    Heads up
    --------
     
    When running, the `newline` and `display` functions
    are helpful.  If you don't use `display`, then lisp will not output
    anything. So, if you are experimenting, and you want to see results
    of what you run, you need to use `display`.
    And regarding `newline`, if you don't use it, all of the output will be smushed
    together.

    Examples
    --------

    >>> # from hindent import Hindent
    >>> # Hindent.initialize()
    >>> # Hindent.run()

    Other usage
    -----------

    This class can also be used as a transpiler to convert Hindent code to Scheme code.
    Use `Hindent.transpile`, `Hindent.transpile_file`, or `Hindent.transpile_string` to
    transpile Hindent code to Scheme code.

    It can also simply be used as a lisp executor by using `Hindent.execute_lisp`.
    This can be helpful if you've already transpiled Hindent code to Scheme code and
    just want to execute it.
    """

    @classmethod
    def initialize(
        cls,
        file_path: Path = Path("./first.hin"),
        lisp_executor: LispExecutor = _default_lisp_executor,
    ):
        """
        Initializes the Hindent environment with a specified file and Lisp executor.

        Parameters
        ----------

        file_path : Path
            The file path of the Hindent code to be formatted and executed.
        lisp_executor : LispExecutor
            The executor function to run the Lisp code. Defaults to `_default_lisp_executor` using Chez Scheme.

        Examples
        --------

        >>> # import Hindent
        >>> from pathlib import Path
        >>> Hindent.initialize(
        ...     Path('./example_hindent_code.hin'),
        ... )
        >>> # then do Hindent.run()


        Using Something Other Than Chez Scheme
        --------------------------------------

        If you want to use something other than Chez Scheme, you can do so by
        passing a different function to ``Hindent.initialize``. This function
        should take a filename as a parameter and return a tuple of the output
        and error of the execution.
        """

        cls._file_path = file_path
        cls._lisp_executor = lisp_executor

    @classmethod
    def run(cls) -> tuple:
        """
        Executes and retrieves the output of Lisp code from the initialized file.

        Returns
        -------
        tuple
            A tuple containing the standard output and standard error from the executed Lisp code.

        Examples
        --------

        >>> # import and initialize Hindent
        >>> output, error = Hindent.run()
        >>> print(output)
        some output
        """
        return Hindent.run_string(
            Hindent._get_text_from_file_path(cls._file_path),
        )

    @classmethod
    def run_file(cls, file_path: Path) -> tuple:
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

        >>> # import and initialize Hindent
        >>> file_path = Path('./example_hindent_code.hin')
        >>> output, error = Hindent.run_file(file_path)
        >>> print(output)
        some output
        """
        return Hindent.run_string(
            Hindent._get_text_from_file_path(file_path),
        )

    @classmethod
    def run_string(cls, hindent_code: str) -> tuple:
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

        >>> # import and initialize Hindent
        >>> hindent_code = (
        ...     "display\\n"
        ...     "  2\\n"
        ...     ""
        ... )
        >>> output, error = Hindent.run_string(hindent_code)
        >>> print(output)
        some output
        """

        # Add parentheses with the fixed function and return the result
        parenthesized_code_fixed = Hindent.transpile_string(hindent_code)

        # Example usage
        output, error = Hindent.execute_lisp(parenthesized_code_fixed)

        return output, error

    @classmethod
    def transpile(cls) -> str:
        """
        Transpiles Hindent code from the initialized file to Scheme code.

        This method reads the Hindent code from the file specified during initialization,
        transpiles it to Scheme code by adding appropriate parentheses based on indentation,
        and returns the transpiled Scheme code.

        Returns
        -------
        str
            The transpiled Scheme code.

        Examples
        --------
        >>> Hindent.initialize(Path('./example.hin'))
        >>> scheme_code = Hindent.transpile()
        >>> print(scheme_code)
        """
        return Hindent.transpile_string(
            Hindent._get_text_from_file_path(cls._file_path),
        )

    @staticmethod
    def transpile_file(file_path: Path) -> str:
        """
        Transpiles Hindent code from a specified file to Scheme code.

        This method reads the Hindent code from the given file, transpiles it to Scheme code
        by adding appropriate parentheses based on indentation, and returns the transpiled
        Scheme code.

        Parameters
        ----------
        file_path : Path
            The path to the file containing the Hindent code to be transpiled.

        Returns
        -------
        str
            The transpiled Scheme code.

        Examples
        --------
        >>> file_path = Path('./example.hin')
        >>> scheme_code = Hindent.transpile_file(file_path)
        >>> print(scheme_code)
        """
        return Hindent.transpile_string(
            Hindent._get_text_from_file_path(file_path),
        )

    @staticmethod
    def transpile_string(hindent_code: str) -> str:
        """
        Transpiles Hindent code to Scheme code by adding appropriate parentheses based on indentation.

        This method processes Hindent code, which uses indentation to denote structure,
        and converts it to valid Scheme code by adding parentheses according to the
        indentation levels.

        Parameters
        ----------
        code : str
            The Hindent code to be transpiled.

        Returns
        -------
        str
            The transpiled Scheme code.

        Examples
        --------
        >>> hindent_code = (
        ...     "display\\n"
        ...     "  2\\n"
        ...     ""
        ... )
        >>> scheme_code = Hindent.transpile(hindent_code)
        >>> print(scheme_code)
        """

        # Split the code into lines
        lines = hindent_code.split("\n")

        validlines = []

        in_code_block = True

        for i, line in enumerate(lines):

            # Handle code blocks
            if line.rstrip() == ".":
                in_code_block = not in_code_block
                continue

            if not in_code_block:
                continue

            # Handle blank lines or lines with only whitespace (except the last line)
            # guard clause to exit early if the line is whitespace or a comment
            if line.strip() == "" or line.strip()[0] == ";":
                continue

            validlines.append(line)

        validlines.append("\n")  # Add a newline to the end

        # Function to calculate the indentation level of a line
        def indentation_level(line):
            return (len(line) - len(line.lstrip())) // 2

        # Process each line
        processed_lines = []

        for i, line in enumerate(validlines[:-1]):

            # Calculate the current and next line's indentation levels
            current_indent = indentation_level(line)
            next_indent = indentation_level(validlines[i + 1])

            # Determine the required parentheses
            if next_indent > current_indent:
                line = "(" + line
            elif next_indent < current_indent:
                line += ")" * (current_indent - next_indent)

            # Special case: same indentation level
            if next_indent == 0 and current_indent == 0:
                line = "(" + line + ")"

            processed_lines.append(line)

        # Join the processed lines
        return "\n".join(processed_lines)

    @staticmethod
    def _save_code_to_file(code, filename):
        with open(filename, "w") as file:
            file.write(code)

    @classmethod
    def execute_lisp(cls, lisp_code: str) -> tuple:
        """
        Executes the given Scheme code after saving it to a temporary file.

        This method is used internally to execute Scheme code. It saves the provided
        Scheme code to a temporary file, executes the file using the configured Lisp executor,
        and then deletes the file.

        Parameters
        ----------
        parenthesized_code_fixed : str
            The Scheme code to be executed.

        Returns
        -------
        tuple
            A tuple containing the standard output and standard error from the executed Scheme code.
        """

        Hindent._save_code_to_file(lisp_code, _SAVED_FILE_SCM)
        output, error = cls._lisp_executor(_SAVED_FILE_SCM)

        # delete file
        os.remove(_SAVED_FILE_SCM)
        return output, error

    @staticmethod
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
        >>> file_path = Path('./example.hin')
        >>> content = Hindent._get_text_from_file_path(file_path)
        >>> print(content)
        """
        file_path = Path(file_path)

        input_code = file_path.read_text()
        return input_code
