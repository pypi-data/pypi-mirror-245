from __future__ import annotations

import asyncio
import logging

from vortex.models import DesignObject
from vortex.models import DesignObjectAmbiguousError
from vortex.models import DesignObjectNotFound
from vortex.models import PuakmaServer
from vortex.spinner import Spinner
from vortex.util import render_objects
from vortex.workspace import Workspace

logger = logging.getLogger("vortex")


async def _acopy_obj(
    workspace: Workspace,
    server: PuakmaServer,
    spinner: Spinner,
    obj: DesignObject,
    copy_params: bool,
) -> int:
    _err_msg = f"Failed to copy {obj} to {obj.app.id}"
    to_app = obj.app
    try:
        indx, existing_obj = to_app.lookup_design_obj(obj.name)
    except DesignObjectAmbiguousError as e:
        logger.warning(f"{_err_msg}: {e}")
        return 1
    except DesignObjectNotFound:
        # Create a new object
        obj.id = -1
        ok = await obj.acreate_or_update(server.app_designer)
        if not ok:
            logger.error(f"{_err_msg} Unable to create Design Object {obj}")
            return 1

        if copy_params:
            await obj.acreate_params(server.app_designer)

        to_app.design_objects.append(obj)
    else:
        # Update the existing object
        spinner.stop()
        print(f"Design Object {obj} already exists in {obj.app}.")
        print("Only the Design data/source will be updated.")
        if input("[Y/y] to continue:") not in ["Y", "y"]:
            logger.error("Operation Cancelled")
            spinner.start()
            return 1
        spinner.start()
        existing_obj.design_data = obj.design_data
        if obj.do_save_source:
            existing_obj.design_source = obj.design_source
        to_app.design_objects[indx] = existing_obj
        obj = existing_obj

    workspace.mkdir(to_app)

    tasks = []
    if obj.do_save_source:
        upload_src_task = asyncio.create_task(
            obj.aupload(server.download_designer, True)
        )
        tasks.append(upload_src_task)
    upload_data_task = asyncio.create_task(obj.aupload(server.download_designer))
    tasks.append(upload_data_task)

    ret = 0
    for result in asyncio.as_completed(tasks):
        try:
            ok = await result
            ret |= 0 if ok else 1
        except (Exception, asyncio.CancelledError):
            for task in tasks:
                task.cancel()
            raise
    try:
        await asyncio.to_thread(obj.save, workspace)
    except OSError as e:
        logger.error(e.strerror)
        ret = 1

    return ret


async def _acopy_objects(
    workspace: Workspace,
    server: PuakmaServer,
    spinner: Spinner,
    objs_to_copy: list[DesignObject],
    copy_params: bool,
) -> int:
    async with server:
        await server.server_designer.ainitiate_connection()
        ret = 0
        tasks = []
        for obj_to_copy in objs_to_copy:
            task = asyncio.create_task(
                _acopy_obj(workspace, server, spinner, obj_to_copy, copy_params)
            )
            tasks.append(task)

        for result in asyncio.as_completed(tasks):
            try:
                ret |= await result
            except (Exception, asyncio.CancelledError) as e:
                logger.error(f"Operation Cancelled: {e}")
                for task in tasks:
                    task.cancel()
                ret = 1
                break
    return ret


def copy_(
    workspace: Workspace,
    server: PuakmaServer,
    obj_ids: list[int],
    to_app_id: int,
    copy_params: bool,
) -> int:
    to_app = workspace.lookup_app(server, to_app_id)
    objs = []
    # Initial Validation.
    # Object to copy must exist locally
    # Object musn't exist in the application we're copying to
    for obj_id in obj_ids:
        try:
            _, obj = workspace.lookup_design_obj(server, obj_id)
            if obj.app == to_app:
                logger.warning(
                    f"Unable to copy {obj}: "
                    f"Object already exists in application {to_app} [{to_app.id}]"
                )
            else:
                obj.app = to_app
                objs.append(obj)
        except (DesignObjectNotFound, DesignObjectAmbiguousError) as e:
            logger.warning(f"Unable to copy object with ID '{obj_id}': {e}")
            return 1

    if not objs:
        logger.error("No objects to copy")
        return 1

    print(f"The following Objects will be copied to {to_app}:\n")
    render_objects(objs, show_params=copy_params)
    if input("\n[Y/y] to continue:") not in ["Y", "y"]:
        return 1

    with (
        workspace.exclusive_lock(),
        Spinner("Copying...") as spinner,
    ):
        return asyncio.run(
            _acopy_objects(workspace, server, spinner, objs, copy_params)
        )
