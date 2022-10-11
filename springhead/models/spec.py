from typing import Any, Dict


class SpringheadSpecification:
    def __init__(self) -> None:
        self.path = ""
        self.spec = None

    def _is_path_valid(self, path: str) -> bool:
        return True

    def is_spec_file_valid(self, yml_dict: Dict[str, Any]) -> bool:
        return True

    def _read_yml_file(self, path):
        pass

    def read_spec_file(self, path):
        return self._read_spec_file(path)

    def _read_spec_file(self, path):
        if not self._is_path_valid(self):
            raise Exception("error")

        yml_config = self._read_yml_file(path)

        if not self.is_spec_file_valid(yml_config):
            raise Exception("error")

        self.spec = yml_config
