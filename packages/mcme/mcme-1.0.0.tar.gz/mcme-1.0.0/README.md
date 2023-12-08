# Meshcapade me command line client

CLI for creating and downloading avatars in the terminal.

## Installation

## Usage

To show the general help use `mcme --help`

### Authentication
When you execute mcme for the first time or after the access token has expired, you will be prompted for username and password. Alternatively you can specify them using `mcme --username --password` or save them as environment variables `MCME_USERNAME` and `MCME_PASSWORD`

### Creating avatars

You can create avatars using the subcommand `mcme create`. You can list the available methods with `mcme create --help`. If you want to download the avatar right away you can do so using 
```
mcme create --download-format <obj/fbx> <from-measurements/from-images/...>
```

### Downloading avatars

You can use
```
mcme download
```
to download your avatars. This will start an export job and after a short processing time, your avatar will be downloaded. You can choose if you want the output as .obj or .fbx file, an output pose, an animation and a compatibility mode. If you don't specify the asset id  of the avatar to download directly, the last ten avatars you created will be listed and you can choose which one to download. If you want to list more than ten, use `--show-max-avatars`.