emptycounter = []
        for x in range(len(tokenized)):
            if tokenized[x] == "" or tokenized[x] == " " or tokenized[x] == "  " or tokenized[x] == "   ":
                emptycounter.append(x)
            else:
                continue
        for y in range(len(emptycounter)):
            del tokenized[y]