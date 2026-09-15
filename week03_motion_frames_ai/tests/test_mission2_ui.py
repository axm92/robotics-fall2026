import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest


@unittest.skipUnless(importlib.util.find_spec('streamlit'),'Streamlit is not installed')
class MissionTwoUI(unittest.TestCase):
    def test_reference_route_revision_save_and_stale_save(self):
        from streamlit.testing.v1 import AppTest
        from missions.mission_2 import REFLECTIONS
        app=AppTest.from_string('''
import streamlit as st
from lab.session import initialize
from pages.mission_2 import render
initialize(st)
render(st)
''',default_timeout=25).run()
        def click(label):
            button=next(b for b in app.button if b.label==label)
            self.assertFalse(button.disabled)
            button.click().run()
            self.assertFalse(app.exception)
        with patch('pages.mission_2.frame_snapshot',return_value={}):
            click('Load latest live snapshot')
            self.assertTrue(app.warning)
        click('Use reference snapshot')
        click('View heading 0°')
        click('View heading 90°')
        click('Check my transformation')
        self.assertFalse(app.session_state['responses']['mission_2.point_answer']['y']==-1)
        app.number_input[1].set_value(-1).run()
        click('Check my transformation')
        click('Show the wrong destination')
        for key in REFLECTIONS:
            app.text_area(key=f'm2.{key}').set_value('Explanation referring to the selected frame and example.').run()
        with tempfile.TemporaryDirectory() as directory,patch('lab.submissions.submission_root',return_value=Path(directory)):
            click('Check and save Mission 2')
            payload=json.loads((Path(directory)/'mission_2/submission.json').read_text())
            self.assertTrue(payload['evidence']['live_verification_pending'])
            self.assertEqual(payload['evidence']['snapshot']['source'],'reference')
            app.text_area(key='m2.safeguard').set_value('A revised safeguard with an explicit fallback.').run()
            self.assertFalse(any(b.label=='Continue to Mission 3' for b in app.button))
            click('Check and save Mission 2')
            click('Continue to Mission 3')
            self.assertEqual(app.session_state['stage'],'mission_3')
