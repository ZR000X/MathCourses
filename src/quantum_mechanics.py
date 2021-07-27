from math_courses import *

set_metadata(
    title="Quantum Mechanics",
    author="et. al.",
    date="2021"
)

def_linear_vector_space = make_and_add_step(
    title="Linear Vector Space",
    definition=True,
    content=[r"There are these axioms, you see..."]
)

def_field = make_and_add_step(
    title="Field",
    definition=True,
    content=[r"A field is the numbers over which a vector space is defined."],
    references=[def_linear_vector_space]
)

def_linear_independence = make_and_add_step(
    references=[def_linear_vector_space]
)

build_output(
    filename="quantum_mechanics"
)