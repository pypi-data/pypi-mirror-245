from biolib._internal.push_application import push_application as _push_application
from biolib._internal.push_application import set_app_version_as_active as _set_app_version_as_active

from biolib.app import BioLibApp as _BioLibApp

def push_app_version(uri: str, path: str) -> _BioLibApp:
    push_data = _push_application(
        app_uri=uri,
        app_path=path,
        app_version_to_copy_images_from=None,
        is_dev_version=True)
    uri = f'{push_data["app_uri"]}:{push_data["sematic_version"]}'
    return _BioLibApp(uri)

def set_app_version_as_default(app_version: _BioLibApp) -> None:
    app_version_uuid = app_version.version['public_id']
    _set_app_version_as_active(app_version_uuid)
