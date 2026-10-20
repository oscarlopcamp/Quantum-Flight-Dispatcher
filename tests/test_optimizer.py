import unittest
from optimizer import compare_searches, decode, is_valid, valid_states
FLIGHTS=[{"code":"MX101","start":8,"end":10,"aircraft":"A320","allowed_gates":[0,1]},{"code":"MX205","start":9,"end":11,"aircraft":"E190","allowed_gates":[0,1]},{"code":"MX310","start":11,"end":13,"aircraft":"B787","allowed_gates":[1]},{"code":"MX415","start":12,"end":14,"aircraft":"A320","allowed_gates":[0,1]}]
class Tests(unittest.TestCase):
 def test_conflict(self): self.assertFalse(is_valid([0,0,1,0],FLIGHTS))
 def test_valid_states(self): self.assertTrue(all(is_valid(decode(s,4),FLIGHTS) for s in valid_states(FLIGHTS)))
 def test_grover(self):
  result=compare_searches(FLIGHTS,128); self.assertEqual(result["search_space"],16); self.assertGreater(result["quantum"]["success_probability"],50); self.assertLess(result["theoretical_grover"],16)
if __name__=="__main__": unittest.main()
