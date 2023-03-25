# Namecoin Research

Python scripts that use RPC calls to extract data from Namecoin Core.

## Active Names

The script `active_names.py`generates a CSV of all active names registered before a threshold date (default 2015-12-31), sorted by age. The output file `active_names_{current_date}.csv` contains block height and date of _name_firstupdate_ for each name, as well as all unique metadata values up until the threshold date.