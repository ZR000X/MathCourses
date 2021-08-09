from os import write
from typing import List
import math
import re

class Ordinal():
    # TODO: Fix the Ordinal Rank Method: Weird loops do weird things.

    """
    An ordinal is simply a set of all things it is greater than.
    """
    def __init__(self, subordinates=[], superiors=[], inform_on_init = True) -> None:
        if type(subordinates) is Ordinal:
            self.subordinates: List[Ordinal] = [subordinates]
        else:
            self.subordinates: List[Ordinal] = subordinates
        self.superiors = superiors
        if inform_on_init:
            self.inform_subordinates()
            self.inform_superiors()

    def __ge__(self, other):
        return other in self.subordinates

    def __le__(self, other):
        return self in other.subordinates

    def equals(self, other):
        return self >= other and other >= self

    def get_rank(self, superiors_asking=[]) -> int:
        """
        the rank of an ordinal is precisely one more than the maximum rank of its subordinates
        """
        # deal with empty lists
        if len(self.subordinates) == 0:
            return 0 
        # Loop through subordinates
        confused = False
        equals = []
        result = 0
        for sub in self.subordinates:
            # check that subordinate is not contradictory
            # Note: the original asker can never be confused
            if sub in superiors_asking:
                confused = True
                equals += [sub]
                continue
            # if not, get some return from the subordinate when asking rank
            rank = sub.get_rank(superiors_asking=superiors_asking + [self])
            # assess the return we got from asking rank
            if type(rank) is int:
                if rank >= result:
                    result = rank + 1
            else:
                if rank[0] >= result:
                    result = rank[0]
                equals += rank[1]
                # this subordinate continues the chain of confusion if it answers to superiors
                # if it sees itself in equals, however, it realises not to be confused
                if len(superiors_asking) > 0 and self not in equals:
                    confused = True                
        # decide what to return based on confusion
        if confused:
            return [result, equals]
        return result

    def get_depth(self, subordinates_asking=[]) -> int:
        """
        the depth of an ordinal is precisely one more than the maximum depth of its superiors
        """
        # deal with empty lists
        if len(self.superiors) == 0:
            return 0 
        # Loop through superiors
        confused = False
        equals = []
        result = 0
        for sup in self.superiors:
            # check that superior is not contradictory
            # Note: the original asker can never be confused
            if sup in subordinates_asking:
                confused = True
                equals += [sup]
                continue
            # if not, get some return from the superior when asking rank
            rank = sup.get_depth(subordinates_asking=subordinates_asking + [self])
            # assess the return we got from asking rank
            if type(rank) is int:
                if rank >= result:
                    result = rank + 1
            else:
                if rank[0] >= result:
                    result = rank[0]
                equals += rank[1]
                # this superior continues the chain of confusion if it answers to subordinates
                # if it sees itself in equals, however, it realises not to be confused
                if len(subordinates_asking) > 0 and self not in equals:
                    confused = True                
        # decide what to return based on confusion
        if confused:
            return [result, equals]
        return result

    def hire_subordinate(self, sub, inform_sub: bool = True):
        if inform_sub:
            if self not in sub.superiors:
                sub.superiors.append(self)
        self.subordinates.append(sub)            

    def inform_subordinates(self):
        """
        Ensures all subordinates are aware of their subordination
        """
        if self.subordinates is not None:
            for sub in self.subordinates:
                if type(sub) is not str and self not in sub.superiors:
                    sub.superiors.append(self)

    def inform_all_subordinates(self):
        self.inform_subordinates()
        for sub in self.subordinates:
            sub.inform_all_subordinates()

    def inform_superiors(self):
        """
        Ensures all superiors are aware of their superiority
        """
        if self.superiors is not None:
            for sup in self.superiors:
                if self not in sup.superiors:
                    sup.subordinates.append(self)
    
    def inform_all_superiors(self):
        self.inform_superiors()
        for sup in self.superiors:
            sup.inform_all_superiors()

    def is_root(self):
        return len(self.subordinates) == 0

    def is_peak(self):
        return len(self.superiors) == 0

    def get_roots(self, roots=[]):
        for sub in self:
            if sub is self or sub in roots:
                return []            
            if sub.is_root():
                roots.append(sub)
            else:
                roots += sub.get_roots(roots)
        return roots

    def get_peaks(self, peaks=[]):
        for sup in self.superiors:
            if sup is self or sup in peaks:
                return []            
            if sup.is_peak():
                peaks.append(sup)
            else:
                peaks += sup.get_peaks(peaks)
        return peaks

