from typing import Optional
import requests
import tomli
import os
import json
import click
import time
from datetime import datetime
import re
from typing_extensions import TypedDict
import openapi_client as client
from openapi_client import DocschemasDocAssetResponse as AssetResponse
from openapi_client import PostgresqlAssetState as AssetState
from .logger import log
from .schemas import ExportParameters

MIME_JPG = "image/jpg"
MIME_PLAIN = "text/plain"
MIME_PNG = "image/png"
MIME_VIDEO = "video/mp4"
MIME_TYPES = {"jpg": MIME_JPG, "jpeg": MIME_JPG, "png": MIME_PNG, "obj": MIME_PLAIN, "mp4": MIME_VIDEO}

class KeycloakTokens(TypedDict, total=False):
    active_user: str
    keycloak_tokens: dict[str, dict[str, str]]

def load_config(config: str) -> dict[str, str]:
    """Load config"""
    with open(config, mode="rb") as conf:
        return tomli.load(conf)

def load_state(keycloak_file) -> KeycloakTokens:
    """Load state from a local file"""
    if not os.path.exists(keycloak_file):
        return KeycloakTokens()
    with open(keycloak_file) as state:
        state_json: KeycloakTokens = json.load(state)
        return state_json

def get_user_and_tokens(state, username) -> tuple[str, dict[str,str]]:
    """Load state from a local file"""
    user = username if username is not None else state.get("active_user")
    if "keycloak_tokens" in state and user in state["keycloak_tokens"]:
        return user, state["keycloak_tokens"][user]
    else:
        return user, {}

def update_state_file(keycloak_file: str, state: KeycloakTokens, keycloak_tokens: dict[str, str], username: str) -> None:
    """Save the generated access tokens in a local file"""
    create_parent_dir_if_not_exists(keycloak_file)
    state["active_user"] = username
    if "keycloak_tokens" in state:
        state["keycloak_tokens"][username] = keycloak_tokens
    else:
        state["keycloak_tokens"] = {}
        state["keycloak_tokens"][username] = keycloak_tokens

    with open(keycloak_file, "w") as state_file:
        json.dump(state, state_file)

def create_parent_dir_if_not_exists(keycloak_file: str) -> None:
    parent_dir = os.path.dirname(keycloak_file)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

def parse_betas(ctx: click.Context, param: click.Parameter, value: str) -> list[float]:
    """Parse betas from command line"""
    return [float(x) for x in value.strip('[').strip(']').split(',')] if value is not None else []

