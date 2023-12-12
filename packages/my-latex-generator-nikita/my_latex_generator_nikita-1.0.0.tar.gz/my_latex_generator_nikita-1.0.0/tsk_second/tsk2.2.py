import enum
import textwrap
import typing


class LatexDocumentClasses(enum.Enum):
    article_key_val = '{article}'


class LatexPackages(enum.Enum):
    graphicx = 'graphicx'


class LatexSyntaxConstructions(enum.Enum):
    document_class = r'\documentclass'
    usepackage_key_val = r'\usepackage{{{package}}}'
    begin_key_val = r'\begin'
    document_key_val = '{document}'
    table_key_val = '{tabular}'
    cells_separator = '&'
    line_separator_key_val = r'\hline'
    end_key_val = r'\end'


class CellAlignVariants(enum.Enum):
    left = 'l'
    centre = 'c'
    right = 'r'


def _get_table_footer() -> str:
    table_footer_base = LatexSyntaxConstructions.table_key_val.value
    table_footer = (
            LatexSyntaxConstructions.end_key_val.value +
            table_footer_base
    )
    return table_footer


def _get_latex_table_content(
        rows_count: int, table_content_raw: typing.List[typing.List[str]]
) -> str:
    latex_table_content: str = ''
    for idx in range(rows_count):
        latex_table_content += (
                LatexSyntaxConstructions.line_separator_key_val.value + '\n'
        )
        latex_table_content += (
                f'{LatexSyntaxConstructions.cells_separator.value}'
                .join(table_content_raw[idx]) + r' \\' + '\n'
        )
    latex_table_content += (
        LatexSyntaxConstructions.line_separator_key_val.value
    )
    return latex_table_content


def _get_table_header(
        columns_count: int, cell_align: CellAlignVariants
) -> str:
    table_header_base = LatexSyntaxConstructions.table_key_val.value
    cell_aligns_header = ''.join(
        ['|' + str(cell_align.value) for _ in range(columns_count)]
    )
    cell_aligns_header += '|'
    table_header = (
            LatexSyntaxConstructions.begin_key_val.value +
            table_header_base +
            f"{{{cell_aligns_header}}}"
    )
    return table_header


def _get_latex_img() -> str:
    return textwrap.dedent(
        r"""
        \begin{figure}
        \centering
        \includegraphics[width=0.5\textwidth]{image.jpg}
        \caption{Пример картинки}
        \label{fig:example}
        \end{figure}
        """
    )


def _get_latex_table(table_content: typing.List[typing.List[str]]) -> str:
    columns_count: int = len(table_content[0])
    table_header: str = _get_table_header(
        columns_count=columns_count, cell_align=CellAlignVariants.centre
    )
    table_content: str = _get_latex_table_content(
        rows_count=len(table_content), table_content_raw=table_content
    )
    table_footer: str = _get_table_footer()
    return table_header + '\n' + table_content + '\n' + table_footer


def _get_latex_doc_req_headers() -> str:
    return (
            LatexSyntaxConstructions.document_class.value +
            LatexDocumentClasses.article_key_val.value + '\n' +
            LatexSyntaxConstructions.usepackage_key_val.value.format(
                package=LatexPackages.graphicx.value,
            ) + '\n'
    )

def get_latex_doc_content(
        table_content: typing.List[typing.List[str]]
) -> str:
    latex_doc_req_headers: str = _get_latex_doc_req_headers()
    latex_doc_prepared = ''
    latex_doc_prepared += latex_doc_req_headers
    latex_doc_prepared += (
            LatexSyntaxConstructions.begin_key_val.value +
            LatexSyntaxConstructions.document_key_val.value + '\n'
    )
    latex_table_content_prep: str = _get_latex_table(table_content)
    latex_img_content: str = _get_latex_img()
    latex_doc_prepared += (
            latex_table_content_prep +
            latex_img_content +
            LatexSyntaxConstructions.end_key_val.value +
            LatexSyntaxConstructions.document_key_val.value
    )
    return latex_doc_prepared


def generate_latex_doc(
        latex_table_raw_content: typing.List[typing.List[str]]
) -> None:
    with open('tsk2.1.tex', 'w') as latex_document:
        latex_doc_content: str = get_latex_doc_content(latex_table_raw_content)
        latex_document.write(latex_doc_content)


if __name__ == '__main__':
    # script copied from tsk2.1 and modified to make also images in Latex
    generate_latex_doc(
        [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # list for example
    )
