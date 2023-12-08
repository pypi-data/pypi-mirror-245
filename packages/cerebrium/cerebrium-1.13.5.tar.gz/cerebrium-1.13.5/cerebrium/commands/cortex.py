import json
import os
from termcolor import colored
import typer
from rich.console import Group
from rich.panel import Panel
from rich import print as console
from typing import Union

import cerebrium.api as api
import cerebrium.sync_files as sync_files

from cerebrium import utils
from cerebrium.core import app
from cerebrium import datatypes
from cerebrium import verification

from cerebrium import __version__ as cerebrium_version
from cerebrium.sync_files import (
    upload_files_to_s3,
    upload_marker_file_and_delete,
)
from cerebrium.utils import cerebriumLog

_EXAMPLE_MAIN = """
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    # Add your input parameters here
    prompt: str
    your_param: Optional[str] = None # an example optional parameter


def predict(item, run_id, logger):
    item = Item(**item)

    ### ADD YOUR CODE HERE
    my_results = {"prediction": item.prompt, "your_optional_param": item.your_param} 
    my_status_code = 200 # if you want to return some status code 

    ### RETURN YOUR RESULTS
    return {"my_result": my_results, "status_code": my_status_code} # return your results
"""


@app.command()
def init(
    init_dir: str = typer.Argument(
        ".",
        help="Directory where you would like to init a Cortex project.",
    ),
    name: str = typer.Option(
        "my-cortex-deployment", help="Name of the Cortex deployment."
    ),
    overwrite: bool = typer.Option(
        False, help="Flag to overwrite contents of the init_dir."
    ),
    requirements_list: str = typer.Option(
        "['transformers', 'torch>=2.0.0']",
        help=(
            "Optional list of requirements. "
            "Example: \"['transformers', 'torch==1.31.1']\""
        ),
    ),
    pkg_list: str = typer.Option(
        "['git', 'ffmpeg' ]",
        help=("Optional list of apt packages. For example: \"['git', 'ffmpeg' ]\""),
    ),
    conda_pkglist: str = typer.Option("", help="Optional list of conda packages."),
    gpu: str = typer.Option(
        "AMPERE_A5000",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'GPU'. "
            f"Can be one of: {datatypes.Hardware.available_hardware()} "
        ),
    ),
    cpu: int = typer.Option(
        2,
        min=datatypes.MIN_CPU,
        max=datatypes.MAX_CPU,
        help=(
            "Number of CPUs to use for the Cortex deployment. "
            "Defaults to 2. Can be an integer between 1 and 48"
        ),
    ),
    memory: float = typer.Option(
        datatypes.DEFAULT_MEMORY,
        min=datatypes.MIN_MEMORY,
        max=datatypes.MAX_MEMORY,
        help=(
            "Amount of memory (in GB) to use for the Cortex deployment. "
            "Defaults to 14.5GB. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: int = typer.Option(
        1,
        min=0,
        max=datatypes.MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. "
            "Defaults to 1. Can be an integer between 1 and 8."
        ),
    ),
    include: str = typer.Option(
        datatypes.DEFAULT_INCLUDE,
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        datatypes.DEFAULT_EXCLUDE,
        help=(
            "Comma delimited string list of relative paths to files/folder to exclude. "
            "Defaults to all hidden files/folders in project root."
        ),
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    predict_data: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    disable_animation: bool = typer.Option(
        bool(os.getenv("CI")),
        help="Whether to use TQDM and yaspin animations.",
    ),
):
    """
    Initialize an empty Cerebrium Cortex project.
    """

    if gpu:
        vals = datatypes.Hardware.available_hardware()
        if gpu not in vals:
            utils.cerebriumLog(message=f"Hardware must be one of {vals}", level="ERROR")
        hardware = getattr(datatypes.Hardware, gpu).name

    if not os.path.exists(init_dir):
        os.makedirs(init_dir)
    elif os.listdir(init_dir) and not overwrite:
        utils.cerebriumLog(
            level="WARNING",
            message="Directory is not empty. "
            "Use an empty directory or use the `--overwrite` flag.",
            end="\t",
        )

    if not os.path.exists(os.path.join(init_dir, "main.py")):
        with open(os.path.join(init_dir, "main.py"), "w") as f:
            f.write(_EXAMPLE_MAIN)

    config = {
        "name": name,
        "gpu": hardware,
        "cpu": cpu,
        "memory": memory,
        "log_level": log_level,
        "include": include,
        "exclude": exclude,
        "cooldown": datatypes.DEFAULT_COOLDOWN,
        "gpu_count": gpu_count,
        "predict_data": predict_data
        or '{"prompt": "Here is some example predict data for your cerebrium.toml which will be used to test your predict function on build."}',
        "min_replicas": 0,
        "disable_predict": False,
        "force_rebuild": False,
        "disable_confirmation": False,
    }
    if disable_animation is not None:
        config["disable_animation"] = disable_animation

    requirements_list = requirements_list.strip("[]").split(",")
    requirements_list = [r.strip().strip("'").strip('"') for r in requirements_list]
    pkg_list = pkg_list.strip("[]").split(",")
    pkg_list = [p.strip().strip("'").strip('"') for p in pkg_list]
    conda_pkglist = conda_pkglist.strip("[]").split(",")
    conda_pkglist = [c.strip().strip("'").strip('"') for c in conda_pkglist]
    # if any of the lists only contain an empty string, set to empty list
    requirements_list = (
        {}
        if len(requirements_list) == 1 and requirements_list[0] == ""
        else requirements_list
    )
    pkg_list = {} if len(pkg_list) == 1 and pkg_list[0] == "" else pkg_list
    conda_pkglist = (
        {} if len(conda_pkglist) == 1 and conda_pkglist[0] == "" else conda_pkglist
    )

    utils.legacy_to_toml_structure(
        config,
        os.path.join(init_dir, "cerebrium.toml"),
        pip=requirements_list,
        apt=pkg_list,
        conda=conda_pkglist,
        overwrite=overwrite,
    )

    print("🚀 Cerebrium Cortex project initialized successfully!")


