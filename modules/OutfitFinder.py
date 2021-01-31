#This module is responsabile for determining the best outfit from a 'wardrobe' based on the current weather
#Wether key parameters are 
# temperature,humidity,wind
# @author Vlad Florea

import ClothesFactory  
import random
import copy


#Defining the maximum numbers of iterations before giving up
HILL_CLIMB_MAX_ITERS = 1000000
HILL_CLIMB_REITERS = 100

#Defining a margin for determining wether is raining or not
rainMargin = 0.5 

#Defining an error increase basesd on the impermeability of the item
rainErrIncrease = 0.2

#Defining the importantness of each item as a percent 
hatPercentage = 0.10
pantsPercentage = 0.35
topPercentage =0.3
shoesPercentage= 0.25



#Class we use to encapsulate a forecast
class Forecast:
     #Constructor
    def __init__(self,temperature: float, humidity: float, wind: float): 
        self.temperature= temperature
        self.humidity=humidity
        self.wind=wind
        #Compute how the weather actually feels like
        #Probably not the best formula, but it does its job
        self.weatherFeelsLike = self.temperature - 0.2*self.wind - (self.temperature*self.humidity)/2

    
    def printMyself(self):
        print("Weather feels like:"+str(self.weatherFeelsLike))
        print("Temperature:"+str(self.temperature))
        print("Humidity:"+str(self.humidity))
        print("Wind:"+str(self.wind))
        


#Class we use to hold an outfit configuation
class ClothConfiguration:
    #Constructor
    def __init__(self, listOfHats: list, listOfPants: list, listOfTops: list, listOfShoes: list):
        #List with all the clothes
        self.hats = listOfHats
        self.pants= listOfPants
        self.tops = listOfTops
        self.shoes = listOfShoes     
        #Current indexes in the lists
        self.indexHats = None
        self.indexPants = None
        self.indexTops= None
        self.indexShoes= None

        #Start indexes, we need those to make sure we can parse all the space if necessary
        self.startIndexHats = None
        self.startIndexPants=None
        self.startIndexTops = None
        self.startIndexShoes=None

#Function that generates a random startConfiguration
def generateRandomClothConfig(startConfiguration: ClothConfiguration):
    startConfiguration.indexHats = random.randint(0, len(startConfiguration.hats)-1)
    startConfiguration.indexPants = random.randint(0, len(startConfiguration.pants)-1)
    startConfiguration.indexTops = random.randint(0, len(startConfiguration.tops)-1)
    startConfiguration.indexShoes = random.randint(0, len(startConfiguration.shoes)-1)

    startConfiguration.startIndexHats =startConfiguration.indexHats
    startConfiguration.startIndexPants=startConfiguration.indexPants
    startConfiguration.startIndexTops=startConfiguration.indexTops
    startConfiguration.startIndexShoes=startConfiguration.indexShoes

    return startConfiguration

#Function we use to compute the avg temperature
def computeAverageTemp(minTemp: float, maxTemp:float):
    return (minTemp+maxTemp)/2

#Function we use to check an outfit against the current weather
#@params: configuration -> current cloth configuration
#         forecast -> current forecast
#@returns: error -> computed error for the given configuration against the forecast
def checkConfig(configuration: ClothConfiguration,forecast:Forecast):
    #Check if its raining
    rainBool= False
    if(forecast.humidity > rainMargin):
        rainBool= True

    weatherFeelsLike = forecast.weatherFeelsLike
    #For each item, determine the error from the actual temperature to the average acceptance temperature (minTemp+maxTemp/2)
    hatErr=abs(computeAverageTemp(configuration.hats[configuration.indexHats].minTemp,configuration.hats[configuration.indexHats].maxTemp) - weatherFeelsLike)
    pantsErr=abs(computeAverageTemp(configuration.pants[configuration.indexPants].minTemp,configuration.pants[configuration.indexPants].maxTemp) - weatherFeelsLike)
    topErr=abs(computeAverageTemp(configuration.tops[configuration.indexTops].minTemp,configuration.tops[configuration.indexTops].maxTemp) - weatherFeelsLike)
    shoesErr=abs(computeAverageTemp(configuration.shoes[configuration.indexShoes].minTemp,configuration.shoes[configuration.indexShoes].maxTemp) - weatherFeelsLike)


    #If it rains and the item is not waterproof, increase the error by 20%
    if(rainBool == True):
        if(configuration.hats[configuration.indexHats].impermeability != True):
            hatErr+= hatErr*rainErrIncrease
        if(configuration.tops[configuration.indexTops].impermeability != True):
            topErr+= topErr*rainErrIncrease
        if(configuration.pants[configuration.indexPants].impermeability != True):
            pantsErr+= pantsErr*rainErrIncrease
        if(configuration.shoes[configuration.indexShoes].impermeability != True):
            pantsErr+= pantsErr*rainErrIncrease


    #Compute the actual error based on the defined importance percentages
    absErr = hatErr*hatPercentage + pantsErr*pantsPercentage + topErr*topPercentage + shoesErr*shoesPercentage
    return absErr


