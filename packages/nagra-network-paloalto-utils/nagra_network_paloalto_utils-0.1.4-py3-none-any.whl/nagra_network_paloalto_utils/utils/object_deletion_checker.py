import logging
import re
from pathlib import Path

from . import rules_getter
from .panorama import get_all_device_groups

# PLAN = os.environ["PLAN"]

log = logging.getLogger("Object Deletion Checker")

# TF_PLAN_SUMMARY_REG = re.compile("Plan: \d* to add, \d* to change, \d* to destroy.\s")
# TF_UNCHANGED_REG = re.compile("\s*# \(\d* unchanged (blocks|attributes) hidden\)\s")
# TF_MUTATED_REG = re.compile('(^\s*# module(.\d*)*\["\S*"\] will be (updated in-place|created))')
# TF_DESTROYED_REG = re.compile("""(\s*# module(.\d*)*\["([^"]*)"\] will be destroyed)""")
TF_DESTROYED_REG = re.compile("""\s*# module.*\["([^"]*)"\] will be destroyed""")

def get_objects_to_delete(plan_file):
    with Path(plan_file).open() as tf:
        lines = tf.readlines()
    # Nb: Currently, the key used for the module is the name of the object
    # We can simply parse the line containing the acction (update,create,destroy)
    names = list(filter(None,(
        # Retrieve the names in quotes for entry to delete
        next(iter(TF_DESTROYED_REG.findall(l)), None)
        for l in lines
    )))
    return names


def get_all_used_objects(url, api_key):
    dgs = get_all_device_groups(url, api_key)

    data = []
    used_objects = []

    log.info("Getting all Security, NAT and PBF rules")
    for dg in dgs:
        sr = rules_getter.get_security_rules(url, api_key, dg)
        nat = rules_getter.get_nat_rules(url, api_key, dg)
        pbf = rules_getter.get_pbf_rules(url, api_key, dg)
        data.append(sr)
        data.append(nat)
        data.append(pbf)

    log.info("All rules pulled from Panorama!")
    for device in data:
        for rule in device:
            used_objects.extend(rule["source"]["member"])
            used_objects.extend(rule["destination"]["member"])
            # For NAT
            if rule.get("destination-translation"):
                used_objects.append(
                    rule["destination-translation"]["translated-address"],
                )
            if rule.get("source-translation"):
                try:
                    used_objects.append(
                        rule["source-translation"]["static-ip"]["translated-address"],
                    )
                except KeyError:
                    continue

    return list(dict.fromkeys(used_objects))