def stream_logs(
    config: datatypes.CerebriumConfig,
    api_key: str,
    setup_response,
    hide_public_endpoint: bool,
    is_run=False,
):
    project_id = setup_response["projectId"]
    build_id = setup_response["buildId"]
    jwt = setup_response["jwt"]
    name = config.deployment.name
    gpu = config.hardware.gpu
    build_status = api._poll_app_status(
        api_key=api_key,
        build_id=build_id,
        disable_animation=bool(config.build.disable_animation),
        disable_build_logs=bool(config.build.disable_build_logs),
        is_run=is_run,
        gpu=gpu,
    )

    if "success" in build_status:
        if not is_run:
            env = "dev-" if "dev" in api_key else ""
            endpoint = f"https://{env}run.cerebrium.ai/v3/{project_id}/{name}/predict"
            curl_command = colored(
                f"curl -X POST {endpoint} \\ \n"
                "     -H 'Content-Type: application/json'\\ \n"
                f"     -H 'Authorization: {jwt}'\\\n"
                '     --data \'{"prompt": "Hello World!"}\' \n',
                "green",
            )
            dashboard_url = (
                f"{api.dashboard_url}/projects/{project_id}/models/{project_id}-{name}"
            )
            builds_url = f"{dashboard_url}?tab=builds"
            runs_url = f"{dashboard_url}?tab=runs"

            if hide_public_endpoint:
                info_string = (
                    f"🔗 [link={dashboard_url}]View your deployment dashboard here[/link]\n"
                    f"🔗 [link={builds_url}]View builds here[/link]\n"
                    f"🔗 [link={runs_url}]View runs here[/link]"
                )
            else:
                info_string = (
                    f"🔗 [link={dashboard_url}]View your deployment dashboard here[/link]\n"
                    f"🔗 [link={builds_url}]View builds here[/link]\n"
                    f"🔗 [link={runs_url}]View runs here[/link]\n\n"
                    f"🛜  Endpoint:\n{endpoint}"
                )

            dashboard_info = Panel(
                info_string,
                title=f"[bold green]🚀 {name} is now live! 🚀 ",
                border_style="green",
                width=100,
                padding=(1, 2),
            )
            success_group = Group(
                dashboard_info,
            )
        else:
            success_group = Group(
                Panel(
                    f"🚀 {name} ran successfully🚀",
                    title="[bold green]Run Completed",
                    border_style="bold green",
                    width=100,
                    padding=(1, 2),
                )
            )

        console(success_group)
        if not hide_public_endpoint:
            print(
                "\n💡You can call the endpoint with the following curl command:\n"
                f"{curl_command}"
            )

        # time.sleep(1.5)
        # if not is_run:
        #     # Open the build dashboard
        #     try:
        #         webbrowser.open(url=dashboard_url, new=2)
        #     except Exception:
        #         pass


