import unittest
from src.raftpi.node.node import NodeState
from src.raftpi.node.log import Term, NodeLog

class LogTest(unittest.TestCase):
    def test_get_term(self):
        term = Term()
        self.assertEqual(term.number, 0)

    def test_get_next_term(self):
        term = Term()
        nextTerm = term.next_term()
        self.assertEqual(nextTerm.number, 1)
        nextNextTerm = nextTerm.next_term()
        self.assertEqual(nextNextTerm.number, 2)

    def test_append(self):
        log = NodeLog(10, NodeState.FOLLOWER)
        self.assertEqual(log.get().state, NodeState.FOLLOWER)
        self.assertEqual(log.get().data, None)
        self.assertEqual(log.get().term.number, 0)

        log.append("test", NodeState.CANDIDATE)
        self.assertEqual(log.get().state, NodeState.CANDIDATE)
        self.assertEqual(log.get().data, "test")
        self.assertEqual(log.get().term.number, 1)
        
        log.append(1234, NodeState.LEADER)
        self.assertEqual(log.get().state, NodeState.LEADER)
        self.assertEqual(log.get().data, 1234)
        self.assertEqual(log.get().term.number, 2)

        print(log._log[1].state)
        self.assertEqual(log._log[1].state, NodeState.CANDIDATE)
        self.assertEqual(log._log[1].data, "test")
        self.assertEqual(log._log[1].term.number, 1)
