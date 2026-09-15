"""Reference scene and validation for the frame mission."""
import math
from datetime import datetime, timezone

TRANSFORM_KEYS = ("base_scan_to_base_link", "base_scan_to_odom")


def transform_point(x, y, tx, ty, yaw):
    return {"x": tx + math.cos(yaw)*x - math.sin(yaw)*y,
            "y": ty + math.sin(yaw)*x + math.cos(yaw)*y}


def reference_snapshot():
    return {"source":"reference", "captured_at":datetime.now(timezone.utc).isoformat(),
            "description":"Instructor-defined geometry; no live ROS frames were measured.",
            "frames":["odom","base_link","base_scan"],
            "transforms":{
                "base_scan_to_base_link":{"translation":{"x":.2,"y":0.,"z":0.},"yaw":0.},
                "base_scan_to_odom":{"translation":{"x":1.,"y":1.2,"z":0.},"yaw":math.pi/2}}}


def valid_snapshot(snapshot):
    if not isinstance(snapshot,dict) or not snapshot or snapshot.get("source") not in ("live","reference") or not snapshot.get("captured_at"):
        return False
    if not isinstance(snapshot.get("frames"),list) or not {"odom","base_link","base_scan"}.issubset(snapshot["frames"]):
        return False
    try:
        for key in TRANSFORM_KEYS:
            item=snapshot["transforms"][key]
            if not all(math.isfinite(float(v)) for v in (item["yaw"], *(item["translation"][axis] for axis in ("x","y","z")))):
                return False
    except (KeyError, TypeError, ValueError):
        return False
    return True


def correct_point(answer):
    try:
        return abs(float(answer["x"])) <= .03 and abs(float(answer["y"])+1) <= .03
    except (KeyError,TypeError,ValueError):
        return False
