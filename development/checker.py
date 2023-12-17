with open("data/points2.csv") as f:
    data = [tuple(map(int, line.split(","))) for line in f.readlines()]

ids = set(d[0] for d in data)

pogledi = {i: set(d[0] for d in data if d[-1] == i) for i in range(4)}

intersections = {(i, j): pogledi[i] & pogledi[j] for i in range(4) for j in range(i + 1, 4)}

print(*(f"({i}, {j}) -> {intersections[i, j]}" for i, j in intersections), sep="\n\n")

diffs = {
    (i, j): (pogledi[i] - pogledi[j]) | (pogledi[j] - pogledi[i]) for i in range(4) for j in range(i + 1, 4)
}
print("diffs")
print(*(f"({i}, {j}) -> {diffs[i, j]}" for i, j in diffs), sep="\n\n")
