from biolib._internal.push_application import push_application as _push_application
from biolib.app import BioLibApp as _BioLibApp

def push_application(uri: str, path: str, is_dev: bool = False) -> _BioLibApp:
    push_data = _push_application(
        app_uri=uri,
        app_path=path,
        app_version_to_copy_images_from=None,
        is_dev_version=is_dev)
    uri = f'{push_data["app_uri"]}:{push_data["sematic_version"]}'
    return _BioLibApp(uri)
