import unittest

from measurement_check import check_measurements


GOOD_ORDER = {
    "fit_preference": "tapered",
    "fabric": "power stretch cotton",
    "measurements_cm": {
        "waist": 82,
        "hip": 98,
        "thigh": 58,
        "inseam": 74,
        "outseam": 102,
        "rise": 27,
    },
}


class MeasurementCheckTests(unittest.TestCase):
    def test_good_order_passes(self):
        result = check_measurements(GOOD_ORDER)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["score"], 100)

    def test_missing_measurement_needs_review(self):
        order = dict(GOOD_ORDER)
        order["measurements_cm"] = dict(GOOD_ORDER["measurements_cm"])
        del order["measurements_cm"]["thigh"]
        result = check_measurements(order)
        self.assertEqual(result["status"], "review")
        self.assertIn("missing or invalid thigh", result["flags"])

    def test_implausible_waist_is_flagged(self):
        order = dict(GOOD_ORDER)
        order["measurements_cm"] = dict(GOOD_ORDER["measurements_cm"], waist=20)
        result = check_measurements(order)
        self.assertTrue(any("waist outside" in flag for flag in result["flags"]))

    def test_inseam_must_be_shorter_than_outseam(self):
        order = dict(GOOD_ORDER)
        order["measurements_cm"] = dict(GOOD_ORDER["measurements_cm"], inseam=104)
        result = check_measurements(order)
        self.assertIn("inseam must be shorter than outseam", result["flags"])

    def test_missing_fit_preference_is_flagged(self):
        order = dict(GOOD_ORDER)
        del order["fit_preference"]
        result = check_measurements(order)
        self.assertIn("missing fit preference", result["flags"])

    def test_non_object_measurements_fail(self):
        result = check_measurements({"measurements_cm": "82"})
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["score"], 0)


if __name__ == "__main__":
    unittest.main()
