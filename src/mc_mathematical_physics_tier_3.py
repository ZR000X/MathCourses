from re import I
from math_courses import *

set_metadata({
    "author": "Zeddar",
    "association": "Indie Academy Discord Server",
    "title": "Mathematical Physics",
    "date": "2021"
})

set_external_references(
    [
        
    ]
)

def_simple_harmonic_oscillator = make_and_add_step(
    title="Simple Harmonic Oscillator",
    env_type="definition",
    content=[r"Observe the wave $$\psi(x,t)=e^{i(\omega t-kx)}$$ where "
    r"$\omega=\frac{2\pi}{T}$ is the frequency in $t$, while $T$ is the period in $t$, " 
    r"$k=\frac{2\pi}{\lambda}$ is the frequency in $x$, while $\lambda$ is the period in $x$."]
)

def_poly_diff = make_and_add_step(
    title="Polynomial Differential Equation",
    env_type="Idea",
    content=[r"Take any polynomial $L(p,q)$ in $p,q$. Replacing $p$ with $\frac{\partial}{\partial t}$ "
    r"and $q$ with $\frac{\partial}{\partial x}$, getting an equation "
    r"$L\left(\frac{\partial}{\partial t},\frac{\partial}{\partial t}\right)\psi(x,t)=0$"],
    references=[def_simple_harmonic_oscillator]
)

def_general_fourier_series = make_and_add_step(
    title="General Fourier Series",
    env_type="definition",
    content=[r"On an interval $[-L,L]$, $$f(x)=\sum_{n=-\infty}^{\infty}F_n e^{-i\frac{\pi n}{L}x}$$"
    r"where $$F_n=\frac{1}{2L}\int_{-L}^L f(t)e^{i\frac{\pi n}{L}t}dt$$"
    ]
)

build_output(
    filename="mathematical_physics"
)