class MathCourseStep():
    """A MathCourseStep is the base type for what makes the sequence of steps of a MathCourse"""
    def __init__(self, title: str="", content: str="") -> None:
        self.title = title
        self.content = content       

class MathCourseObject(Ordinal, MathCourseStep):
    """A MathCourseObject is a MathCourseStep which are formal pieces of mathematical content."""
    def __init__(self, title: str="", content: str="", env_type=None, environment=None, proof=None, references=None) -> None:
        super().__init__(subordinates=references, superiors=[], inform_on_init=True)
        self.title = title
        self.content = content
        self.rank = 0
        if self.subordinates is not None:
            for sub in self.subordinates:
                if type(sub) is str:
                    self.rank = math.inf
                    break
                if sub.rank >= self.rank:
                    self.rank = sub.rank + 1
        self.proof = proof
        self.context_indices = {}
        self.env_type = env_type
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

class MathCourse(Ordinal):
    def __init__(self, title: str="", author: str="", date: str="", content: str="", references=None) -> None:
        super().__init__(subordinates=references, superiors=[], inform_on_init=True)
        self.title = title
        self.content = content
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

def sure_join(input, joiner=", ") -> str:
    """
    Input is either a string or a list
    """
    if input is None:
        return ""
    if type(input) is str:
        return input
    return joiner.join(input)

class ExternalReference():
    def __init__(self, title=None, authors=None, keywords=None) -> None:
        self.title: str = title
        self.authors: str = sure_join(authors)
        self.keywords: str = sure_join(keywords)

class ExtRefArticle(ExternalReference):
    def __init__(self, title=None, authors=None, keywords=None, journal=None, 
    volume=None, number=None, pages=None, year=None, DOI=None) -> None:
        super().__init__(title=title, authors=authors, keywords=keywords)
        self.journal: str = journal
        self.volume: str = volume
        self.number: str = number
        self.pages: str = pages
        self.year: str = year
        self.DOI: str = DOI

    def __str__(self):
        out = ""
        if self.authors is not None:
            out += self.authors+". "
        if self.title is not None:
            out += env_wrap("textit", self.title+". ")
        if self.year is not None:
            out += "("+self.year+"). "
        if self.journal is not None:
            out += "In: "+self.journal
        if self.volume is not None:
            out += "Vol. "+self.volume+". "
        if self.number is not None:
            out += "no. "+self.number+". "
        if self.pages is not None:
            out += "pgs. "+self.pages+". "
        if self.DOI is not None:
            out += self.DOI
        return out

class ExtRefBook(ExternalReference):
    def __init__(self, title=None, authors=None, keywords=None, 
    isbn=None, series=None, year=None, publisher=None) -> None:
        super().__init__(title=title, authors=authors, keywords=keywords)
        self.isbn: str = isbn
        self.series: str = series
        self.year: str = year
        self.publisher: str = publisher

    # TODO: add __str__ method

class ExtRefOnline(ExternalReference):
    def __init__(self, title=None, authors=None, keywords=None, url=None, addendum=None) -> None:
        super().__init__(title=title, authors=authors, keywords=keywords)
        self.url: str = url
        self.addendum: str = sure_join(addendum)

    # TODO: add __str__ method

class ExtRefInBook(ExternalReference):
    def __init__(self, title=None, authors=None, keywords=None, 
    publisher=None, year=None, chapter=None) -> None:
        super().__init__(title=title, authors=authors, keywords=keywords)
        self.publisher: str = publisher
        self.year: str = year
        self.chapter: str = chapter

    # TODO: add __str__ method

