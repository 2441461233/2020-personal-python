import unittest
import GHAnalysis


class MyTestCase(unittest.TestCase):
    def test_dataLoadIn(self):
        data = GHAnalysis.Data("testdata", reload=1)
        self.assertTrue(data.dataLoadIn("testdata"))

    def test_answerCheck(self):
        data = GHAnalysis.Data("testdata", reload=1)
        self.assertEqual(data.getEventsUsers("izuzero", "PushEvent"), 13)
        self.assertEqual(data.getEventsRepos("sheimi/SGit", "IssuesEvent"), 3)
        self.assertEqual(data.getEventsUsersAndRepos("petroav", "petroav/6.828", "CreateEvent"), 1)

if __name__ == "__main__":
    unittest.main()