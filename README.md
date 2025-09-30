# sct2df

Schematic Checking Tool Netlist to DataFrame library

```py
from pathlib import Path
from sct2df.parse import (
    to_record_list
)
import pandas as pd
#import polars as pl

# where ever your file is
sct_netlist_txt_file = Path("data") / "Example_SCT_Netlist.txt"

# returns records to not enforce pandas version without reason to
record_list = to_record_list(path=sct_netlist_txt_file, symbols=["U1", "U3", "J1"])

# actually make the dataframe
dataframe = pd.DataFrame.from_records(df_record_list)

# Save it to CSV file
dataframe_path = Path("data") / "Example_SCT_Netlist.csv"
dataframe.to_csv(dataframe_path, index=False)

# Print out information (or further analysis)
print(df)
```
