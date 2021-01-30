import csv

with open('Cloathes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    cloathes = {} # In matricea asta o sa fie toate datele din csv, mai putin prima coloana cu numele
    # De exemplu: cloathes[0] e prima linie si cloathes[0][0] e nr crt=1 sau cloathes[0][1] sunt blugii
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            cloathes[line_count-1]=row
            line_count += 1
    print(cloathes[0][1])
    print(cloathes[1])