import datetime

from mango_pycore.environment_data.adapters.access_control_adapter import AccessControl
from mango_pycore.environment_data.adapters.s3_environment_adapter import S3Environment
from mango_pycore.environment_data.datatypes import EnvironmentDriver
from mango_pycore.tools.utils import set_environment_vars

_ENVIRONMENT_VARS = {}


class EnvironmentDataService:
    def __init__(self, driver: str, parameters: dict):

        assert driver in EnvironmentDriver, "Allowed values for driver are access_control, s3"

        self._driver = None
        if driver == "access_control":
            assert 'url' in parameters.keys(), "url parameter is missing for access control driver"
            assert 'secret_b' in parameters.keys(), "secret_b parameter is missing for access control driver"
            assert 'uuid_key' in parameters.keys(), "uuid_key parameter is missing for access control driver"

            self._driver = AccessControl(
                url=parameters["url"],
                secret_b=parameters["secret_b"],
                uuid_key=parameters["uuid_key"]
            )

        if driver == "s3":
            assert 'bucket' in parameters.keys(), "bucket parameter is missing for s3 driver"
            assert 'key' in parameters.keys(), "key parameter is missing for s3 driver"
            assert 'access_key' in parameters.keys(), "access_key parameter is missing for s3 driver"
            assert 'secret_key' in parameters.keys(), "secret_key parameter is missing for s3 driver"
            assert 'region' in parameters.keys(), "region parameter is missing for s3 driver"

            self._driver = S3Environment(
                bucket=parameters["bucket"],
                key=parameters["key"],
                access_key=parameters["access_key_id"],
                secret_key=parameters["secret_key_id"],
                region=parameters["region"]
            )



    def load_environment_data(self, origin: str):
        global _ENVIRONMENT_VARS
        if self._driver:
            date = datetime.datetime.now()

            # origin is not in environment or environment does not exist
            if origin not in _ENVIRONMENT_VARS:
                data = self._driver.get_backend_data(origin)
                if data:
                    _ENVIRONMENT_VARS[origin] = {
                        "date": date,
                        "data": data
                    }

            # Origin was found
            else:
                if (date - _ENVIRONMENT_VARS[origin]["date"]).seconds > 300:  # Data is deprecated by timeout of 5 min
                    data = self._driver.get_backend_data(origin)
                    if data:
                        _ENVIRONMENT_VARS[origin] = {
                            "date": date,
                            "data": data
                        }
                else:  # Data still valid
                    _ENVIRONMENT_VARS[origin]["date"] = date
                    print("Returning existing config data: ", _ENVIRONMENT_VARS[origin]["data"])

        if origin in _ENVIRONMENT_VARS:
            set_environment_vars(origin=origin, data=_ENVIRONMENT_VARS[origin]["data"])
            if isinstance(_ENVIRONMENT_VARS[origin]["data"], dict):
                _ENVIRONMENT_VARS[origin]["data"].update({
                    "ORIGIN": origin
                })
            return _ENVIRONMENT_VARS[origin]["data"]
