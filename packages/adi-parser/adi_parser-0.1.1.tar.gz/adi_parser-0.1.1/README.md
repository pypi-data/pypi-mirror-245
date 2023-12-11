# adi_parser
This is a simple utility package, originally to parse 
[.adi files](https://wikitia.com/wiki/Amateur_Data_Interchange_Format_(ADIF)#ADI_.28.adi_file_extension.29) 
from [LoTW](https://lotw.arrl.org/), but now from anywhere.

By default, adi_parser parses [LoTW .adi arguments](#parsing-in-lotw-adi-format). 
You can optionally parse
[all arguments as a python dictionary](#parsing-all-arguments-from-a-adi).


## Examples
### Parsing in LoTW .adi format
```py
from adi_parser import parse_adi

adi_header, qso_reports = parse_adi("path/to/your_data.adi")
```
Where `adi_header: Header` and `qso_reports: list[QSOReport]`. 
These are dataclasses, which are defined in `adi_parser.dataclasses`.

All dataclass values are assumed to be missing by default.

Both `GRIDSQUARE` and `MY_GRIDSQUARE` are converted to lat/lat with
[maidenhead](https://github.com/space-physics/maidenhead).

### Parsing all arguments from a .adi
```py
from adi_parser import parse_adi

result = parse_adi("path/to/your_data.adi", return_type=dict)
```
Where the result dictionary follows this format:
```py
result = {
    "header": {
        "full_text": str,
        "argument_1": str,
        "argument_2": str,
        ...
    },
    "qso_reports": [
        {
            "full_text": str,
            "argument_1": {
                "value": str,
                "length": int,
                "type": str | None,
                "comment": str | None,
            },
            "argument_2": {
                ...
            },
            ...
        },
        ...
    ]
}
``` 