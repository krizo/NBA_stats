import yaml
import os


class DbCredentials:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    @property
    def _credentials_file(self):
        return self.dir_path + os.sep + 'db_credentials.yml'

    @property
    def _credentials(self):
        with open(self._credentials_file, 'r', encoding='utf-8') as stream:
            return yaml.safe_load(stream)

    @property
    def user_name(self) -> str:
        return self._get_credential('user_name')

    @property
    def password(self) -> str:
        return self._get_credential('password')

    @property
    def port(self) -> int:
        return int(self._get_credential('port'))

    @property
    def hostname(self) -> str:
        return self._get_credential('hostname')

    @property
    def driver(self) -> str:
        return self._get_credential('driver')

    @property
    def db_name(self) -> str:
        return self._get_credential('db_name')

    def _get_credential(self, property_name: str) -> str:
        value = self._credentials.get(property_name)
        assert value, f"No credentials for {property_name}"
        return value