#Function we use to generate an available outfit using the hill climbing algorithm
#@params: csvPath: path to the csv file
#forecast: Forecast obj that holds the current weather
#@returns: crtConfig: ClothConfiguration object that holds the current configuration
def findWardrobe(csvPath: str, forecast:Forecast):
    wardrobe = ClothesFactory.generateClothesFromCsv(csvPath)

    #Make a list for each item type
    hatItems = []
    pantsItems=[]
    topItems=[]
    shoesItems=[]
    #Fill the lists 
    for item in wardrobe:
        if item.clothtype == ClothesFactory.ClothType.Cap:
            hatItems.append(item)
        elif item.clothtype == ClothesFactory.ClothType.Pants:
            pantsItems.append(item)
        elif item.clothtype == ClothesFactory.ClothType.Top:
            topItems.append(item)
        elif item.clothtype == ClothesFactory.ClothType.Shoes:
            shoesItems.append(item)

    #Generate a random configuration from the lists
    crtConfig = ClothConfiguration(hatItems, pantsItems, topItems,shoesItems)
    crtConfig = generateRandomClothConfig(crtConfig)

    minErr = checkConfig(crtConfig,forecast)
    iters = 0 
    while(iters < HILL_CLIMB_MAX_ITERS):
        #Move in the 'direction' of the hats

        #Make a hard coppy of the crt configuration
        newHatConfig= copy.deepcopy(crtConfig)

        #Update the crt configuration. Make sure we increment in a circular manner
        newHatConfig.indexHats = (newHatConfig.indexHats+1)%len(newHatConfig.hats)

        #Compute the newError
        newHatConfigErr= checkConfig(newHatConfig,forecast)
        
        #Check against the actual minimum
        if(newHatConfigErr < minErr):
            minErr=newHatConfigErr
            crtConfig = copy.deepcopy(newHatConfig)
            iters+=1
            continue

        #Move in the 'direction' of the tops in the same manner
        newTopConfig= copy.deepcopy(crtConfig)

        newTopConfig.indexTops=(newTopConfig.indexTops+1)%len(newTopConfig.tops)

        newTopConfigErr=checkConfig(newTopConfig,forecast)
        if(newTopConfigErr<minErr):
            minErr=newTopConfigErr
            crtConfig= copy.deepcopy(newTopConfig)
            iters+=1
            continue
        
        #Move in the 'direction' of pants in the same manner
        newPantsConfig=copy.deepcopy(crtConfig)

        newPantsConfig.indexPants=(newPantsConfig.indexPants+1)%len(newPantsConfig.pants)

        newPantsConfigErr=checkConfig(newPantsConfig,forecast)
        if(newPantsConfigErr<minErr):
            minErr=newPantsConfigErr
            crtConfig= copy.deepcopy(newPantsConfig)
            iters+=1
            continue
        
        #Move in the 'direction' of shoes in the same manner
        newShoesConfig=copy.deepcopy(crtConfig)

        newShoesConfig.indexShoes=(newShoesConfig.indexShoes+1)%len(newShoesConfig.shoes)

        newShoesConfigErr=checkConfig(newShoesConfig,forecast)
        if(newShoesConfigErr<minErr):
            minErr=newShoesConfigErr
            crtConfig= copy.deepcopy(newShoesConfig)
            iters+=1
            continue

        #If we didn't manage to find a new minimum by trying every direction then it means we reached a local minimum
        #print("Found a local minimum in:"+str(iters+1)+" iterations !")
        return crtConfig,minErr
    #print("Max no. of iters reached, probably there is a config better than this one in the proximity")
    return crtConfig,minErr



def HC(temp,humidity,wind):
	csvPath ="./resources/Cloathes.csv"
	testForecast = Forecast(temp,float(humidity/100),wind)
	crtConfig,crtErr = findWardrobe(csvPath,testForecast)
	for i in range(HILL_CLIMB_REITERS):
		newConfig,newErr = findWardrobe(csvPath,testForecast)
		if(newErr < crtErr):
			crtErr=newErr
			crtConfig=newConfig
	return crtConfig.hats[crtConfig.indexHats].printMyself(),crtConfig.tops[crtConfig.indexTops].printMyself(),crtConfig.pants[crtConfig.indexPants].printMyself(),crtConfig.shoes[crtConfig.indexShoes].printMyself()

#print(HC(30,0.2,4))
'''
#For testing
if __name__ == '__main__':
    csvPath ="../resources/Cloathes.csv"
    testForecast = Forecast(30,0.2,4)
    print("Current forecast is:")
    testForecast.printMyself()

    print("Running hill climb algorithm for " + str(HILL_CLIMB_REITERS)+ " times...")
    crtConfig,crtErr = findWardrobe(csvPath,testForecast)
    for i in range(HILL_CLIMB_REITERS):R
        newConfig,newErr = findWardrobe(csvPath,testForecast)
        if(newErr < crtErr):
            crtErr=newErr
            crtConfig=newConfig


    print("Hat:")
    crtConfig.hats[crtConfig.indexHats].printMyself()
    print("Top:")
    crtConfig.tops[crtConfig.indexTops].printMyself()
    print("Pants:")
    crtConfig.pants[crtConfig.indexPants].printMyself()
    print("Shoes:")
    crtConfig.shoes[crtConfig.indexShoes].printMyself()
'''