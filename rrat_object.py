import toml
import glob
import pprint
from typing import Union
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class Property:
    name: str = None
    value: Union[str, int, float, bool, None] = None
    error: Union[str, int, float, bool, None] = False
    frequency: Union[float, None] = None
    telescope: str = None
    minflux: Union[float, bool, None] = None
    ref: str = None


class RRAT:
    list_of_properties = ["Name", "RA", "Dec", "Period", "DM", "Pdot"]

    def __init__(self, toml_dict: dict) -> None:
        self.toml_dict = toml_dict
        for property in self.list_of_properties:
            if property in self.toml_dict:
                setattr(self, property, Property(name=property, **self.toml_dict[property]))
            else:
                setattr(self, property, Property(name=property))
        if "BurstRate" in self.toml_dict:
            setattr(self, "BurstRate", Property(name = "BurstRate", **self.toml_dict["BurstRate"]["Discovery"]))
        else:
            setattr(self, "BurstRate", Property(name="BurstRate"))

        if "Flux" in self.toml_dict:
            pass
        else:
            setattr(self, "Flux", Property(name="Flux"))






if __name__ == "__main__":
    list_of_rrats = glob.glob("rrats/*toml")

    list_of_rrat_objects = []

    for rrats in list_of_rrats:
        list_of_rrat_objects.append(RRAT(toml.load(rrats)))

    env = Environment(
        loader=FileSystemLoader(["templates"]), autoescape=select_autoescape(["html"])
    )
    template = env.get_template("listed_template.html")
    with open("templates/test_out.html", "w") as f:
        out = template.render(
            header=["Name", "RA", "Dec", "Period", "DM", "Pdot" , "BurstRate"],
            list_of_rrat_objects=list_of_rrat_objects,
        )
        f.write(out)
