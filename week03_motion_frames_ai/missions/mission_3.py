from pathlib import Path
import hashlib
from lab.models import RequirementResult, make_check

REFLECTIONS=('assumptions','problems','modifications','test_argument','remaining_limits','ai_disclosure','test_plan')


def current_hash(root):
    digest=hashlib.sha256()
    for p in sorted([*(root/'week03_pattern').rglob('*.py'),*(root/'test').rglob('*.py')]):
        digest.update(p.relative_to(root).as_posix().encode());digest.update(p.read_bytes())
    return digest.hexdigest()


def evaluate(result,lock,responses,source_root):
    source_root=Path(source_root)
    preserved=bool(lock.get('integrity_valid') and lock.get('source_sha256'))
    fresh=bool(result.get('source_sha256')==current_hash(source_root))
    files=all((source_root/p).exists() for p in ('week03_pattern/pattern.py','week03_pattern/pattern_node.py','test/test_student_pattern.py'))
    tests=bool(result.get('unit_tests_passed') and result.get('test_count',0)>=9)
    shape=bool(result.get('shape_check_passed') and result.get('pattern')==lock.get('pattern'))
    bounds=bool(result.get('commands_bounded') and result.get('model_stop_passed'))
    live=bool(result.get('integration_passed') and result.get('final_stop_verified'))
    pending=bool(responses.get('mission_3.live_pending') and str(responses.get('mission_3.live_issue','')).strip())
    explanations=all(str(responses.get(f'mission_3.{key}','')).strip() for key in REFLECTIONS)
    requirements=[
        RequirementResult('original','Original prompt, response, and source preserved',preserved,'preserved' if preserved else 'missing or changed','preserved'),
        RequirementResult('fresh','Evaluation matches current source and tests',fresh,'current' if fresh else 'rerun evaluator','current'),
        RequirementResult('files','Implementation and student tests present',files,files,'true'),
        RequirementResult('tests','Automated tests pass',tests,result.get('test_count',0),'>=9 passing'),
        RequirementResult('pattern','Assigned geometry and command limits verified',shape and bounds,shape and bounds,'true'),
        RequirementResult('revision','Implementation revised from preserved AI code',bool(result.get('source_differs_from_original')),result.get('source_differs_from_original',False),'true'),
        RequirementResult('live','Live verification completed or explicitly pending',live or pending,'verified' if live else ('pending' if pending else 'no evidence'),'verified or documented pending'),
        RequirementResult('analysis','Review, tests, and conclusions explained',explanations,'complete' if explanations else 'unfinished','complete'),
    ]
    return make_check('Your code, AI record, tests, and conclusions are documented.'+(' Live ROS verification remains pending.' if not live else ''),requirements)
