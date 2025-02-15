def print_table(table):
    """
    Imprime una tabla en formato legible.
    """
    for row in table:
        print("\t".join(f"{val:.2f}" for val in row))

def format_table_for_frontend(table):
    """
    Formatea una tabla para enviarla al frontend.
    """
    return [[round(val, 2) for val in row] for row in table]