import os
from pathlib import Path
import re


class QueryLoader:
    _query = None
    _params = None
    _params_regex = re.compile(r"\$\w+(?=\b)")

    def __init__(self, file_path: Path):
        """An object that will lazy load a cypher query from a file and its parameters.
        
        file_path: Path, a  path to a .cypher file.
        """
        self.path = file_path

    @property
    def query(self) -> str:
        if self._query is None:
            with self.path.open() as f:
                self._query = f.read()
        return self._query

    @property
    def params(self) -> dict:
        if self._params is None:
            self._params = {x: None for x in QueryLoader.find_params(self.query)}
        return self._params

    @params.setter
    def params(self, params_dictionary):
        if not isinstance(params_dictionary, dict):
            raise TypeError("params is expected to be dictionary.")
        self._params = params_dictionary

    @staticmethod
    def find_params(string):
        return QueryLoader._params_regex.findall(string)

    def __repr__(self):
        return self.query

    def __str__(self):
        return self.query

    def __call__(self):
        return self.query, self.params


class CypherQueries:
    """Container for QueryLoaders built from a directory of cypher queries.

    Parameters:
    dir: Path, a path to a directory containing .cypher files.    
    """

    def __init__(self, dir):
        dir = Path(dir)
        if not dir.is_dir():
            raise ValueError(
                "dir must represent a path to a directory containing cypher files."
            )
        for f in os.listdir(dir):
            if f.endswith("cypher"):
                fpath = Path(dir, f)
                name = fpath.stem
                setattr(self, name, QueryLoader(fpath))