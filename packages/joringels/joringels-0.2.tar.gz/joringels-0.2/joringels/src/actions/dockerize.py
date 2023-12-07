# dockerize.py
# RUN like: jo dockerize
import os, shutil, subprocess
import docker
import os
from docker.errors import BuildError
from docker.errors import ContainerError, ImageNotFound, APIError

# colors for printing
import colorama as color

color.init()
COL_RM = color.Style.RESET_ALL
YELLOW = color.Fore.YELLOW
GREEN = color.Fore.GREEN
RED = color.Fore.RED
WHITE = color.Fore.WHITE

from joringels.src.joringels_server import JoringelsServer
import joringels.src.settings as sts
import joringels.src.helpers as helpers
import joringels.src.arguments as arguments
from joringels.src.actions import fetch

info = (
    f"This re-builds a docker image for joringels and installs "
    f"a joringels package using pipenv\n"
    f"then a docker container 'jo' is created and run.\n"
    f"\nThe image takes some minutes to build!  "
    f"Do you whish to continue [y/n]? : "
)


def run(*args, host=None, entryName, **kwargs) -> None:
    appParams = fetch.main(
        *args, host="loc", entryName="testing.cluster_params._joringels.mappings", **kwargs
    ).get(sts.appName)
    with helpers.temp_chdir(path=sts.dockerPath) as p:
        data = prep_data(*args, **kwargs)
        if input(info) == "y":
            docker_bulid(appParams, *data)
        if input(f"\n{YELLOW}Do you whish to run the container{COL_RM} [y/n]? : ") == "y":
            docker_run(*args, **appParams, **kwargs)


def prep_data(*args, safeName=None, **kwargs):
    if safeName is None:
        safeName = f"{os.environ.get('DATASAFENAME')}{sts.eext}"
    else:
        safeName = f"{safeName}{sts.eext}"
    pgDir = f"root/{sts.appBasePath.split(os.getlogin())[-1].replace(os.sep, '/').strip('/')}"
    return safeName, pgDir


def docker_bulid(appParams, safeName, pgDir, *args, **kwargs):
    copy_secrets(safeName, *args, **kwargs)
    prep_files(safeName, *args, **kwargs)
    buildCmd = docker_build_image(safeName, pgDir, *args, **kwargs)
    cleanup(safeName, *args, **kwargs)


def copy_secrets(safeName, *args, **kwargs):
    # get secrets to COPY to docker image
    safePath = os.path.join(sts.encryptDir, safeName)
    shutil.copyfile(safePath, os.path.join(os.getcwd(), safeName))


def cleanup(safeName: str, *args, **kwargs):
    safePath = os.path.join(os.getcwd(), safeName)
    if os.path.exists(safePath):
        os.remove(safePath)


def prep_files(*args, **kwargs):
    """
    dos2unix
    not clear if needed here
    """
    for file in os.listdir(sts.dockerPath):
        with open(os.path.join(sts.dockerPath, file), "r") as f:
            text = f.read()
        text = text.replace("\r\n", "\n")
        with open(os.path.join(sts.dockerPath, file), "w") as f:
            f.write(text)


def docker_build_image(safeName, pgDir, *args, **kwargs):
    client = docker.from_env()
    build_args = {
        "DATASAFENAME": os.path.splitext(safeName)[0],
        "GIT_ACCESS_TOKEN": os.environ.get("GIT_ACCESS_TOKEN"),
        "PACKAGEDIR": pgDir,
    }
    print(f"Building image for {sts.appName} in {os.getcwd()} with args: {build_args}")
    if input("\nCheck the build params ! Do you wish to [y/n]? : ").lower() == "y":
        try:
            image, build_log = client.images.build(
                path=".", tag=sts.appName, buildargs=build_args, nocache=True, rm=True
            )
            for line in build_log:
                print(line)
            print(f"Successfully built image {image.tags}")
            return image.tags
        except BuildError as e:
            print(f"Build failed: {e}")
            return None


def docker_run(*args, ip_address, ports, **kwargs):
    # Assuming pgName and prDir are passed as arguments to the function
    dockerCommand = (
        f"docker run -itd --rm --name {sts.appName[:2]} --privileged "
        f"-e \"DATAKEY={os.environ.get('DATAKEY')}\" "
        f"-e \"DATASAFEKEY={os.environ.get('DATASAFEKEY')}\" "
        f"-e \"NODEMASTERIP={os.environ.get('DATASAFEIP')}\" "
        f"-e \"DATASAFENAME={os.environ.get('DATASAFENAME')}\" "
        f"--network illuminati -p {':'.join([str(p) for p in ports])} --ip {ip_address} "
        f"{sts.appName}"
    )
    print(
        f"{GREEN}\n\nDONE: \nCopy the build command:{COL_RM}\n"
        f"{YELLOW}CHANGE DIRECTORY to or stay Joringels directory{COL_RM}\n"
        f"{WHITE}paste to run the container...{COL_RM}\n"
        f"{dockerCommand}"
    )
    return dockerCommand


def main(*args, **kwargs) -> None:
    return run(*args, **kwargs)


if __name__ == "__main__":
    main(**arguments.mk_args().__dict__)

# # currently not used because python docker installed
# def _docker_build_image(safeName, pgDir, *args, **kwargs):
#     buildCmd = (
#                     f"docker build --progress=plain --no-cache "
#                     f"--build-arg DATASAFENAME={os.path.splitext(safeName)[0]} "
#                     f"--build-arg GIT_ACCESS_TOKEN={os.environ.get('GIT_ACCESS_TOKEN')} "
#                     f"--build-arg PACKAGEDIR={pgDir} "
#                     f"-t {sts.appName} ."
#         )
#     print(f"Building: {os.getcwd()}: {os.listdir()}\n{buildCmd = }")
#     if input(f"\n{YELLOW}Do you whish to continue{COL_RM} [y/n]? : ") == 'y':
#         subprocess.run(buildCmd, shell=True)
#     return buildCmd

# # not working TypeError: run() got an unexpected keyword argument 'ip'
# def _docker_run(*args, ip_address, ports, **kwargs):
#     client = docker.from_env()

#     # Prepare environment variables
#     envVars = ['DATAKEY', 'DATASAFEKEY', 'NODEMASTERIP', 'DATASAFENAME',]
#     environment = {var: os.environ.get(var) for var in envVars}

#     # Prepare port bindings
#     port_bindings = {f'{port}/tcp': port for port in ports}

#     print(f"Running Docker container for {sts.appName} with IP {ip_address} and ports {ports}")

#     try:
#         container = client.containers.run(
#             sts.appName,
#             name=sts.appName[:2],
#             detach=True,
#             privileged=True,
#             environment=environment,
#             network="illuminati",
#             ports=port_bindings,
#             ip=ip_address
#         )

#         print(f"Container {container.id} started")
#         return container.id

#     except (ContainerError, ImageNotFound, APIError) as e:
#         print(f"Error running container: {e}")
#         return None