class ExternalReferences():
    def __init__(self, list_or_dict_of_references=None) -> None:
        self.dict_of_references = {}
        self.list_of_references = []
        if list_or_dict_of_references is not None:
            # constructor takes input and crafts both dict and ref
            if type(list_or_dict_of_references) is dict:
                self.dict_of_references = list_or_dict_of_references
                for value in list_or_dict_of_references.values():
                    if type(value) is not ExternalReference:
                        raise Exception("Trying to add non-ExternalReference to ExternalReferences.")
                    self.list_of_references.append(value)
            elif type(list_or_dict_of_references) is list:
                self.list_of_references = list_or_dict_of_references
                for ref in list_or_dict_of_references:
                    if not issubclass(type(ref), ExternalReference):
                        raise Exception("Trying to add non-ExternalReference to ExternalReferences.")
                    self.dict_of_references[ref.title] = ref
            elif list_or_dict_of_references is not None:
                raise Exception("Trying to create ExternalReference with neither list or dict.")
            else:
                self.list_of_references = None
                self.dict_of_references = None

    def __str__(self):
        if self.list_of_references is None:
            return ""
        out = r"""\section*{External References}"""+"\n"
        refs = []
        for ref in self.list_of_references:
            refs.append(str(ref))
        out += env_enum(refs, options=r"label={[\arabic*]}")
        return out

    def add_ref(self, ref, key=None):
        if not type(ref) is ExternalReference:
            raise Exception("Trying to add non-ExternalReference to ExternalReferences.")
        self.list_of_references.append(ref)
        if key is not None:
            self.dict_of_references[key] = ref
        else:
            self.dict_of_references[ref.title] = ref

    # TODO: Add more useful methods here.

# Initiate the universe and its metadata
u = MathCourse()
r = ExternalReferences()
def set_metadata(dict_meta_data):
    global u
    u.metadata = dict_meta_data

def set_external_references(list_or_dict_of_references):
    k = ExternalReferences(list_or_dict_of_references)
    r.list_of_references = k.list_of_references
    r.dict_of_references = k.dict_of_references

def make_step(title="", content="", env_type=None, environment=None, references=None, proof=None):
    if env_type is not None or environment is not None or references is not None or proof is not None:
        return MathCourseObject(title=title, content=content, environment=environment, env_type=env_type, references=references)
    else:
        return MathCourseStep(title=title, env_type=env_type, environment=environment, content=content, references=references)    
    
def add_step(step):
    u.add_step(step)

def make_and_add_step(title="", content=[], env_type=None, environment=None, references=None, proof=None):
    step = make_step(title=title, content=content, environment=environment, env_type=env_type, references=references, proof=proof)
    add_step(step)
    return step

def list_union(start_list, then_include) -> None:
    """
    This method ensures an output that includes everything from both lists
    """
    if type(then_include) is str:
        if then_include not in start_list:
            start_list.append(then_include)
    elif type(then_include) is list:
        for item in then_include:
            if item not in start_list:
                start_list.append(item)
    return start_list

def required_preamble(title: str, author: str, date: str):
    """
    Every output must contain this in the preamble
    """
    return [r"\documentclass{article}",
    r"\usepackage[utf8]{inputenc}",
    r"\usepackage{amsthm}",
    r"\usepackage{amsfonts}",
    r"\usepackage{breqn}",
    r"\usepackage{enumitem}",
    r"\usepackage{tcolorbox}",
    r"\title{"+title+"}",
    r"\author{"+author+"}",
    r"\date{"+date+"}"]

# If anyone is lazy to construct their own preamble, using this one should cover most needs
def default_preamble(title: str, author: str, date: str) -> List[str]:
    """
    This is the default preamble, which is a bit more than the required preamble
    """
    return list_union(
        start_list=required_preamble(title=title, author=author, date=date),
        then_include=[
            r"\usepackage{physics}"
        ]        
    )

### These methods help construct LaTeX code with minimal room for LaTex error
def env_wrap(environment: str, content: str, options=None) -> str:
    if options is not None:
        options = "["+options+"]"
    else:
        options = ""
    return r"\begin{"+environment+r"}"+options+content+r"\end{"+environment+r"}"

def wrap(wrapper: str, text: str) -> str:
    return wrapper+text+wrapper

