import math
import unittest
from lab.frame_learning import reference_snapshot,valid_snapshot,transform_point,correct_point


class FrameLearningTests(unittest.TestCase):
    def test_sensor_body_and_odom_agree(self):
        body=transform_point(-.2,-1,.2,0,0)
        self.assertAlmostEqual(body['x'],0)
        self.assertAlmostEqual(body['y'],-1)
        world=transform_point(body['x'],body['y'],1,1,math.pi/2)
        self.assertAlmostEqual(world['x'],2)
        self.assertAlmostEqual(world['y'],1)

    def test_wrong_interpretation_destination(self):
        wrong=transform_point(2,1,1,1,math.pi/2)
        self.assertAlmostEqual(wrong['x'],0)
        self.assertAlmostEqual(wrong['y'],3)

    def test_snapshot_requires_complete_finite_transforms(self):
        data=reference_snapshot()
        self.assertTrue(valid_snapshot(data))
        data['transforms']['base_scan_to_odom']['yaw']=float('nan')
        self.assertFalse(valid_snapshot(data))
        self.assertFalse(valid_snapshot({'source':'live','captured_at':'today','frames':None}))
        self.assertFalse(valid_snapshot({}))

    def test_calculation_feedback(self):
        self.assertTrue(correct_point({'x':0,'y':-1}))
        self.assertFalse(correct_point({'x':2,'y':1}))
        self.assertFalse(correct_point({'x':float('nan'),'y':-1}))
