from math_courses import *

set_metadata(
    title="Algebra Story",
    author="Zeddar",
    date="2021-07-18"
)

def_naturals = make_and_add_step(
    title= "Counting, or Natural, Numbers",
    definition=True,
    content=[r"""The set of counting numbers is formed via the process of counting. We define them
    using the base 10 version of the arabic numeral system, as the set $\mathbb{N}$, defined by
    $$\mathbb{N}=\{1,2,3,4,5,6,7,8,9,10, 11, \ldots, 99, 100, 101, \ldots\}$$
    Each of these numbers can be understood as a discrete number of identical objects."""]
)

def_natural_addition = make_and_add_step(
    title= "Addition of Natural Numbers",
    definition=True,
    content=[r"""Once we can count, and have defined the natural numbers to decribe counts, we can
    define addition of two or more counts to be the total count, using continued counting. We use the 
    `$+$' symbol to denote the addition of however many counts $a,b,c,\ldots$, and denote 
    $$a+b+c+\ldots=C$$
    as the statement ``the sum of $a,b,c,\ldots$, that is, the total count found when counting 
    all of $a,b,c,\ldots$, is $C$."""],
    references=[def_naturals]
)

prop_some_adding_properties = make_and_add_step(
    title="",
    content=[r"""For any natural numbers $a,b\in\mathbb{N}$, we have"""+env_wrap("enumerate", r"""
    \item $a+b=b+a$
    \item $a+(b+c)=(a+b)+c$""")],
    proof=["Exercise."],
    references=[def_naturals, def_natural_addition]
)

def_sum_of_all_counts = make_and_add_step(
    title= "The Set of All Sums of Natural Numbers",
    definition=True,
    content=[r"""Consider every an all sums of any two natural numbers, defined by"""+
    mmath(r"\mathbb{N}+\mathbb{N}=\{a+b:a,b\in\mathbb{N}\}")],
    references=[def_naturals, def_natural_addition]
)

prop_all_natural_sums_are_natural = make_and_add_step(
    title="All Natural Sums are Natural",
    content=[r"""We have that """+mmath(r"\mathbb{N}+\mathbb{N}\subseteq\mathbb{N}")+"""and, further,
    in fact, """+mmath(r"\mathbb{N}+\mathbb{N}=\mathbb{N}\setminus\{1\}")],
    proof=["Exercise."],
    references=[def_naturals, def_natural_addition, def_sum_of_all_counts]
)

prop_counting_system = make_and_add_step(
    title="Counting System",
    content=[r"""We now summarise what we have so far and encapsulate it as the counting system.
    Let $a,b,c$ be arbitrary natural numbers.""" +
    env_wrap("enumerate", r"""
    \item (Natural Numbers) """+ math(r"\mathbb{N}=\{1,2,3,\ldots\}") + """
    \item (Commutativity) $a+b=b+a$
    \item (Associativity) $(a+b)+c=a+(b+c)=a+b+c$,
    \item (Closure of Natural Addition) $a+b\in\mathbb{N}$
    \item (Natural Sums) $\mathbb{N}+\mathbb{N}=\{a+b:a,b\in\mathbb{N}\}$
    \item (Closure of Natural Addition) $\mathbb{N}+\mathbb{N}\subset\mathbb{N}$""")],
    proof=["These can be neatly proven with the references."],
    references=u.progression[:-1]
)

def_subtraction = make_and_add_step(
    title="subtraction",
    definition=True,
    content=[r"""For arbitrary $a,b,c\in\mathbb{N}$, we let $$a+b=c\Rightarrow c-b=a$$
    where `$-$' is the subtraction operation."""],
    references=[def_naturals, def_natural_addition]
)
# - Define a+b=c to imply c-b=a, and trivially prove c-a=b follows.
# - The set N-N of all differences of natural numbers.
# -- Show that N is a subset of N-N.
# -- What conditions have arbitrary x in N-N also be natural, when not?
# -- Define -N={-n : n in N, -(a-b)=b-a for all a,b in N}
# -- Define 0=x-x for all x in N.
# -- Prove that N-N=-N or {0} or N, using a>b->a-b is natural, and either a<b, a=b, a>b.
# -- We define N-N=Z, the integers, where Z+=N, the positive integers, and Z-=-N.
# - We can now solve any equation a+x=b where a,b are integers, with another integer x.
# - The set NN of the products of natural numbers, prove that NN=N.
# - The set ZZ of the products of integers, prove that ZZ=NZ=Z, where they are defined in the obvious way.
# -- We need that ab=bc, (ab)c=a(bc), and the multiplication rules...
# -- for all a,b natural, ab is natural, (-a)b=-(ab) is neg-natural, a(-b)=-(ab) is neg-natural, (-a)(-b)=ab is natural.
# ... TBC

build_output(
    filename="algebra_story"
)
