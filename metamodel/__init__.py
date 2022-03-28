from metamodel.error import UndefinedAction
from metamodel.metamodel import MetaModel
from metamodel.statemachine import StateMachine

Models = {}
"""
reference to all loaded models
"""


class Model(StateMachine):
    """
    Load a given model definition as a StateMachine
    """

    def __init__(self, schema, declaration):
        self.schema = schema
        mm = MetaModel()
        declaration(mm.role, mm.cell, mm.defun)
        mm.reindex()
        self.places = mm.places
        self.transitions = mm.transitions
        global Models
        Models[schema] = self

    def test_fire(self, state, action, multiple=1):
        role = self.transitions[action]['role']
        try:
            out, role = self.transform(state, action, multiple)
            return out, True, role
        except BaseException:
            return state, False, role

    def fire(self, state, action, multiple=1):
        out, ok, role = self.test_fire(state, action, multiple)
        if ok:
            for i, v in enumerate(out):
                state[i] = v
            return True, role
        else:
            return False, role
