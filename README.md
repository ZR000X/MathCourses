# MathCourses
A useful tool for coding LaTeX math courses in Python.

## How to use
The math_courses.py file offers any importing script with several convenient methods. Using these methods, the writer can construct a sequences of math course objects, such as definitions, propositions, or casual text, while linking previous objects to later objects with a list of pointers. This puts the mathematics in a certain structure within the code, which can later be utilised by the program to construct some interesting information about the structure of the math, while also printing equivalent latex code that can be compiled out-of-the-box.

## Reference levels
A particular interest in this project is, while building a course, to observe what is here called a "complexity level" of a piece of math. Granted that the way a course is built may hold some subjectivity in the hands of the author, and that this is not an exact measure of the inherent complexity of the math, it nevertheless makes for interesting study on its own. A goal of this project, besides offering easy-to-use writing tools, is to study these levels.

The definition of the complexity level of a math course object, for now, is one more than the maximum of the complexity levels of the object's references. This is thus a recursively defined property, and relies on accurate referencing. The base case is when an object has zero references: it then is given complexity level zero, and this is usually subject below "below the scope of the course", or initial definitions. As a guideline, whenever an object needs to mention another concept within the course in order to make sense, that other concept's object should be referenced.

As another guideline, one course should only reference

## How to contribute
It would be interesting to collaboratively build math courses that shared concepts. Therefore, contribute by tweaking math_courses.py or by adding new course files to the math_courses directory.

## License
Please see the accompanying license file.