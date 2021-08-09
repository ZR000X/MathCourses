from math_courses import *

# set_metadata({
#     "author": "Tazzzz",
#     "title": "Taz Doos",
#     "date": "30 Doostember"
# })

# step = make_and_add_step(
#     title="First Step",
#     content=["Lada"],
#     env_type="Hi"
# )


# build_output(filename="TazDoos")

list_of_ordinals = []
def make_and_add(ords=[]):
    new_ord = Ordinal(ords)
    list_of_ordinals.append(new_ord)
    return new_ord

E = make_and_add()
D = make_and_add(E)
C = make_and_add(E)
B = make_and_add([C,D])
A = make_and_add([B,C,D])
E.subordinates.append(A)

for ord in list_of_ordinals:
    print(ord.get_rank())