import json
import click
import os
import requests

url = "https://content.dropboxapi.com"


@click.command()
@click.option(
    "--remote_path", prompt="", help="Path in the user's Dropbox to save the file"
)
@click.option("--local_path", help="Path in the user's local to save the file")
@click.option(
    "--mode",
    default="add",
    help="Selects what to do if the file already exists. The default for this union is add",
)
@click.option(
    "--autorename",
    default=True,
    help="If there's a conflict, as determined by mode, have the Dropbox server try to autorename the file to avoid conflict. The default for this field is False.",
)
@click.option(
    "--mute",
    default=False,
    help="Normally, users are made aware of any file modifications in their Dropbox account via notifications in the client software. If true, this tells the clients that this modification shouldn't result in a user notification. The default for this field is False",
)
@click.option(
    "--strict_conflict",
    default=False,
    help="Be more strict about how each WriteMode detects conflict. For example, always return a conflict error when mode = WriteMode.update and the given 'rev' doesn't match the existing file's 'rev', even if the existing file has been deleted. This also forces a conflict even when the target path refers to a file with identical contents. The default for this field is False",
)
def file_upload(
    remote_path: str,
    local_path: str,
    mode: str,
    autorename: bool,
    mute: bool,
    strict_conflict: bool,
) -> None:

    if not os.path.exists(local_path):
        click.echo(f"File with path {local_path} doesn't exist")
        click.echo(os.path.curdir)
        return

    upload_url = url + "/2/files/upload"
    auth_token = f"Bearer {os.getenv('DROPBOX_ACCESS_TOKEN')}"
    api_arg = {
        "path": remote_path,
        "mode": mode,
        "autorename": autorename,
        "mute": mute,
        "strict_conflict": strict_conflict,
    }
    headers = {
        "Authorization": auth_token,
        "Dropbox-API-Arg": json.dumps(api_arg),
        "Content-Type": "application/octet-stream",
    }

    with open(local_path) as payload:
        click.echo("uploading ..")
        files = {"upload_file": payload}
        res = requests.post(url=upload_url, headers=headers, files=files)

    if res.status_code == 200:
        click.echo(f"file {local_path} successfully upload to {remote_path}")
        return

    click.echo(f"something went wrong and the file {local_path} could't be upload")
    click.echo(f"reason: {res.text}")