def setup_app(
    api_key: str,
    config: datatypes.CerebriumConfig,
    cerebrium_function: str = "deploy",
):
    # Set api_key using login API Key if not provided
    if not api_key:
        print(
            "🗝️  No API key provided. Getting your API Key from your cerebrium.toml file..."
        )
        api_key = utils.get_api_key()
    if not api_key:
        utils.cerebriumLog(
            level="ERROR",
            message="No API key provided. Please provide an API key using the --api-key flag or by running `cerebrium login`.",
        )
    config.api_key = api_key

    requirements_hash = utils.content_hash(
        files=[], strings=str(config.dependencies.pip)
    )
    pkglist_hash = utils.content_hash(files=[], strings=str(config.dependencies.apt))
    conda_pkglist_hash = utils.content_hash(
        files=[], strings=str(config.dependencies.conda)
    )

    file_list = utils.determine_includes(
        include=config.deployment.include,
        exclude=config.deployment.exclude,
    )

    config.partial_upload = False
    # If files are larger than 100MB, use partial_upload and localFiles
    if utils.check_deployment_size(file_list, 100):
        if len(file_list) < 1000:
            print("📦 Large upload, only uploading files that have changed...")
            config.partial_upload = True
            config.local_files = sync_files.gather_hashes(file_list)
        else:
            print(
                "⚠️ 1000+ files detected. Partial sync not possible. Try reduce the number of files or file size for faster deployments."
            )

    # Include the predict data in the content hash to trigger a rebuild if the predict changes
    files_hash = utils.content_hash(file_list, strings=[config.build.predict_data])

    backend_params = {
        "name": config.deployment.name,
        "function": cerebrium_function,
        "cooldown": config.scaling.cooldown,
        "cerebrium_version": cerebrium_version,
        "min_replicas": config.scaling.min_replicas,
        "max_replicas": config.scaling.get("max_replicas"),
        "hardware": config.hardware.get("gpu", datatypes.DEFAULT_GPU_SELECTION).upper(),
        "gpu_count": config.hardware.get("gpu_count", datatypes.DEFAULT_GPU_COUNT),
        "cpu": config.hardware.get("cpu", datatypes.DEFAULT_CPU),
        "memory": config.hardware.get("memory", datatypes.DEFAULT_MEMORY),
        "python_version": config.deployment.get("python_version"),
        "requirements_hash": requirements_hash,
        "pkglist_hash": pkglist_hash,
        "upload_hash": files_hash,
        "conda_pkglist_hash": conda_pkglist_hash,
        "force_rebuild": config.build.force_rebuild,
        "init_debug": config.build.get("init_debug", False),
        # "pre_init_debug": pre_init_debug,
        "log_level": config.build.log_level,
        "disable_animation": config.build.disable_animation,
        "disable_build_logs": config.build.disable_build_logs,
        "disable_syntax_check": config.build.disable_syntax_check,
        "hide_public_endpoint": config.build.hide_public_endpoint,
        "predict_data": config.build.predict_data,
        "disable_predict": config.build.disable_predict,
        "partial_upload": config.get("partial_upload", False),
        "local_files": config.get("local_files", []),
    }

    backend_params = utils.remove_null_values(backend_params)
    setup_response = api._setup_app(
        headers={"Authorization": api_key},
        body=backend_params,
    )
    print(f"🆔 Build ID: {setup_response['buildId']}")
    build_status = setup_response["status"]
    if build_status == "pending":
        if config.partial_upload:
            uploaded_count = upload_files_to_s3(setup_response["uploadUrls"])
            upload_marker_file_and_delete(
                setup_response["markerFile"], uploaded_count, setup_response["buildId"]
            )
            stream_logs(
                config=config,
                api_key=api_key,
                setup_response=setup_response,
                hide_public_endpoint=config.build.hide_public_endpoint,
                is_run=cerebrium_function == "run",
            )
        else:
            zip_file_name = setup_response["keyName"]
            upload_url = setup_response["uploadUrl"]
            if api.upload_cortex_files(
                upload_url=upload_url,
                zip_file_name=zip_file_name,
                file_list=file_list,
                disable_syntax_check=config.build.disable_syntax_check,
                disable_animation=config.build.disable_animation,
                predict_data=config.build.predict_data,
                requirements=config.dependencies.pip,
                pkglist=config.dependencies.apt,
                conda_pkglist=config.dependencies.conda,
            ):
                stream_logs(
                    config=config,
                    api_key=api_key,
                    setup_response=setup_response,
                    hide_public_endpoint=config.build.hide_public_endpoint,
                    is_run=cerebrium_function == "run",
                )
    elif build_status == "running":
        print("🤷 No file changes detected. Getting logs for previous build...")
        stream_logs(
            config=config,
            api_key=api_key,
            setup_response=setup_response,
            hide_public_endpoint=config.build.hide_public_endpoint,
            is_run=cerebrium_function == "run",
        )
    else:
        cerebriumLog("ERROR", "No content has changed and previous build failed.")


