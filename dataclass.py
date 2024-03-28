from dataclasses import dataclass


@dataclass
class DataClass:
    data: dict

    def __getattr__(self, name):
        return self.data.get(name)


