from scaner import *

def first(rule):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'

    # condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            fres = []
            rhs_rules = diction[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            if '#' not in fres:
                return fres
            else:
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('#')
                return fres


def follow(nt):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows

    solset = set()
    if nt == start_symbol:
       
        solset.add('$')

    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                        res = first(subrule)
                        if res is not None:
                          if '#' in res:
                              newList = []
                              res.remove('#')
                              ansNew = follow(curNT)
                              if ansNew != None:
                                  if type(ansNew) is list:
                                      newList = res + ansNew
                                  else:
                                      newList = res + [ansNew]
                              else:
                                  newList = res
                              res = newList
                    else:
                        if nt != curNT:
                            res = follow(curNT)

                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


def computeAllFirsts():
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs

    print(f"\nGramatica: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")

    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        firsts[y] = t

    print("\nCalcular firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef,\
        term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalcular los follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1


def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef
    #print("\nTabla First y Follows\n")

    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2

    # print(f"{{:<{10}}} "
    #       f"{{:<{mx_len_first + 5}}} "
    #       f"{{:<{mx_len_fol + 5}}}"
    #       .format("Non-T", "FIRST", "FOLLOW"))
    # for u in diction:
    #     print(f"{{:<{10}}} "
    #           f"{{:<{mx_len_first + 5}}} "
    #           f"{{:<{mx_len_fol + 5}}}"
    #           .format(u, str(firsts[u]), str(follows[u])))

    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.append('$')

    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    grammar_is_LL = True

    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            if res is not None:
              if '#' in res:
                  if type(res) == str:
                      firstFollow = []
                      fol_op = follows[lhs]
                      if fol_op is str:
                          firstFollow.append(fol_op)
                      else:
                          for u in fol_op:
                              firstFollow.append(u)
                      res = firstFollow
                  else:
                      res.remove('#')
                      res = list(res) +\
                            list(follows[lhs])
              ttemp = []
              if type(res) is str:
                  ttemp.append(res)
                  res = copy.deepcopy(ttemp)
              for c in res:
                  xnt = ntlist.index(lhs)
                  yt = terminals.index(c)
                  if mat[xnt][yt] == '':
                      mat[xnt][yt] = mat[xnt][yt] \
                                     + f"{lhs}->{' '.join(y)}"
                  else:
                      if f"{lhs}->{y}" in mat[xnt][yt]:
                          continue
                      else:
                          grammar_is_LL = False
                          mat[xnt][yt] = mat[xnt][yt] \
                                         + f",{lhs}->{' '.join(y)}"

    #print("\nGenerar tabla parser:\n")
    # frmt = "{:>12}" * len(terminals)
    # print(frmt.format(*terminals))

    # j = 0
    # for y in mat:
    #     frmt1 = "{:>12}" * len(y)
    #     print(f"{ntlist[j]} {frmt1.format(*y)}")
    #     j += 1   
    

    return (mat, grammar_is_LL, terminals)




#-----------------

def validateStringUsingStackBuffer(parsing_table, grammarll1,
                                   table_term_list, input_string,
                                   term_userdef,start_symbol):

    print(f"\nCadena Test => {input_string}\n")
    conjunto_arbol = []
    if grammarll1 == False:
        return f"\nInput String = " \
               f"\"{input_string}\"\n" \
               f"Grammar is not LL(1)"


    stack = [start_symbol, '$']
    buffer = []

    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    print("{:>50} {:>50} {:>50}".
          format("Buffer", "Stack","Action"))

    while True:
        if stack == ['$'] and buffer == ['$']:
            print("{:>50} {:>50} {:>50}"
                  .format(' '.join(buffer),
                          ' '.join(stack),
                          "Valid"))
            return "\nCadena Valida", conjunto_arbol
        elif stack[0] not in term_userdef:
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != "":
                entry = parsing_table[x][y]
                print("{:>50} {:>50} {:>50}".
                      format(' '.join(buffer),
                             ' '.join(stack),
                             f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', "").strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                return f"\nInvalid String! No rule at " \
                       f"Table[{stack[0]}][{buffer[-1]}]."
        else:
            if stack[0] == buffer[-1]:
                print("{:>50} {:>50} {:>50}"
                      .format(' '.join(buffer),
                              ' '.join(stack),
                              f"Matched:{stack[0]}"))
                conjunto_arbol.append(stack[0])
                buffer = buffer[:-1]
                stack = stack[1:]
            else:
                return "\nCadena Invalida! " \
                       "Unmatched terminal symbols"

              
#---------------------
rules = ["S -> Program",
"Program -> Statement newline Statementlist",
"Statement -> for ( Typevar ; Expr ; Expr ) { newline Statementlist newline } | if ( Expr ) { newline Statementlist newline } else { newline Statementlist newline } | Typevar | Funciones ( ListId )",
"Statementlist -> Statement newline Statementlist | #",
"ListId -> id , ListId | #",
"Typevar -> Type id > cadena Stringlist",
"Type -> string | char",
"Stringlist -> cadena , Stringlist | #",
"Expr -> Orexpr",
"Orexpr -> Andexpr Orexprprime",
"Orexprprime -> or Andexpr Orexprprime | #",
"Andexpr -> Notexpr Andexprprime",
"Andexprprime -> and Notexpr Andexprprime | #",
"Notexpr -> Compexpr Notexprprime",
"Notexprprime -> not Compexpr Notexprprime | #",
"Compexpr -> Intexpr Compexprprime",
"Compexprprime -> CompOp Intexpr Compexprprime | #",
"Intexpr -> Factor Intexprprime",
"Intexprprime -> + Factor Intexprprime | - term Intexprprime | #",
"Factor -> - Factor | id | cadena | ( Expr )",
"Literal -> none | true | false",
"CompOp -> igualq | difq | menorq | mayorq",
"Funciones -> crack | mvp | localiza | saca | wachea"
]


nonterm_userdef=['S',
                 "Program",
                 "StatmentList",
                 "Statement",
                 "SimpleStatement",
                 "ListId",
                 "Typevar",
                 "Type",
                 "Stringlist",
                 "Expr",
                 "Orexpr",
                 "Orexprprime",
                 "Andexpr",
                 "Andexprprime",
                 "Notexpr",
                 "Notexprprime",
                 "Compexpr",
                 "Compexprprime",
                 "Intexpr",
                 "Intexprprime",
                 "Factor",
                 "Literal",
                 "CompOp",
                 "Funciones"
                 ]


term_userdef=[';',
              "newline",
              "for",
              "(",
              ")",
              ";",
              "{",
              "}",
              "if",
              "else",
              "id",
              ",",
              ">",
              "cadena",
              "string",
              "char",
              "bool",
              "or",
              "and",
              "not",
              "+",
              "-",
              "none",
              "true",
              "false",
              "igualq",
              "difq",
              "menorq",
              "mayorq",
              "crack",
              "mvp",
              "localiza",
              "saca",
              "wachea",
              ]

sample_input_string="string id > cadena newline wachea ( id , ) newline"


print("Scanner\n")
tokens = scan(sample_input_string)

for token in tokens:
    print(f" {token[0]}, Valor: {token[1]}, Línea: {token[2]}")


print("\n-----------------------------------------------\nParser\n")
diction = {}
firsts = {}
follows = {}


computeAllFirsts()

start_symbol = list(diction.keys())[0]

computeAllFollows()

(parsing_table, result, tabTerm) = createParseTable()

if sample_input_string != None:
  validity, conjunto_estados = validateStringUsingStackBuffer(parsing_table, result,
                      tabTerm, sample_input_string,
                      term_userdef,start_symbol)
  print(validity)
else:
  print("\nNo input String detected")



print("Listo para armar el arbol\n")
print(conjunto_estados)
