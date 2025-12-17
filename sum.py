import sys

if len(sys.argv) != 3:
    print("Erreur : deux arguments requis")
    sys.exit(1)

arg1 = float(sys.argv[1])
arg2 = float(sys.argv[2])

print(arg1 + arg2)
