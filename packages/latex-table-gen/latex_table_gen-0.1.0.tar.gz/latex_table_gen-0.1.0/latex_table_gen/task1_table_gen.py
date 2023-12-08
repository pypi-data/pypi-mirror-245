import textwrap
from typing import Any, Optional, TypeVar

T = TypeVar('T')


def get_at(lst: list[T], idx: int, default: T) -> T:
    return lst[idx] if 0 <= idx < len(lst) else default


def gen_latex_table(data: list[list[Any]]) -> Optional[str]:
    if not data or not data[0]:
        return None

    row_size = len(data[0])
    header_align = f"|{'|'.join('c' for _ in range(row_size))}|"

    hline = "\\hline \n"
    line_separator = r" \\ " + hline

    table_body = hline + line_separator.join(
        ' & '.join(map(lambda idx: str(get_at(row, idx, "")), range(row_size)))
        for row in data
    ) + line_separator

    return textwrap.dedent(
        r"""
        \begin{table}[]
        \begin{tabular}
        """
    ) + f"{{{header_align}}}" + table_body + textwrap.dedent(
        r"""
        \end{tabular}
        \end{table}
        """
    )



if __name__ == '__main__':
    print(gen_latex_table([
        ["str", "number", "bool or None", "sometimes empty"],
        ["foo", 123, None, ],
        ["bar", 123, True, "sometimes not"],
    ]))
