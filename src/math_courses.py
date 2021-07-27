from typing import List

class TitleContent():
    """
    A simple object which holds a title and some content.
    """
    def __init__(self, title:str="", content:str="") -> None:
        self.title = title
        self.content = content

class Referenceable(TitleContent):
    """
    A referenceable object has a title, some content, and a list of other references
    """

    def __init__(self, title:str="", content:str="", references=None) -> None:
        super().__init__(title=title, content=content)
        self.references: List[Referenceable] = references

    def get_references(self):
        return self.references

class MathCourseStep(Referenceable):
    """A MathCourseStep is a referenceable object placed within math courses"""
    def __init__(self, title: str="", content: str="", references=None) -> None:
        super().__init__(title=title, content=content, references=references)
        self.context_indices = {}

    def add_index(self, context, context_index) -> None:
        self.context_indices[context] = context_index

    def rem_index(self, context) -> None:
        del(self.context_indices[context])

    def get_index(self, context) -> object:
        return self.context_indices[context]

    def has_index(self, context, context_index) -> bool:
        return context in self.context_indices and context_index == self.get_index(context)

    def has_context(self, context) -> bool:
        return context in self.context_indices

class MathCourseObject(MathCourseStep):
    """A MathCourseObject is a MathCourseObject which can calculate base reference levels,
    as these are primarily meant to be pieces of formalised mathematics."""
    def __init__(self, title: str="", content: str="", references=None) -> None:
        super().__init__(title=title, content=content, references=references)
        self.level = self.get_base_ref_level()
        self.proof = None

    def get_base_ref_level(self):
        """A level of a MCO is recrusively defined as one more than the max level
        of its references, and 0 if it has no references."""
        if self.references is None:
            return 0
        result = 0        
        for ref in self.references:
            ref_level = ref.get_base_ref_level()
            if ref_level + 1 > result:
                result = ref_level + 1
        return result

class MathCourse(Referenceable):
    def __init__(self, title: str="", author: str="", date: str="", content: str="", references=None) -> None:
        super().__init__(title=title, content=content, references=references)
        self.steps: List[MathCourseObject] = []
        self.steps_dict = {}
        self.progression: List[MathCourseStep] = []
        self.metadata = {}
        self.metadata['title'] = title
        self.metadata['author'] = author
        self.metadata['date'] = date
        if references is None:
            self.references: List[MathCourse] = []
        else:
            self.references = references

    def add_step(self, step: MathCourseStep):
        if 'title' not in self.metadata:
            self.metadata['title'] = ""
        step.add_index(self.metadata['title'], len(self.steps))
        if issubclass(type(step),MathCourseObject):
            self.steps.append(step)
            self.steps_dict[step.title] = step
        self.progression.append(step)

class MathDefinition(MathCourseObject):
    def __init__(self, title: str="", content: str="", references=None) -> None:
        super().__init__(title=title, content=content, references=references)

class MathProposition(MathCourseObject):
    """This type of MCO is one that comes with a proof that shows its truth. The references
    of this MCO type is all the other MCOs in the Math Universe that are used in the proof."""
    def __init__(self, title: str="", content: str="", proof:TitleContent=None, references=None) -> None:
        super().__init__(title=title, content=content, references=references)
        self.proof = proof

# Initiate the universe and its metadata
u = MathCourse()
def set_metadata(title, author, date):
    """This method sets the universe metadata"""
    u.metadata['title'] = title
    u.metadata['author'] = author
    u.metadata['date'] = date

def make_step(title="", content="", definition=False, references=None, proof=None, object=True):
    if definition:
        return MathDefinition(title, content, references)
    elif proof is not None: 
        return MathProposition(title, content, TitleContent(title+" (Proof)", proof), references)
    elif object:
        return MathCourseObject(title, content, references)
    else:
        return MathCourseStep(title, content, references)

def add_step(step):
    u.add_step(step)

def make_and_add_step(title="", content="", definition=False, references=None, proof=None):
    step = make_step(title=title, content=content, definition=definition, references=references, proof=proof)
    add_step(step)
    return step

# If anyone is lazy to construct their own preamble, using this one should cover most needs
def standard_preamble(title: str, author: str, date: str) -> List[str]:
    return [r"\documentclass{article}",
    ### The packages are needed to run the code
    r"\usepackage[utf8]{inputenc}",
    r"\usepackage{amsthm}",
    r"\usepackage{amsfonts}",
    r"\usepackage{breqn}",
    ### declaration of theorem types
    r"\newtheorem{definition}{Definition}",
    r"\newtheorem{proposition}[definition]{Proposition}",
    r"\newtheorem{exercise}[definition]{Exercise}",
    r"\newtheorem{example}[definition]{Example}",
    r"\newtheorem{question}[definition]{Question}",
    ### metadata
    r"\title{"+title+"}",
    r"\author{"+author+"}",
    r"\date{"+date+"}"]

### These methods help construct LaTeX code with minimal room for LaTex error
def env_wrap(environment: str, text: str) -> str:
    return r"\begin{"+environment+r"}"+text+r"\end{"+environment+r"}"

def wrap(wrapper: str, text: str) -> str:
    return wrapper+text+wrapper

def math(text: str) -> str:
    return wrap(r" $ ", text)

def mmath(text: str) -> str:
    return wrap(r" $$ ", text)

def enclose(head: str = "", text: str = "") -> str:
    return "\\"+head+'{'+text+'}'
 
def build_output(filename, title="", author="",
                 date="", universe=u, preamble=None):
    if title == "":
        title = u.metadata['title']
    if author == "":
        author = u.metadata['author']
    if date == "":
        date = u.metadata['date']
    if preamble is None:
        latex_output = standard_preamble(title=title, author=author, date=date)
    else:
        latex_output = preamble

    def build_enviro(latex_output, step: MathCourseObject, type_name:str, proof=False, references=True):

        if type(step.content) is not list:
            raise Exception("Content is not a list.")
        if step.title is None:
            latex_output.append(enclose("begin", type_name))
        else:
            latex_output.append(enclose("begin", type_name)+"["+str(step.title+"]"))
        latex_output.append(enclose("label", str(step.get_index(u.metadata['title']))))
        latex_output += step.content
        if proof and step.proof is not None:
            latex_output.append(r"\begin{proof}")
            for line in step.proof.content:
                latex_output.append(line+"\n")
            latex_output.append(r"\end{proof}")
        if step.references is None:
            latex_output.append(r"This "+type_name+" had no references and so has base reference level $0$.")
        elif references:
            latex_output.append(r"This "+type_name+r" builds off of the following: ")
            for ref in step.references:
                ref: MathCourseObject
                latex_output.append(r"(\ref{"+str(ref.get_index(u.metadata['title']))+r"}), level "+str(ref.get_base_ref_level())+r", ")
            latex_output.append(r"and so has base reference level "+str(step.get_base_ref_level())+".")
        latex_output.append(r"\end{"+type_name+r"}")
        return latex_output
    
    latex_output.append(r"\begin{document}"+"\n")
    latex_output.append(r"\maketitle"+"\n")
    
    for step in universe.steps:
        if type(step) is MathDefinition:
            latex_output = build_enviro(latex_output=latex_output, step=step, type_name="definition")
        elif type(step) is MathProposition:
            latex_output = build_enviro(latex_output=latex_output, step=step, type_name="proposition", proof=True)
        else:
            latex_output += step.content

    latex_output.append(r"\end{document}")

    with open("./bin/"+filename+".tex", "w") as file:
        for line in latex_output:
            file.write(line+"\n")
        file.close()
