

def parse(grammar, words):
  grammar = parse_bef(grammar)
  table, ambiguous = grammar.parsing_table(ls_crean = True)
  if ambiguous:
    raise Warning("es ambiguo")
