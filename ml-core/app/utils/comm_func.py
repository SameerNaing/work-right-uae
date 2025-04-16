import shutil
import requests
import pymupdf4llm


def pdf_to_markdown(file):
    return pymupdf4llm.to_markdown(file)


def download_files(urls, filenames, destination_folder, allow_exts=None):
    for url, filename in zip(urls, filenames):
        response = requests.get(url, stream=True)
        ext = (
            response.headers.get("Content-Disposition")
            .split("filename=")[-1]
            .split(".")[-1]
        )

        if allow_exts and ext not in allow_exts:
            continue

        filename = f"{filename}.{ext}"
        with open(f"{destination_folder}/{filename}", "wb") as f:
            f.write(response.content)
            return f"{destination_folder}/{filename}"


def delete_folder(folder):
    shutil.rmtree(folder)


def get_username_from_email(email):
    username = email.split("@")[0]
    if "." in username:
        username = username.split(".")[0]

    return username.capitalize()
