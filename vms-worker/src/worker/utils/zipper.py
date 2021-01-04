import os
from io import BytesIO
from zipfile import ZipFile


def __get_files_form_dir(dir):
    result = []
    for root, dirs, files in os.walk(dir):
        rel_root = os.path.relpath(root, dir)
        for file in files:
            result.append(os.path.join(rel_root, file))
    return result


def zip_directory(dir) -> BytesIO:
    zip_stream = BytesIO()
    with ZipFile(zip_stream, "w") as zip:
        for file in __get_files_form_dir(dir):
            zip.write(os.path.join(dir, file), arcname=file)
    zip_stream.seek(0)
    return zip_stream
