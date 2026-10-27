
import json
import unittest

from lambda_function import lambda_handler


class TestLambdaFunction(unittest.TestCase):

    def test_successful_job(self):
        event = {
            "Records": [{
                "body": json.dumps({
                    "job_id": "JOB-001",
                    "action": "process_order"
                })
            }]
        }

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["processed_count"], 1)
        self.assertEqual(body["results"][0]["job_id"], "JOB-001")
        self.assertEqual(body["results"][0]["status"], "success")

    def test_failed_job_raises_error(self):
        event = {
            "Records": [{
                "body": json.dumps({
                    "job_id": "JOB-002",
                    "simulate_failure": True
                })
            }]
        }

        with self.assertRaises(ValueError):
            lambda_handler(event, None)


if __name__ == "__main__":
    unittest.main()
