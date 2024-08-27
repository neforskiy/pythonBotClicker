async def Delete1stAndLastAndPreLastSymbolFromDBsQuery(string):
    string = str(string)
    str_new = string[:-1]
    str_middle = str_new[:-1]
    str_end = str_middle[1:]
    string = str(str_end)
    return string