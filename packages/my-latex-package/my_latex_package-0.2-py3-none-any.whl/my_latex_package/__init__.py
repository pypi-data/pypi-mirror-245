'''
Необходимо реализовать генератор LaTeX в функциональном стиле. Для генерации латеха нельзя использовать сторонние библиотеки.
2.1
Написать функцию для генерации таблиц. На вход поступает двойной список, на выходе строка с отформатированным валидным латехом. 
'''

def generate_latex_table(matrix):
    """
    Generate a LaTeX formatted table from a 2D list (matrix).

    Args:
    matrix (list of list of str): The 2D list representing the table.

    Returns:
    str: A string containing the LaTeX formatted table.
    """

    # Start the tabular environment
    num_columns = len(matrix[0])
    latex_table = "\\begin{tabular}{" + "|c" * num_columns + "|}\n\\hline\n"

    # Add rows of the table
    for row in matrix:
        latex_table += " & ".join(row) + " \\\\\n\\hline\n"

    # End the tabular environment
    latex_table += "\\end{tabular}"

    return latex_table

def main():
    matrix = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"]
    ]
    print(generate_latex_table(matrix))

if __name__ == "__main__":
    main()