def enclose(head: str = "", text: str = "") -> str:
    return "\\"+head+'{'+text+'}'

def env_enum(list_to_enum, options=None):
    out = ""
    for item in list_to_enum:
        out += r"\item "+item+"\n"
    return env_wrap(environment="enumerate", content=out, options=options)
 
def build_output(filename, title="", author="",
                 date="", universe=u, preamble=None, ext_refs=r):    
    # ensure input integrity
    if title == "":
        title = u.metadata['title']
    if author == "":
        author = u.metadata['author']
    if date == "":
        date = u.metadata['date']
    if preamble is None:
        preamble = default_preamble(title=title, author=author, date=date)
    else:
        preamble = list_union(required_preamble, preamble)
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
            if step.env_type is not None:
                thm = step.env_type
                must_be_in_preamble = r"\newtheorem{"+str(thm)+"}{"+str(thm[0].upper())+str(thm[1:])+"}"
                preamble.append(must_be_in_preamble)
                envs_in_preamble.append(thm)
                break
    first_env = envs_in_preamble[0]
    for step in universe.steps[count:]:
        if step.env_type is not None:
            thm = step.env_type
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
        if step.env_type is None:
            thm = "environment"
        else:
            thm = step.env_type
        if step.subordinates is None:
            to_append += "\n \n This "+thm+" has no references is thus rank $0$."
        elif type(step) is MathCourseObject:
            to_append += "\n \n This "+thm+" references: "
            for ref in step.subordinates:
                if type(ref) is str:
                    ext_refs: ExternalReferences
                    num = 0
                    for reff in ext_refs.list_of_references:
                        if reff.title == ref:
                            break
                        num += 1
                    to_append += r"[\ref{"+str(num)+r"}], "
                else:
                    to_append += r"(\ref{"+str(ref.get_index(u.metadata['title']))+r"}), "
            if step.rank == math.inf:
                write_step = r"$\infty$"
            else:
                write_step = str(step.rank)
            to_append += r"and is thus rank "+write_step+"."
        if step.env_type is not None:
            to_append = env_wrap(environment=step.env_type, options=step.title, content=to_append)
        if step.environment is not None:
            to_append = env_wrap(environment=step.environment, content=to_append)
        if type(step) is MathCourseObject:
            options = ""
            if step.env_type != "":
                options = "title="+step.env_type[0].upper()+step.env_type[1:]
            if step.title != "":
                options += ": " + step.title
            title = step.env_type + ": " + step.title
            to_append = env_wrap("tcolorbox", to_append, options=options)
        latex_output.append(to_append)

    latex_output.append(str(ext_refs))

    latex_output.append(r"\end{document}")

    with open("./bin/"+filename+".tex", "w") as file:
        for line in latex_output:
            file.write(line+"\n")
        file.close()

# TODO: Finish this

# def check_latex(input, square=True, ):
#     """
#     This string will automatically check the correctness of brackets,
#     as well as placeing "\left" and "\right" in front of them appropriately
#     """
#     if type(input) is str:
#         is_string_else_is_step = True
#     elif issubclass(type(input), MathCourseStep):
#         is_string_else_is_step = False
#     else:
#         raise Exception("Trying to check LaTeX of input neither string nor MathCourseStep.")
#     if not is_string_else_is_step:
#         iterate = input
#     else:
#         iterate = input.content
    
#     stack = [] # types of brackets: $, $$, {, [, (, \{ <-- last 3 should have \left & \right
#     out = iterate
#     for i in range(len(iterate)):
#         if iterate[i] == "$":
#             if i+1 < len(iterate) and iterate[i+1] == "$":
#                 if stack[-1] == "$$":
#                     stack.pop()
#                 else:
#                     stack.append("$$")
#             else:
#                 if stack[-1] == "$":
#                     stack.pop()
#                 else:
#                     stack.append("$")
#         elif iterate[i] == "{":
#             stack.append("{")
#         elif iterate[i] == "}":
#             if stack[-1] == "{":
#                 stack.pop()
#             else:
#                 if not is_string_else_is_step:
#                     raise Exception("LaTeX Error in step :: "+input.title+" :: Stack was "+sure_join(stack))
#         elif 
