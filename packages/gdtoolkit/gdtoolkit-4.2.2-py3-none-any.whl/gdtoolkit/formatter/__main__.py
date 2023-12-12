"""GDScript formatter

Uncompromising GDScript code formatter. The only configurable thing is
max line length allowed and tabs/spaces indent. The rest will be taken
care of by gdformat in a one, consistent way.

Usage:
  gdformat <path>... [options]

Options:
  -c --check                 Don't write the files back,
                             just check if formatting is possible.
  -d --diff                  Don't write the files back,
                             just suggest formatting changes
                             (implies --check).
  -f --fast                  Skip safety checks.
  -l --line-length=<int>     How many characters per line to allow.
                             [default: 100]
  -s --use-spaces=<int>      Use spaces for indent instead of tabs.
  -h --help                  Show this screen.
  --version                  Show version.

Examples:
  echo 'pass' | gdformat -   # reads from STDIN
"""
import sys
import difflib
from typing import List, Tuple, Optional
import pkg_resources

from docopt import docopt
import lark

from gdtoolkit.formatter import format_code, check_formatting_safety
from gdtoolkit.formatter.exceptions import (
    TreeInvariantViolation,
    FormattingStabilityViolation,
    CommentPersistenceViolation,
)
from gdtoolkit.parser import parser
from gdtoolkit.common.utils import find_gd_files_from_paths
from gdtoolkit.common.exceptions import (
    lark_unexpected_token_to_str,
    lark_unexpected_input_to_str,
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    arguments = docopt(
        __doc__,
        version="gdformat {}".format(
            pkg_resources.get_distribution("gdtoolkit").version
        ),
    )

    if arguments["--diff"]:
        arguments["--check"] = True

    line_length = int(arguments["--line-length"])
    spaces_for_indent = (
        int(arguments["--use-spaces"])
        if arguments["--use-spaces"] is not None
        else None
    )
    safety_checks = not arguments["--fast"]
    files: List[str] = find_gd_files_from_paths(
        arguments["<path>"], excluded_directories=set(".git")
    )

    if files == ["-"]:
        _format_stdin(line_length, spaces_for_indent, safety_checks)
    elif arguments["--check"]:
        _check_files_formatting(
            files, line_length, spaces_for_indent, arguments["--diff"], safety_checks
        )
    else:
        _format_files(files, line_length, spaces_for_indent, safety_checks)


def _format_stdin(
    line_length: int, spaces_for_indent: Optional[int], safety_checks: bool
) -> None:
    code = sys.stdin.read()
    success, _, formatted_code = _format_code(
        code, line_length, spaces_for_indent, "STDIN", safety_checks
    )
    if not success:
        sys.exit(1)
    print(formatted_code, end="")


# pylint: disable-next=too-many-locals
def _check_files_formatting(
    files: List[str],
    line_length: int,
    spaces_for_indent: Optional[int],
    print_diff: bool,
    safety_checks: bool,
) -> None:
    formattable_files = set()
    failed_files = set()
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                code = handle.read()
                success, actually_formatted, formatted_code = _format_code(
                    code, line_length, spaces_for_indent, file_path, safety_checks
                )
                if success and actually_formatted:
                    print(f"would reformat {file_path}", file=sys.stderr)
                    if print_diff:
                        print(
                            "\n".join(
                                difflib.unified_diff(
                                    code.splitlines(),
                                    formatted_code.splitlines(),
                                    file_path,
                                    file_path,
                                    lineterm="",
                                )
                            ),
                            file=sys.stderr,
                        )
                    formattable_files.add(file_path)
                elif not success:
                    failed_files.add(file_path)
        except OSError as exceptions:
            print(
                f"Cannot open file {file_path!r}: {exceptions.strerror}",
                file=sys.stderr,
            )
            failed_files.add(file_path)
    if len(formattable_files) == 0:
        print(
            "{} file{} would be left unchanged".format(
                len(files), "s" if len(files) != 1 else ""
            )
        )
        sys.exit(0 if len(failed_files) == 0 else 1)
    formattable_num = len(formattable_files)
    left_unchanged_num = len(files) - formattable_num
    print(
        "{} file{} would be reformatted, {} file{} would be left unchanged.".format(
            formattable_num,
            "s" if formattable_num != 1 else "",
            left_unchanged_num,
            "s" if left_unchanged_num != 1 else "",
        ),
        file=sys.stderr,
    )
    sys.exit(1)


def _format_files(
    files: List[str],
    line_length: int,
    spaces_for_indent: Optional[int],
    safety_checks: bool,
) -> None:
    formatted_files = set()
    failed_files = set()
    for file_path in files:
        try:
            with open(file_path, "r+", encoding="utf-8") as handle:
                code = handle.read()
                success, actually_formatted, formatted_code = _format_code(
                    code, line_length, spaces_for_indent, file_path, safety_checks
                )
                if success and actually_formatted:
                    print(f"reformatted {file_path}")
                    formatted_files.add(file_path)
                    handle.seek(0)
                    handle.truncate(0)
                    handle.write(formatted_code)
                elif not success:
                    failed_files.add(file_path)
        except OSError as exceptions:
            print(
                f"Cannot open file {file_path!r}: {exceptions.strerror}",
                file=sys.stderr,
            )
            failed_files.add(file_path)
    reformatted_num = len(formatted_files)
    left_unchanged_num = len(files) - reformatted_num
    print(
        "{} file{} reformatted, {} file{} left unchanged.".format(
            reformatted_num,
            "s" if reformatted_num != 1 else "",
            left_unchanged_num,
            "s" if left_unchanged_num != 1 else "",
        )
    )
    sys.exit(0 if len(failed_files) == 0 else 1)


def _format_code(
    code: str,
    line_length: int,
    spaces_for_indent: Optional[int],
    file_path: str,
    safety_checks: bool,
) -> Tuple[bool, bool, str]:
    success = True
    actually_formatted = False
    formatted_code = code

    try:
        code_parse_tree = parser.parse(code, gather_metadata=True)
        comment_parse_tree = parser.parse_comments(code)
        formatted_code = format_code(
            gdscript_code=code,
            max_line_length=line_length,
            spaces_for_indent=spaces_for_indent,
            parse_tree=code_parse_tree,
            comment_parse_tree=comment_parse_tree,
        )
        if formatted_code != code:
            actually_formatted = True
            if safety_checks:
                check_formatting_safety(
                    code,
                    formatted_code,
                    max_line_length=line_length,
                    spaces_for_indent=spaces_for_indent,
                    given_code_parse_tree=code_parse_tree,
                    given_code_comment_parse_tree=comment_parse_tree,
                )
    except lark.exceptions.UnexpectedToken as exception:
        success = False
        print(
            f"{file_path}:\n",
            lark_unexpected_token_to_str(
                exception, formatted_code if actually_formatted else code
            ),
            sep="\n",
            file=sys.stderr,
        )
    except lark.exceptions.UnexpectedInput as exception:
        success = False
        print(
            f"{file_path}:\n",
            lark_unexpected_input_to_str(exception),
            sep="\n",
            file=sys.stderr,
        )
    except TreeInvariantViolation:
        success = False
        print(
            f"{file_path}: Failed to format, formatted code parse tree differs",
            file=sys.stderr,
        )
    except FormattingStabilityViolation:
        success = False
        print(
            f"{file_path}: Failed to format, formatted code is unstable",
            file=sys.stderr,
        )
    except CommentPersistenceViolation:
        success = False
        print(
            f"{file_path}: Failed to format,",
            "some comments are missing in formatted code",
            sep="",
            file=sys.stderr,
        )
    return success, actually_formatted, formatted_code


if __name__ == "__main__":
    main()
