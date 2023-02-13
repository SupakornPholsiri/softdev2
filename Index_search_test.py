from Index import Index

index = Index()
searched = index.search("บทความ")

for info in searched:
    print(f"{info} : {searched[info]}")