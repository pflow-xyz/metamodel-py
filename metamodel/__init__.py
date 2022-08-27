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

    def to_record(self):
        """ export to record format """
        places = [None]*len(self.places)
        for label, p in self.places.items():
            places[p['offset']] = (
                label, p['initial'], p['capacity'], p['offset'], (p['coords']['x'], p['coords']['y']))

        transitions = [0] * len(self.transitions)
        for label, t in self.transitions.items():
            guards = []
            for guard_label, guard_delta in t['guards'].items():
                guards.append((guard_label, guard_delta))
            transitions[t['offset']] = (
                label, t['delta'], guards, t['role'], (t['coords']['x'], t['coords']['y']))

        return (self.schema, places, transitions)

    @staticmethod 
    def from_record(r):
        (schema, places, transitions) = r
        
        def declaration(role, cell, fn):
            pass # empty

        m = Model(schema, declaration)

        for p in places:
            (label, initial, capacity, offset, coords) = p
            m.places[label] = { "label": label, "initial": initial, "capacity": capacity, "offset": offset, "coords": coords }

        for t in transitions:
            (label, delta, guards, role, coords) = t
            guard_map = {}
            for g in guards:
                (label, delta) = g
                guard_map[label] = delta

            m.transitions[label] = { "label": label, "delta": delta, "guards": guard_map, "role": role, "coords": coords }

        return m
