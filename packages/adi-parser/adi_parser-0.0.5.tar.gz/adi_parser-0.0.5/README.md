# adi_parser
This is a simple utility package to parse 
[.adi files](https://wikitia.com/wiki/Amateur_Data_Interchange_Format_(ADIF)#ADI_.28.adi_file_extension.29) 
from [LoTW](https://lotw.arrl.org/). 

It does *not* parse all possible .adi values, only those I've found from 
LoTW .adi exports.

Parsed data is returned as dataclasses. Their definitions are located in 
```adi_parser.dataclasses```. 
All dataclass values are assumed to be missing by default.

## Example
```py
from adi_parser import parse_adi

adi_header, qso_reports = parse_adi("your_data.adi")
```
