import toml
import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd
from pprint import pprint as print

table_keys = ["Name", "RA", "Dec", "DM", "Period"] #, "BurstRate", "Flux", "Width"]
units = ["","HH:MM:SS.SS","DD:MM:SS.SS","s","hr^{-1}","Jy","ms"]
df_keys = table_keys + [x+"_ref" for x in table_keys]


if __name__ == "__main__":
    list_of_rrats = glob.glob("rrats/*toml")
    rrat_dict = {}

    for key in df_keys:
        rrat_dict[key] = []

    for rrat in list_of_rrats:
        try:
            rrat_toml = toml.load(rrat)
            for key in table_keys:
                if key in rrat_toml:
                    if "value" in rrat_toml[key]:
                        rrat_dict[key].append(rrat_toml[key]["value"])
                        if "ref" in rrat_toml[key]:
                            rrat_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                        else:
                            rrat_dict[key + "_ref"].append(None)
                    else:
                        # it's a nested dictionary
                        pass
                else:
                    rrat_dict[key].append(None)
                    rrat_dict[key + "_ref"].append(None)
        except toml.decoder.TomlDecodeError:
            print(rrat)
            pass

    df = pd.DataFrame(rrat_dict)
    print(df)

    env = Environment(
        loader=FileSystemLoader(["templates"]), autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")
    with open("templates/test_out.html", "w") as f:
        out = template.render(header=table_keys, df=df[table_keys])
        f.write(out)