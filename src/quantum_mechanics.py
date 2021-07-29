from re import I
from math_courses import *

set_metadata(
    title="Quantum Mechanics",
    date="2021"
)

def_linear_vector_space = make_and_add_step(
    title="Linear Vector Space",
    thm_name="definition",
    content=[r"There are these axioms, you see..."]
)

def_field = make_and_add_step(
    title="Field",
    thm_name="definition",
    content=[r"A field is the numbers over which a vector space is defined."],
    references=[def_linear_vector_space]
)

def_linear_independence = make_and_add_step(
    title="Linear Independence of Vectors",
    thm_name="definition",
    content=[
        r"""A set of vectors $\mathbb{V}$ is said to be linearly independent if the only such
linear relation $$a_1v_1+a_2v_2+\ldots+a_nv_n=0,$$ where all $v_i\in\mathbb{V}$ and all
$a_i\in\mathbb{C}$, is the trivial one with all $a_i = 0$. If the set of vectors
is not linearly independent, we say they are linearly dependent. """
    ],
    references=[def_linear_vector_space]
)

def_dim_of_vs = make_and_add_step(
    title = "Vector Space Dimension",
    references=[def_linear_vector_space, def_linear_independence],
    thm_name="definition"
)

thm_1 = make_and_add_step(
    content=[r"""Any vector $\ket{V}$ in an $n$-dimensional space can be written as a
linear combination of $n$ linearly independent vectors $\ket{1}\ldots\ket{n}$."""],
    thm_name="theorem",
    references=[def_linear_vector_space, def_linear_independence, def_dim_of_vs]
)

def_basis = make_and_add_step(
    title="Vector Basis",
    content=[r"""A set of $n$ linearly independent vectors in an $n$-dimensional space
        is called a basis."""],
    thm_name="theorem",
    references=[def_linear_vector_space, def_linear_independence, def_dim_of_vs]
)

def_coords_wrt_a_basis = make_and_add_step(
    title="Coordinates of a Vector w.r.t. a Basis",
    content=[r"""The coordinates of a vector $\ket{v}$ in a basis $\{\ket{j_i}:i\in I\}$
    are the cooefficients of the expansion $$\ket{v}=v_1\ket{j_1}+\ldots+v_n\ket{j_n}$$ 
    of $\ket{v}$ in that basis."""],
    thm_name="definition",
    references=[def_basis, thm_1]
)

hamiltonian_spring_mass_system = make_and_add_step(
    content=[r"""The Hamiltonian $H$ of a spring-mass harmonic oscillator is given by"""+
    env_wrap("equation",r"H=\frac{p^2}{2m}+\frac{\omega^2x^2}{2}")+r"""
    where $\omega^2=k/m$ is the classical frequency of the oscillating system."""],
    thm_name="fact"
)

inverted_hamiltonian_spring_mass_system = make_and_add_step(
    content=[r"""The inverted harmonic oscillator changes the sign of the harmonic oscillator,
    so it has Hamiltonian"""+
    env_wrap("equation",r"H=\frac{p^2}{2m}-\frac{\omega^2x^2}{2}")+r"""
    where $\omega^2=k/m$ is the classical frequency of the oscillating system."""],
    thm_name="fact",
    references=[hamiltonian_spring_mass_system]
)

hamiltonian_spring_mass_system_adjust = make_and_add_step(
    content=[r"""Put $\omega^2=m^2-\lambda$, then $\lambda<m^2$ describes the
    regular harmonic oscillator and $\lambda>m^2$ describes the inverted one, while
    $m^2=\lambda$ is simply a free particle; that is, a particle such that its potential energy
    is independent of its position."""],
    thm_name="fact",
    references=[hamiltonian_spring_mass_system, inverted_hamiltonian_spring_mass_system]
)

eqn_evolution_system = make_and_add_step(
    content=[r"""Consider with the following system. 
    $$\psi(x,t)=\mathcal{N}(t)\exp\left(-\frac{1}{2}\omega_r x^2\right)$$
    with initial conditions $\psi(x,0)=\psi_0,~\mathcal{N}(0)=\mathcal{N}_0$, 
    and where $\omega_r=m$.""" ],
    thm_name="formula"
)

hermitian_operator = make_and_add_step(
    content=["""A Hermitian operator is an operator that is equal 
    to its own conjugate transpose."""],
    thm_name="definition"
)

hermitian_matrix = make_and_add_step(
    content=["""A Hermitian matrix is a complex square 
    matrix that is equal to its own conjugate transpose."""],
    thm_name="definition"
)

# expand_harmonic_oscillator_hamiltonian_by_taylor = make_and_add_step(
#     content=[r"""The harmonic oscillator Hamiltonian $$H=T+V=\frac{p^2}{2m}+\frac{\omega^2x^2}{2}$$
#     can have the potential expanded by Taylor series: $$]
# )

equations_of_motion_for_the_oscillator = make_and_add_step(
    thm_name="equations",
    content=[r"""The equations of motion for the oscillator are $$\dot{x}=
    \frac{\partial H}{\partial p}=\frac{p}{m},~~~~\dot{p}=-\frac{\partial H}{\partial x}=
    -m\omega^2 x$$ which, through elimination of $\dot{p}$, becomes
    $$\ddot{x}=-\omega^2x$$ which easily solves by
    $$x(t)=A\cos(\omega t+\phi)$$ where $x_0=x(0)=A\cos(\phi)$. Note then that
    $$E=T+V=\frac{1}{2}m\dot{x}^2+\frac{1}{2}m\omega^2x^2=\frac{1}{2}mA^2\omega^2$$
    where $E$ is the energy of the classical system."""],
    ##TODO: add more references
    references=[hamiltonian_spring_mass_system]
)

quantum_oscillator = make_and_add_step(
    thm_name="fact",
    content=[r"""The equation for a quantum oscillator with state $|\psi>$ is
    $$i\hbar\frac{d}{dt}\ket{\psi}=H\ket{\psi}$$"""]

)



build_output(
    filename="quantum_mechanics"
)