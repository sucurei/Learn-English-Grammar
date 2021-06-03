(deffacts facts
        (waiting_input)
        (answer)
        (rule G1 S NN A)
        (rule G2 S NN EPS)
        (rule G3 A VBP B)
        (rule G4 A VBP C)
        (rule G5 A VBP D)
        (rule G6 A VBP E)
        (rule G7 A VBP D)
        (rule G8 A VBP EPS)
        (rule G9 B DT S)
        (rule G10 C NNP A)
        (rule G11 C NNP EPS)
        (rule G12 D TO I)
        (rule G13 D TO C)
		(rule G14 E NNS EPS)
		(rule G15 F RB EPS)
		(rule G16 G PRP A)
		(rule G17 G PRP H)
		(rule G18 H MD I)
		(rule G19 I VB B)
		(rule G20 I VB C)
		(rule G21 I VB D)
		(rule G21 J PRP EPS)
		(rule G22 S PRP A)
		(rule G23 A VBP S)
)

(defrule apply_rule
        (rule ?g ?nonterminal ?first ?next)
        ?a <- (text ?nonterminal ?first $?rest)
        ?b <- (answer $?steps)
        =>
        (assert (text ?next $?rest))
        (assert (answer $?steps ?g))

        (retract ?a)
        (retract ?b)
)

(defrule success
        ?a <- (text EPS)
        (answer $?steps)
        =>
        (assert (correct_state "YES"))
        (printout t "Seems to be CORRECT" $?steps crlf)

        (retract ?a)
)

(defrule failure
        ?a <- (text $?)
        =>
        (assert (wrong_state "NO"))
        (printout t "This sentence seems to be incorrect." crlf)

        (retract ?a)
)