def validate_export_parameter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Check export parameters for direct download after creation"""
    if ctx.params["download_format"] is None:
        if value is not None:
            raise click.BadOptionUsage(str(param.name), f"Please use option --download_format if you want to download avatar. Otherwise, please leave out option --{param.name}.", ctx=None)
    # Set pose default value if download is requested
    elif param.name == "pose" and value is None:
        return "A"
    return value

def get_export_parameters(ctx: click.Context) -> ExportParameters:
    """Get download parameters from parent context."""
    if ctx is None or ctx.parent is None:
        raise click.ClickException("Parent context empty")
    download_format = ctx.parent.params["download_format"]
    pose = ctx.parent.params["pose"]
    animation = ctx.parent.params["animation"]
    compatibility_mode = ctx.parent.params["compatibility_mode"]
    out_file = ctx.parent.params["out_file"]
    return ExportParameters(download_format, pose, animation, compatibility_mode, out_file)

def download_avatar(out_filename: str, download_url: str) -> None:
    """Download avatar using presigned aws s3 url."""
    with open(out_filename, 'wb') as file:
        try:
            stream = requests.get(download_url, stream=True, timeout=60)
            stream.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise click.ClickException(str(err)) from err
        for chunk in stream.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)

def parse_avatar_asset(avatar: AssetResponse) -> tuple[str, dict]:
    """Parse avatar from api response and return as dict with selected attributes"""
    if avatar.attributes is not None and \
        avatar.attributes.created_at is not None and \
            avatar.attributes.origin is not None and \
                avatar.attributes.state is not None:
        created_at = datetime.fromtimestamp(avatar.attributes.created_at).strftime("%Y/%m/%d %H:%M:%S")
        created_from_match = re.search("(?<=FROM_).*", avatar.attributes.origin)
        created_from = created_from_match.group() if created_from_match is not None else ""
        name = avatar.attributes.name
        asset_id = avatar.id
        return avatar.attributes.state, {"assetID": asset_id, "name": name, "timestamp": created_at, "origin": created_from}
    return "", {}

def get_ready_avatars(api_instance: client.AvatarsApi, show_max_avatars: int) -> list[dict]:
    """List avatars that have state READY"""
    avatars: list[dict] = []
    page = 1
    # iterate through pages and collect avatars with state ready until there are enough
    while len(avatars) < show_max_avatars:
        api_response = api_instance.list_avatars(limit=show_max_avatars*2, page=page)
        if api_response.data is None:
            raise click.ClickException("Response came back empty")
        if len(api_response.data) == 0:
            break
        for avatar_asset in api_response.data:
            avatar_state, avatar = parse_avatar_asset(avatar_asset)
            if avatar_state == AssetState.READY:
                avatars.append(avatar)
            if len(avatars) == show_max_avatars:
                break
        page += 1
    return avatars

def select_asset_id(api_instance: client.AvatarsApi, show_max_avatars: int) -> tuple[str, str]:
    """Select which avatar to download from available asset ids"""
    avatars = get_ready_avatars(api_instance=api_instance, show_max_avatars=show_max_avatars)
    # No avatars available for this account
    if len(avatars) == 0:
        raise click.ClickException("You have no created avatars to download.")
    # Print avatars available for selection
    prompt_text = "\n\n{:<8}{:<30}{:<40}{:<20}{:<20}\n".format("Number", "Name", "Asset ID", "Created from", "Timestamp")
    for i, avatar in enumerate(avatars):
        prompt_text += "-"*120 + "\n"
        prompt_text += "{:<8}{:<30}{:<40}{:<20}{:<20}\n".format(i, avatar["name"], avatar["assetID"], avatar["origin"], avatar["timestamp"])
    log.info(prompt_text)
    avatar_number = click.prompt('Number of avatar to download', type=int)
    return avatars[avatar_number]["assetID"], avatars[avatar_number]["name"]

class TimeoutTracker(object):
    """Helper class for tracking timeout length"""
    def __init__(self, timeout_length):
        self.start_time = time.time()
        self.timeout = timeout_length
    def timed_out(self):
        return time.time() - self.start_time > self.timeout*60

def get_timestamp():
    """Get timestamp"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

class Uploader:
    """Class for uploading files that can be mocked"""
    def upload(self, file_to_upload: str, upload_url: str) -> None:
        """Upload an image to given url"""
        content_type = MIME_TYPES[file_to_upload.split(".")[-1].lower()]
        with open(file_to_upload, 'rb') as input:
            upload_response = requests.put(upload_url, data=input, headers={'Content-Type': content_type})
        upload_response.raise_for_status()

def get_measurements_dict(
    height,
    weight,
    bust_girth,
    ankle_girth,
    thigh_girth,
    waist_girth,
    armscye_girth,
    top_hip_girth,
    neck_base_girth,
    shoulder_length,
    lower_arm_length,
    upper_arm_length,
    inside_leg_height
    ) -> dict[str, float]:
    """Helper for assembling input measurements"""
    measurements = {
                        "Height": height,
                        "Weight": weight,
                        "Bust_girth": bust_girth,
                        "Ankle_girth": ankle_girth,
                        "Thigh_girth": thigh_girth,
                        "Waist_girth": waist_girth,
                        "Armscye_girth": armscye_girth,
                        "Top_hip_girth": top_hip_girth,
                        "Neck_base_girth": neck_base_girth,
                        "Shoulder_length": shoulder_length,
                        "Lower_arm_length": lower_arm_length,
                        "Upper_arm_length": upper_arm_length,
                        "Inside_leg_height": inside_leg_height
                    }
    for key, value in measurements.copy().items():
        if value is None:
            del measurements[key]
    return measurements
