## Module responsible
# for generathing ClothItem objects from a csv file
# 
# 
# @author Vlad Florea 

import enum
# Using enum class create enumerations

import csv
# We use csv to parse csv files

#Enum for representing cloth items type
class ClothType(enum.Enum):
   Pants = 1
   Top = 2
   Cap = 3
   Shoes = 4



#Class that represents a clothing item. It is used as a structure.
class ClothItem:
     #Constructor
    def __init__(self,id: int, clothtype: ClothType, name: str, minTemp: int, maxTemp: int, impermeability: bool): 
        self.id = id
        self.clothtype =clothtype 
        self.name = name
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.impermeability = impermeability

    def printMyself(self):
        #print(self.name)
        #print("minTemp:"+str(self.minTemp))
        #print("maxTemp:"+str(self.maxTemp))
        #print("Impermeability:"+str(self.impermeability))
        return (self.name)



#Defined list we use to compare with the csv header        
firstRow = ["Nr.Crt","Nume","Tip","Temperatura Minima","Temperatura Maxima","Impermeabilitate","Link Poza"]


#We use this function to generate a list of cloth items
def generateClothesFromCsv(csvPath: str):
    genClothes = []
    with open(csvPath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #Parse row by row
        for row in csv_reader:
            #First line contains the header cols
            if line_count == 0:
                if len(row) != len(firstRow):
                    print("The header of the csv is bad, wrong length")
                line_count += 1
            else:
                #Check the type against predefinted types
                clothStrType = row[2]
                actualType = None
                for crtType in ClothType:
                    if clothStrType == crtType.name:
                        actualType = crtType
                if(actualType == None):
                    print("Wrong type of cloth, unexpected! Type:"+clothStrType) 
                
                #Generate a new cloth item and add it to the list
                crtClothItem = ClothItem(int(row[0]),actualType,row[1],int(row[3]),int(row[4]),bool(row[5]))
                genClothes.append(crtClothItem)               
                line_count += 1
    return genClothes


#For test purposes
if __name__ == '__main__':
    csvPath ="../resources/Cloathes.csv"
    clothes =generateClothesFromCsv(csvPath)
    for cloth in clothes:
        cloth.printMyself()