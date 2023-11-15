molecules = { # molecule_name : [probability, {binding_parameters}]
    'molecule_a': [0.3, {0: 1,
                         1: 0.8}],
    'molecule_b': [0.6, {0: 1,
                         1: 0.6}],
    'molecule_c': [0.1, {0: 1,
                         1: 0.7}]
}

connectors = {
    'one': [0.05, {0: 0}],
    'two': [0.5, {0: 1,
                  1: 1}],
    'three': [0.45, {0: 1,
                    1: 1,
                    2: 1}]
}
