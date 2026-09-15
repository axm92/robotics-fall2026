from lab.models import RequirementResult, make_check
from lab.frame_learning import valid_snapshot, correct_point

REFLECTIONS = ("frame_roles", "mounting", "point_meaning", "moving_coordinates",
               "wrong_source", "wrong_behavior", "consequence", "safeguard", "test_plan")


def evaluate(snapshot, responses):
    present=lambda key: bool(str(responses.get(f"mission_2.{key}","")).strip())
    roles=all(present(k) for k in ("frame_roles","mounting"))
    interpretation=all(present(k) for k in ("point_meaning","moving_coordinates"))
    diagnosis=all(present(k) for k in ("wrong_source","wrong_behavior"))
    safeguards=all(present(k) for k in ("consequence","safeguard","test_plan"))
    points=correct_point(responses.get("mission_2.point_answer",{}))
    checks=[
        RequirementResult("snapshot","Live or reference frame evidence selected",valid_snapshot(snapshot),snapshot.get("source","missing"),"live or reference"),
        RequirementResult("roles","Frame roles and mounting explained",roles,"complete" if roles else "unfinished","complete"),
        RequirementResult("point","Reference point converted into base_link",points,"checked" if points else "revise using worked example","(0, -1) m"),
        RequirementResult("interpretation","Coordinates compared at two headings",interpretation and responses.get("mission_2.compared",False),"complete" if interpretation and responses.get("mission_2.compared",False) else "unfinished","complete"),
        RequirementResult("diagnosis","Wrong-frame example inspected and explained",diagnosis and responses.get("mission_2.wrong_viewed",False),"complete" if diagnosis and responses.get("mission_2.wrong_viewed",False) else "unfinished","complete"),
        RequirementResult("safeguards","Consequence, safeguard, and test specified",safeguards,"complete" if safeguards else "unfinished","complete"),
    ]
    summary="You interpreted frames, transformed a point, and explained how to detect a frame mistake."
    if snapshot.get("source")=="reference":
        summary+=" Reference geometry was used; live frame inspection remains unverified."
    return make_check(summary,checks)