@app.command()
def deploy(
    name: str = typer.Option("", help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    disable_syntax_check: bool = typer.Option(
        False, help="Flag to disable syntax check."
    ),
    gpu: str = typer.Option(
        "",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'AMPERE_A6000'. "
            "Can be one of "
            "'TURING_4000', "
            "'TURING_5000', "
            "'AMPERE_A4000', "
            "'AMPERE_A5000', "
            "'AMPERE_A6000', "
            "'AMPERE_A100'"
        ),
    ),
    cpu: Union[int, None] = typer.Option(
        None,
        min=datatypes.MIN_CPU,
        max=datatypes.MAX_CPU,
        help=(
            "Number of vCPUs to use for the Cortex deployment. Defaults to 2. "
            "Can be an integer between 1 and 48."
        ),
    ),
    memory: float = typer.Option(
        None,
        min=datatypes.MIN_MEMORY,
        max=datatypes.MAX_MEMORY,
        help=(
            "Amount of memory(GB) to use for the Cortex deployment. Defaults to 16. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: int = typer.Option(
        None,
        min=1,
        max=datatypes.MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. Defaults to 1. "
            "Can be an integer between 1 and 8."
        ),
    ),
    min_replicas: int = typer.Option(
        None,
        min=0,
        max=200,
        help=(
            "Minimum number of replicas to create on the Cortex deployment. "
            "Defaults to 0."
        ),
    ),
    max_replicas: int = typer.Option(
        None,
        min=1,
        max=200,
        help=(
            "A hard limit on the maximum number of replicas to allow. "
            "Defaults to 2 for free users. "
            "Enterprise and standard users are set to maximum specified in their plan"
        ),
    ),
    predict_data: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    python_version: str = typer.Option(
        "",
        help=(
            "Python version to use. "
            "Currently, we support '3.8' to '3.11'. Defaults to '3.10'"
        ),
    ),
    include: str = typer.Option(
        "",
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to exclude. "
        "Defaults to all hidden files/folders in project root.",
    ),
    cooldown: int = typer.Option(
        None,
        help="Cooldown period in seconds before an inactive replica of your deployment is scaled down. Defaults to 60s.",
    ),
    force_rebuild: bool = typer.Option(
        None,
        help="Force rebuild. Clears rebuilds deployment from scratch as if it's a clean deployment.",
    ),
    init_debug: bool = typer.Option(
        None,
        help="Stops the container after initialization.",
    ),
    log_level: Union[str, None] = typer.Option(
        None,
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    config_file: str = typer.Option(
        "",
        help="Path to cerebrium.toml file. You can generate a config using `cerebrium init-cortex`. The contents of the deployment config file are overridden by the command line arguments.",
    ),
    disable_confirmation: bool = typer.Option(
        False,
        help="Whether to disable the confirmation prompt before deploying.",
    ),
    disable_predict: Union[bool, None] = typer.Option(
        None, help="Flag to disable running predict function."
    ),
    disable_animation: bool = typer.Option(
        None,
        help="Whether to use TQDM and yaspin animations.",
    ),
    disable_build_logs: bool = typer.Option(
        False, help="Whether to disable build logs during a deployment."
    ),
    hide_public_endpoint: bool = typer.Option(
        False,
        help="Whether to hide the public endpoint of the deployment when printing the logs.",
    ),
):
    """
    Deploy a Cortex deployment to Cerebrium
    """
    gpu = gpu.upper() if isinstance(gpu, str) else gpu
    log_level = log_level.upper() if isinstance(log_level, str) else log_level

    config = verification.validate_cortex(
        name=name,
        gpu=gpu,
        cpu=cpu,
        memory=memory,
        gpu_count=gpu_count,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        python_version=python_version,
        include=include,
        exclude=exclude,
        cooldown=cooldown,
        force_rebuild=force_rebuild,
        init_debug=init_debug,
        log_level=log_level,
        disable_animation=disable_animation,
        disable_build_logs=disable_build_logs,
        disable_confirmation=disable_confirmation,
        disable_predict=disable_predict,
        disable_syntax_check=disable_syntax_check,
        hide_public_endpoint=hide_public_endpoint,
        config_file=config_file,
        predict_data=predict_data,
    )

    setup_app(
        api_key=api_key,
        config=config,
        cerebrium_function="deploy",
    )


@app.command()
def build(
    name: str = typer.Option("", help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    disable_syntax_check: bool = typer.Option(
        False, help="Flag to disable syntax check."
    ),
    gpu: str = typer.Option(
        "",
        help=(
            "Hardware to use for the Cortex deployment. "
            "Defaults to 'AMPERE_A6000'. "
            "Can be one of "
            "'TURING_4000', "
            "'TURING_5000', "
            "'AMPERE_A4000', "
            "'AMPERE_A5000', "
            "'AMPERE_A6000', "
            "'AMPERE_A100'"
        ),
    ),
    cpu: Union[int, None] = typer.Option(
        None,
        min=datatypes.MIN_CPU,
        max=datatypes.MAX_CPU,
        help=(
            "Number of vCPUs to use for the Cortex deployment. Defaults to 2. "
            "Can be an integer between 1 and 48."
        ),
    ),
    memory: Union[float, None] = typer.Option(
        None,
        min=datatypes.MIN_MEMORY,
        max=datatypes.MAX_MEMORY,
        help=(
            "Amount of memory(GB) to use for the Cortex deployment. Defaults to 16. "
            "Can be a float between 2.0 and 256.0 depending on hardware selection."
        ),
    ),
    gpu_count: Union[int, None] = typer.Option(
        None,
        min=1,
        max=datatypes.MAX_GPU_COUNT,
        help=(
            "Number of GPUs to use for the Cortex deployment. Defaults to 1. "
            "Can be an integer between 1 and 8."
        ),
    ),
    python_version: str = typer.Option(
        "",
        help=(
            "Python version to use. "
            "Currently, we support '3.8' to '3.11'. Defaults to '3.10'"
        ),
    ),
    predict: Union[str, None] = typer.Option(
        None,
        help="JSON string containing all the parameters that will be used to run your "
        "deployment's predict function on build to ensure your new deployment will work "
        "as expected before replacing your existing deployment.",
    ),
    include: str = typer.Option(
        "",
        help=(
            "Comma delimited string list of relative paths to files/folder to include. "
            "Defaults to all visible files/folders in project root."
        ),
    ),
    exclude: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to exclude. Defaults to all hidden files/folders in project root.",
    ),
    force_rebuild: Union[bool, None] = typer.Option(
        None,
        help="Force rebuild. Clears rebuilds deployment from scratch as if it's a clean deployment.",
    ),
    config_file: str = typer.Option(
        "",
        help="Path to cerebrium.toml file. You can generate a config using `cerebrium init-cortex`. The contents of the deployment config file are overridden by the command line arguments.",
    ),
    log_level: Union[str, None] = typer.Option(
        None, help="Log level for the Cortex build. Can be one of 'DEBUG' or 'INFO'"
    ),
    disable_confirmation: bool = typer.Option(
        False,
        help="Whether to disable the confirmation prompt before deploying.",
    ),
    disable_predict: Union[bool, None] = typer.Option(
        None, help="Flag to disable running predict function."
    ),
    disable_animation: Union[bool, None] = typer.Option(
        None,
        help="Whether to use TQDM and yaspin animations.",
    ),
    disable_build_logs: bool = typer.Option(
        False, help="Whether to disable build logs during a deployment."
    ),
    hide_public_endpoint: bool = typer.Option(
        False,
        help="Whether to hide the public endpoint of the deployment when printing the logs.",
    ),
):
    """
    Build and run your Cortex files on Cerebrium to verify that they're working as expected.
    """

    config = verification.validate_cortex(
        name=name,
        config_file=config_file,
        cpu=cpu,
        memory=memory,
        gpu_count=gpu_count,
        hide_public_endpoint=hide_public_endpoint,
        python_version=python_version,
        include=include,
        exclude=exclude,
        force_rebuild=force_rebuild,
        log_level=log_level,
        disable_animation=disable_animation,
        disable_build_logs=disable_build_logs,
        disable_syntax_check=disable_syntax_check,
        cerebrium_function="run",
        predict_data=predict,
        disable_confirmation=disable_confirmation,
        disable_predict=disable_predict,
    )

    setup_app(
        api_key=api_key,
        config=config,
        cerebrium_function="run",
    )
