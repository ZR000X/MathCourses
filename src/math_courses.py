from typing import List
import re

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
    def __init__(self, title: str="", content: str="", thm_name=None, environment=None, references=None) -> None:
        super().__init__(title=title, content=content, references=references)
        self.context_indices = {}
        self.thm_name = thm_name
        self.environment = environment

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
    def __init__(self, title: str="", content: str="", thm_name=None, environment=None, proof=None, references=None) -> None:
        super().__init__(title=title, content=content, environment=environment, references=references, thm_name=thm_name)
        self.level = self.get_ref_level()
        self.proof = proof

    def get_ref_level(self):
        if self.references is None:
            return 0
        result = 0
        for ref in self.references:
            if not ref.level is None:
                ref_level = ref.level
            else:
                ref_level = ref.reccalc_ref_level()
            if ref_level >= result:
                result = ref_level + 1
        return result

    def reccalc_ref_level(self):
        """A level of a MCO is recrusively defined as one more than the max level
        of its references, and 0 if it has no references."""
        if self.references is None:
            return 0
        result = 0        
        for ref in self.references:
            ref_level = ref.reccalc_ref_level()
            if ref_level >= result:
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

# Initiate the universe and its metadata
u = MathCourse()
def set_metadata(title="", author="", date=""):
    """This method sets the universe metadata"""
    u.metadata['title'] = title
    u.metadata['author'] = author
    u.metadata['date'] = date

def make_step(title="", content="", thm_name=None, environment=None, references=None, proof=None):
    if thm_name is None:
        return MathCourseStep(title=title, thm_name=thm_name, environment=environment, content=content, references=references)    
    elif proof is not None: 
        return MathCourseObject(title=title, content=content, environment=environment, thm_name=thm_name, proof=TitleContent(title+" (Proof)", proof), references=references)
    return MathCourseObject(title=title, content=content, environment=environment, thm_name=thm_name, references=references)        

def add_step(step):
    u.add_step(step)

def make_and_add_step(title="", content=[], thm_name=None, environment=None, references=None, proof=None):
    step = make_step(title=title, content=content, environment=environment, thm_name=thm_name, references=references, proof=proof)
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
    r"\usepackage{physics}",
    ### metadata
    r"\title{"+title+"}",
    r"\author{"+author+"}",
    r"\date{"+date+"}"]

### These methods help construct LaTeX code with minimal room for LaTex error
def env_wrap(environment: str, content: str, title=None) -> str:
    if title is not None:
        title = "["+title+"]"
    else:
        title = ""
    return r"\begin{"+environment+r"}"+title+content+r"\end{"+environment+r"}"

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
    # ensure input integrity
    if title == "":
        title = u.metadata['title']
    if author == "":
        author = u.metadata['author']
    if date == "":
        date = u.metadata['date']
    if preamble is None:
        preamble = standard_preamble(title=title, author=author, date=date)
    latex_output = preamble

    envs_in_preamble = []
    for item in preamble:
        if r"\newtheorem{" in item:
            item_shrink = item.replace(r"\newtheorem{", "")
            thm = item_shrink[:item_shrink.index("}")]
            envs_in_preamble.append(thm)
    count = 0
    if len(envs_in_preamble) == 0:
        for step in universe.steps:
            count += 1
            if step.thm_name is not None:
                thm = step.thm_name
                must_be_in_preamble = r"\newtheorem{"+str(thm)+"}{"+str(thm[0].upper())+str(thm[1:])+"}"
                preamble.append(must_be_in_preamble)
                envs_in_preamble.append(thm)
                break
    first_env = envs_in_preamble[0]
    for step in universe.steps[count:]:
        if step.thm_name is not None:
            thm = step.thm_name
            if thm not in envs_in_preamble:
                must_be_in_preamble = r"\newtheorem{"+str(thm)+"}["+str(first_env)+"]{"+str(thm[0].upper())+str(thm[1:])+"}"
                preamble.append(must_be_in_preamble)
                envs_in_preamble.append(thm)
    
    # add begin document stuff
    latex_output.append(r"\begin{document}"+"\n")
    latex_output.append(r"\maketitle"+"\n")
    
    # build the course step by step
    for step in universe.steps:
        if type(step.content) is not list:
            raise Exception("Content ::"+step.title+":: is not a list.")
        to_append = ""
        to_append += (enclose("label", str(step.get_index(u.metadata['title']))))
        
        to_append += re.sub(' +', ' '," ".join(step.content))
        if step.proof is not None:
            if type(step.proof) is not list:
                raise Exception("Proof ::"+step.proof.title+":: is not a list.")
            to_append.append(r"\begin{proof}")
            to_append += step.proof
            to_append.append(r"\end{proof}")
        if step.thm_name is None:
            thm = "environment"
        else:
            thm = step.thm_name
        if step.references is None:
            to_append += "\n \n This "+thm+" has no references and so has reference level $0$."
        elif type(step) is MathCourseObject:
            to_append += "\n \n This "+thm+" builds off of the following: "
            for ref in step.references:
                to_append += r"(\ref{"+str(ref.get_index(u.metadata['title']))+r"}), level "+str(ref.get_ref_level())+r", "
            to_append += r"and so has reference level "+str(step.get_ref_level())+"."
        if step.thm_name is not None:
            to_append = env_wrap(environment=step.thm_name, title=step.title, content=to_append)
        if step.environment is not None:
            to_append = env_wrap(environment=step.environment, content=to_append)
        latex_output.append(to_append)

    latex_output.append(r"\end{document}")

    with open("./bin/"+filename+".tex", "w") as file:
        for line in latex_output:
            file.write(line+"\n")
        file.close()
