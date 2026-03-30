import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table


def save_df_as_image(df: pd.DataFrame, output_path: str):
    """
    Converts a pandas DataFrame into a simple, readable table image using Matplotlib.

    Args:
        df: The DataFrame to render.
        output_path: Path where the PNG image will be saved.
    """
    if df.empty:
        # Create a placeholder if DF is empty
        df = pd.DataFrame({"Aviso": ["Nenhum dado encontrado para gerar a tabela."]})

    # Create figure and axis
    # We use a dynamic height based on the number of rows to keep it readable
    num_rows = len(df)
    fig_height = max(2, num_rows * 0.5)
    fig, ax = plt.subplots(figsize=(12, fig_height))

    # Hide axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    # Create the table
    tab = table(ax, df, loc="center", cellLoc="center")

    # Simple styling for readability
    tab.auto_set_font_size(False)
    tab.set_fontsize(11)
    tab.scale(1.2, 1.5)  # Row height and column width scaling

    # Header styling
    for (row, col), cell in tab.get_celld().items():
        if row == 0:
            cell.set_text_props(
                weight="bold", color="white", ha="center", va="center", wrap=True
            )
            cell.set_facecolor("#404040")  # Dark gray header
        else:
            cell.set_facecolor("#f2f2f2" if row % 2 == 0 else "white")  # Zebra striping

    # Save the figure
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
