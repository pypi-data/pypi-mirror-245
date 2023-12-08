
import os
from typing import Any, Optional
import openapi_client as client
import click
from os import path
from datetime import datetime
from .logger import log
from .auth import authenticate
from .helpers import (load_config, 
                      parse_betas, 
                      validate_export_parameter, 
                      get_export_parameters, 
                      download_avatar,
                      select_asset_id,
                      get_timestamp,
                      get_measurements_dict,
                      Uploader)
from .avatars import from_betas, export, from_images, from_measurements, from_scans, from_video


CURRENT_DIR = path.dirname(path.abspath(__file__))
DEFAULT_CONFIG = path.join(CURRENT_DIR, "../configs/prod.toml")

@click.group()
@click.pass_context
@click.option('--config',
              type=click.Path(exists=True), default=DEFAULT_CONFIG, help="Path to config file")
@click.option(
    "--username",
    default=lambda: os.environ.get("MCME_USERNAME")
)
@click.option(
    "--password",
    default=lambda: os.environ.get("MCME_PASSWORD")
)
def cli(ctx: click.Context, 
        username: str,
        password: str,
        config: str) -> None:
    """
    Command-line interface for the Meshcapade.me API.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["keycloak_tokens"] = os.path.expanduser(ctx.obj["config"]["cli_state"]["keycloak_tokens"])
    ctx.obj["token"] = authenticate(ctx.obj["config"]["auth"], ctx.obj["keycloak_tokens"], username, password)
    # construct api client
    configuration = client.Configuration(
        host = ctx.obj["config"]["api"]["host"]
    )
    configuration.access_token =  ctx.obj["token"]
    # Enter a context with an instance of the API client
    ctx.obj["api_client"] = client.ApiClient(configuration)
    

@cli.result_callback()
@click.pass_context
def close_api_client(
    ctx: click.Context,
    result: Any,
    **kwargs):
    ctx.obj["api_client"].close()


@cli.group()
@click.pass_context
@click.option(
    "--download-format",
    type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
    is_eager=True,
    help="Format for downloading avatar"
)
@click.option(
    "--pose",
    type=click.Choice(["T", "A", "SCAN", "U", "I", "W"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Pose the downloaded avatar should be in"
)
@click.option(
    "--animation",
    type=click.Choice(["a-salsa"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Animation for the downloaded avatar"
)
@click.option(
    "--compatibility-mode",
    type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Compatibility mode"
)
@click.option(
    "--out-file",
    type=click.Path(dir_okay=False),
    callback=validate_export_parameter,
    help="File to save created avatar mesh to"
)
def create(
    ctx: click.Context, 
    download_format: str, 
    pose: str, 
    animation: str, 
    compatibility_mode: str, 
    out_file: click.Path
    ) -> None:
    """
    Create avatars.
    """
    # all create avatar operations need keycloak authentication
    ctx.obj["download"] = True if download_format is not None else False


@create.command(name="from-betas")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--betas',
              type=click.UNPROCESSED, callback=parse_betas, 
              help="Beta values. Supply like 0.1,0.2 or \"[0.1,0.2]\"")
@click.option('--name',
              type=str, 
              default="avatar_from_betas",
              help="Name of created avatar")
@click.option('--model-version',
              type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False), 
              help="Model version")
def create_from_betas(
    ctx: click.Context,
    gender: Optional[client.EnumsGender], 
    betas: list[float], 
    name: str, 
    model_version: Optional[client.EnumsModelVersion]
    ) -> None:
    """Create avatar from betas."""
    # Create avatar from betas
    api_instance = client.CreateAvatarsFromBetasApi(ctx.obj["api_client"])
    asset_id = from_betas(gender, betas, name, model_version, api_instance)
    log.info(f"AssetID: {asset_id}")

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-measurements")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              required=True,
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_measurements",
              help="Name of created avatar")
@click.option('--height',
              type=float,
              help="Height")
@click.option('--weight',
              type=float,
              help="Weight")
@click.option('--bust-girth',
              type=float,
              help="Bust girth")
@click.option('--ankle-girth',
              type=float,
              help="Ankle girth")
@click.option('--thigh-girth',
              type=float,
              help="Thigh girth")
@click.option('--waist-girth',
              type=float,
              help="Waist girth")
@click.option('--armscye-girth',
              type=float,
              help="Armscye girth")
@click.option('--top-hip-girth',
              type=float,
              help="Top hip girth")
@click.option('--neck-base-girth',
              type=float,
              help="Neck base girth")
@click.option('--shoulder-length',
              type=float,
              help="Shoulder length")
@click.option('--lower-arm-length',
              type=float,
              help="Lower arm length")
@click.option('--upper-arm-length',
              type=float,
              help="Upper arm length")
@click.option('--inside-leg-height',
              type=float,
              help="Inside leg height")
@click.option('--model-version',
              type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False), 
              help="Model version")
def create_from_measurements(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
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
    inside_leg_height,
    model_version: Optional[client.EnumsModelVersion]
    ) -> None:
    """Create avatar from measurements."""
    # Create avatar from measurements
    measurements = get_measurements_dict(
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
    )
    api_instance_from_measurements = client.CreateAvatarFromMeasurementsApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_measurements(gender, name, measurements, model_version, api_instance_from_measurements, api_instance_avatars, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)

@create.command(name="from-images")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_images",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input image")
@click.option('--height',
              type=int,
              help="Height of the person in the image")
@click.option('--weight',
              type=int,
              help="Weight of the person in the image")
@click.option('--image-mode',
              type=click.Choice(["AFI", "SHAPY", "BEDLAM_CLIFF"], case_sensitive=False),
              default="AFI",
              help="Mode for avatar creation")
def create_from_images(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    height: int,
    weight: int,
    image_mode: str
    ) -> None:
    """Create avatar from images."""
    api_instance_images = client.CreateAvatarFromImagesApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_images(gender, name, input, height, weight, image_mode, api_instance_images, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-scans")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_scans",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input image")
@click.option('--init-pose',
              type=str,
              help="Pose for initialization")
@click.option('--up-axis',
              type=str,
              help="Up axis")
@click.option('--look-axis',
              type=str,
              help="Look axis")
@click.option('--input-units',
              type=str, 
              help="Input units of scan")
def create_from_scans(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    init_pose: str,
    up_axis: str,
    look_axis: str,
    input_units: str
    ) -> None:
    """Create avatar from images."""
    api_instance_scan = client.CreateAvatarFromScansApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_scans(gender, name, input, init_pose, up_axis, look_axis, input_units, api_instance_scan, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-video")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_images",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input video")
@click.option('--model-version',
              type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False), 
              help="Model version")
def create_from_video(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    model_version: Optional[client.EnumsModelVersion],
    ) -> None:
    """Create avatar from video."""
    api_instance_video = client.CreateAvatarFromVideoApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_video(gender, name, input, model_version, api_instance_video, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@cli.command(name="download")
@click.pass_context
@click.option(
    "--format",
    type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
    default="OBJ",
    help="Format for downloading avatar"
)
@click.option(
    "--pose",
    type=click.Choice(["T", "A", "SCAN", "U", "I", "W"], case_sensitive=False),
    default = "A",
    help="Pose the downloaded avatar should be in"
)
@click.option(
    "--animation",
    type=click.Choice(["a-salsa"], case_sensitive=False),
    help="Animation for the downloaded avatar"
)
@click.option(
    "--compatibility-mode",
    type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
    help="Compatibility mode"
)
@click.option(
    "--out-file",
    type=click.Path(dir_okay=False),
    help="File to save created avatar mesh to"
)
@click.option(
    "--asset-id",
    type=str,
    help="Asset id of avatar to be downloaded"
)
@click.option(
    "--show-max-avatars",
    type=int,
    default=10,
    help="Maximum number of created avatars to show (most recent ones are shown first)"
)
def export_and_download_avatar(
    ctx: click.Context,
    format: str, 
    pose: str, 
    animation: str, 
    compatibility_mode: str, 
    out_file: click.Path,
    asset_id: str,
    show_max_avatars: int
    ) -> None:
    """
    Export avatar using asset id.
    """
    api_instance = client.AvatarsApi(ctx.obj["api_client"])
    name = None
    if asset_id is None:
        asset_id, name = select_asset_id(api_instance, show_max_avatars)

    # Export avatar
    timeout = ctx.obj["config"]["cli"]["timeout"]
    download_url = export(asset_id, format, pose, animation, compatibility_mode, api_instance, timeout)
    out_filename = str(out_file) if out_file is not None else \
        f"{get_timestamp()}_{name}.{format.lower()}" if name is not None else \
        f"{get_timestamp()}_{asset_id}.{format.lower()}"
    download_avatar(out_filename, download_url)
    log.info(f"Downloaded avatar to {out_filename}")



@cli.command()
@click.pass_context
def info(ctx: click.Context) -> None:
    """Show API info."""
    # Create an instance of the API class
    api_instance = client.InfoApi(ctx.obj["api_client"])

    try:
        # Show API info
        api_response: str = api_instance.info()
        log.info(api_response)
    except Exception as e:
        log.info("Exception when calling InfoApi->info: %s\n" % e)
