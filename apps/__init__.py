import pyspark.sql.functions as F
from dataclasses import dataclass


class ruleDomain:
    @dataclass
    class ruleDomainParameters:
        name: str
        age: str
        city: str

    @dataclass
    class dtypesAllowed:
        name: str
        age: int
        city: str

    def __init__(self, data_dict, df):
        self._df = df
        self._domain_params = self._get_domain_parameters(data_dict)

    def _get_domain_parameters(self, data_dict):
        return self.ruleDomainParameters(**data_dict)

    def _valid_dataframe_dtypes(self):
        allowed_fields = self.dtypesAllowed.__dataclass_fields__.keys()
        _dtypes = (
            self._df
            .select(*[F.col(_col).alias(_alias) for _alias, _col in self._domain_params.__dataclass_fields__.items() if _alias in allowed_fields])
        ).dtypes
        self.dtypesAllowed(**dict(_dtypes))
        ## should throw error

    # @classmethod
    # def transform_data(cls, data_dict):
    #     data_obj = cls.ruleDomainParameters(**data_dict)
    #     # Perform any transformations on the data object here
    #     transformed_data = data_obj  # Placeholder for the transformation
    #     return transformed_data
