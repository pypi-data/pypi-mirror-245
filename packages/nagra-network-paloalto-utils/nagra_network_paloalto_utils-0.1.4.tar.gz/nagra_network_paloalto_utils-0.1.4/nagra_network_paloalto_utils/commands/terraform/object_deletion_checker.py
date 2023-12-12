import logging
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils.object_deletion_checker import (
    get_all_used_objects,
    get_objects_to_delete,
)

log = logging.getLogger(__name__)


@click.command()
@click.argument("planfile", type=Path, envvar="PLAN", default="plan.tfplan.txt")
def check_delete(planfile):
    """
    Check if the objects removed from the configuration are used somehwere
    """
    objects_to_check = get_objects_to_delete(planfile)

    if not objects_to_check:
        log.info("No objects to delete")
        return
    log.info(f"Attempting to delete the following objects: {objects_to_check}")

    log.info(f"Checking panorama for existing relations...")
    used_objects = get_all_used_objects()
    objects_in_use = list(set(used_objects) & set(objects_to_check))

    if objects_in_use:
        log.error(
            f"Some objects that you are trying to delete are still in use: {objects_in_use}",
        )
        exit(1)
    log.info("None of the object to delete are in use.")