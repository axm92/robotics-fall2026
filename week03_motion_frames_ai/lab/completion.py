"""Revalidate saved submissions against current answers, code, and evidence."""
import json
from pathlib import Path
from lab.autosave import submission_root
from lab.ai_log import load_lock
from lab.evidence import ai_evaluation,evidence_id
from missions import mission_1,mission_2,mission_3

SOURCE_ROOT=Path(__file__).resolve().parents[1]/'ros2_ws/src/week03_pattern'


def mission_status(st):
    responses=st.session_state.get('responses',{})
    checked=st.session_state.get('checked_evidence_ids',{})
    status={}
    for name in ('mission_1','mission_2','mission_3'):
        relevant={k:v for k,v in responses.items() if k.startswith(name+'.')}
        try:
            if name=='mission_1':
                current=evidence_id({k:v for k,v in relevant.items() if not k.startswith('mission_1.error.')})
                valid=mission_1.evaluate(list(responses.get('mission_1.results',{}).values()),responses).passed
            elif name=='mission_2':
                current=evidence_id(relevant)
                valid=mission_2.evaluate(responses.get('mission_2.snapshot',{}),responses).passed
            else:
                lock=load_lock();result=ai_evaluation()
                current=evidence_id(result,lock,relevant,mission_3.current_hash(SOURCE_ROOT))
                valid=mission_3.evaluate(result,lock,responses,SOURCE_ROOT).passed
            saved=json.loads((submission_root()/name/'submission.json').read_text(encoding='utf-8'))
            valid=valid and current==checked.get(name)==saved.get('evidence',{}).get('evidence_id')
            # An exported source file must still match its working copy.
            if name=='mission_3' and valid:
                for folder in ('week03_pattern','test'):
                    for source in (SOURCE_ROOT/folder).rglob('*.py'):
                        copy=submission_root()/name/'source'/source.relative_to(SOURCE_ROOT)
                        valid=valid and copy.read_bytes()==source.read_bytes()
            status[name]=bool(valid)
        except (OSError,ValueError,TypeError,KeyError):
            status[name]=False
    return status


def verification_summary(st):
    responses=st.session_state.get('responses',{})
    rows=[]
    for name in ('straight','turn_then_drive','arc'):
        source=responses.get('mission_1.results',{}).get(name,{}).get('source','missing')
        rows.append({'activity':'Mission 1: '+name.replace('_',' '),'evidence':source,'live_verified':source=='live'})
    source=responses.get('mission_2.snapshot',{}).get('source','missing')
    rows.append({'activity':'Mission 2: frames','evidence':source,'live_verified':source=='live'})
    result=ai_evaluation()
    live=bool(result.get('integration_passed') and result.get('final_stop_verified'))
    rows.append({'activity':'Mission 3: program','evidence':'live' if live else 'code/model tests; live pending','live_verified':live})
    return rows
