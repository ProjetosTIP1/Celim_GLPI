import os
import pandas as pd
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils.table_renderer import save_df_as_image

def test_save_df_as_image_creates_file():
    # Setup
    df = pd.DataFrame({
        "Numero": ["123", "456"],
        "Solicitante": ["User A", "User B"],
        "Titulo": ["Bug 1", "Bug 2"]
    })
    output_path = "test_table.png"
    
    # Action
    if os.path.exists(output_path):
        os.remove(output_path)
    
    save_df_as_image(df, output_path)
    
    # Assert
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    
    # Cleanup
    if os.path.exists(output_path):
        os.remove(output_path)

if __name__ == "__main__":
    test_save_df_as_image_creates_file()
    print("Test passed!")
