import unittest
from metamodel import Models, Model
from examples import Counter, Pointer, TicTacToe
from metamodel.error import InvalidOutput, InvalidInput, GuardFail


class ModelTestCase(unittest.TestCase):

    def test_ref_by_schema(self):
        self.assertTrue(self, 'counter_v1' in Models)
        self.assertTrue(self, 'pointer_v1' in Models)

    def test_fire_counter(self):
        state = [0, 0]
        Counter.fire(state, 'inc0', 2)
        Counter.fire(state, 'inc1', 1)
        self.assertEqual(state, [2, 1])
        Counter.test_fire(state, 'inc1', 1)
        self.assertEqual(state, [2, 1])

    def test_counter_model(self):
        state, _ = Counter.transform([0, 0], 'inc0', 1)
        state, _ = Counter.transform(state, 'inc1', 3)
        self.assertEqual(state, [1, 3])

    def test_pointer_model(self):
        state, _ = Pointer.transform(Pointer.initial_vector(), 'create', 1)

        with self.assertRaises(InvalidInput):
            Pointer.transform(state, 'fake_action', 1)

        with self.assertRaises(InvalidOutput):
            Pointer.transform(state, 'create', 1)

        self.assertEqual(state, [1, 0, 0])
        state, _ = Pointer.transform(state, 'update', 1)
        self.assertEqual(state, [2, 0, 0])
        state, _ = Pointer.transform(state, 'disable', 1)
        self.assertEqual(state, [3, 1, 0])

        with self.assertRaises(GuardFail):
            Pointer.transform(state, 'update', 1)

        with self.assertRaises(InvalidOutput):
            Pointer.transform(state, 'disable', 1)

        state, _ = Pointer.transform(state, 'enable', 1)
        self.assertEqual(state, [4, 0, 0])

    def test_tic_tac_toe(self):
        state0, _ = TicTacToe.transform(TicTacToe.initial_vector(), 'X', 1)
        state1, _ = TicTacToe.transform(state0, '11', 1)
        state2, _ = TicTacToe.transform(state1, 'O', 1)
        TicTacToe.transform(state2, '01', 1)

    def test_record_conversion(self):
        rec = Counter.to_record()
        m = Model.from_record(rec)

        self.assertEqual(m.initial_vector(), Counter.initial_vector())
