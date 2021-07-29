preamble = [r"\documentclass{article}",
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
    r"\newtheorem{question}[definition]{Question}"]

for item in preamble:
        if r"\newtheorem{" in item:
            item_shrink = item.replace(r"\newtheorem{", "")
            first_env = item_shrink[:item_shrink.index("}")]
            break

print(first_env)