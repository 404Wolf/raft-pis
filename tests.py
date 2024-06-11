import unittest
import src.raftpiTests.nodeTests.log_test

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromModule(src.raftpiTests.nodeTests.log_test))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

