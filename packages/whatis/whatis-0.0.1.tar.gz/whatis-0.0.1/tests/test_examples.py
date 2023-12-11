from whatis import whatis

class X:
    def __init__(self):
        self.shape = "banana"

# (object, kwargs, output) groups
objs = [
([[1, 2], [3, 4]], {"hor_spacing": 1},
"""
list len=2
 ├ list len=2
 │ ├ 1: int
 │ └ 2: int
 │
 ├ list len=2
 │ ├ 3: int
 └ └ 4: int
"""
),
({(1, 2): 2}, {"hor_spacing": 1},
"""
dict len=1
 ├ tuple len=2
 │ ├ 1: int
 │ └ 2: int
 └ └→ 2: int
"""
),
([{i:i for i in range(100)}], {},
"""
list len=1
  ├ dict len=100
  │  ├ 0: int
  │  ├ └→ 0: int
  │  │
  │  ├ 1: int
  │  ├ └→ 1: int
  │  │
  │  ├ 2: int
  │  ├ └→ 2: int
  │  │
  │  ├ 3: int
  │  ├ └→ 3: int
  │  │
  └  └ ...
"""
),
(X(), {"hor_spacing": 1},
"""
X shape=banana
"""
),
([(1, 5), {1: (2, 3), (4, 5): 6}, {3, 8}], {"hor_spacing": 1},
"""
list len=3
 ├ tuple len=2
 │ ├ 1: int
 │ └ 5: int
 │
 ├ dict len=2
 │ ├ 1: int
 │ ├ └→ tuple len=2
 │ │     ├ 2: int
 │ │     └ 3: int
 │ │
 │ ├ tuple len=2
 │ │ ├ 4: int
 │ │ └ 5: int
 │ └ └→ 6: int
 │
 ├ set len=2
 │ ├ 8: int
 └ └ 3: int
"""
),
([(1, 5), {1: (2, 3), (4, 5): 6}, {3, 8}], {"hor_spacing": 5},
"""
list len=3
     ├ tuple len=2
     │     ├ 1: int
     │     └ 5: int
     │
     ├ dict len=2
     │     ├ 1: int
     │     ├ └→ tuple len=2
     │     │         ├ 2: int
     │     │         └ 3: int
     │     │
     │     ├ tuple len=2
     │     │     ├ 4: int
     │     │     └ 5: int
     │     └ └→ 6: int
     │
     ├ set len=2
     │     ├ 8: int
     └     └ 3: int
"""
),
([(1, 5), {1: (2, 3), (4, 5): 6}, {3, 8}], {"unicode": False, "hor_spacing": 1},
"""
list len=3
 - tuple len=2
 | - 1: int
 | L 5: int
 |
 - dict len=2
 | - 1: int
 | - -> tuple len=2
 | |     - 2: int
 | |     L 3: int
 | |
 | - tuple len=2
 | | - 4: int
 | | L 5: int
 | L -> 6: int
 |
 - set len=2
 | - 8: int
 L L 3: int
"""
),
([(1, 5), {1: (2, 3), (4, 5): 6}, {3, 8}], {"show_index": True, "hor_spacing": 1},
"""
list len=3
 ├ 0 → tuple len=2
 │ ├ 0 → 1: int
 │ └ 1 → 5: int
 │
 ├ 1 → dict len=2
 │ ├ 1: int
 │ ├ └→ tuple len=2
 │ │     ├ 0 → 2: int
 │ │     └ 1 → 3: int
 │ │
 │ ├ tuple len=2
 │ │ ├ 0 → 4: int
 │ │ └ 1 → 5: int
 │ └ └→ 6: int
 │
 ├ 2 → set len=2
 │ ├ 0 → 8: int
 └ └ 1 → 3: int
"""
),
([{3:[1]*100},[1]*100], {},
"""
list len=2
  ├ dict len=1
  │  ├ 3: int
  │  ├ └→ list len=100
  │  │      ├ 1: int
  │  │      ├ 1: int
  │  │      ├ 1: int
  │  │      ├ 1: int
  │  └      └ ...
  │
  ├ list len=100
  │  ├ 1: int
  │  ├ 1: int
  │  ├ 1: int
  │  ├ 1: int
  └  └ ...
"""
),
([{3:[1]*4},[1]*4], {"rec_len_limit": 4},
"""
list len=2
  ├ dict len=1
  │  ├ 3: int
  │  ├ └→ list len=4
  │  │      ├ 1: int
  │  │      ├ 1: int
  │  │      ├ 1: int
  │  └      └ 1: int
  │
  ├ list len=4
  │  ├ 1: int
  │  ├ 1: int
  │  ├ 1: int
  └  └ 1: int
"""
)
]


def test_examples():
    for index, (obj, kwargs, out) in enumerate(objs):
        out_real = "\n".join(whatis(obj, display=False, **kwargs))
        out = out.strip()
        out_real = out_real.strip()
        if out != out_real:
            print("EXPECTED:")
            print(out)
            print("\nREAL:")
            print(out_real)
        assert out.strip() == out_real.strip(), f"Failed at index {index}"

