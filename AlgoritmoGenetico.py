import random
import operator
import time

population = [
    [44, 956, 126, 164, 263, 1447],
    [203, 797, 394, 245, 489, 872],
    [195, 805, 108, 161, 1690, 41],
    [121, 879, 323, 361, 1284, 32],
    [23, 977, 484, 151, 493, 872],
    [19, 981, 265, 425, 1105, 205],
    [289, 711, 52, 372, 185, 1391],
    [173, 827, 208, 294, 112, 1386],
    [69, 931, 33, 388, 770, 809],
    [371, 629, 28, 231, 357, 1384],
    [3, 997, 150, 347, 1226, 277],
    [232, 768, 329, 64, 1379, 228],
    [384, 616, 367, 412, 1208, 13],
    [39, 961, 240, 106, 1241, 413],
    [8, 992, 306, 275, 674, 745],
    [345, 655, 331, 136, 949, 584],
    [291, 709, 474, 448, 143, 935],
    [1, 999, 314, 265, 249, 1172],
    [135, 865, 11, 112, 1041, 836],
    [17, 983, 153, 333, 159, 1355],
]



'''
FUNCTIONS AND RESTRICTIONS
'''

def multiplyAndSumVarsForCoefs(vars, coefs):
    total = 0

    for i in range(0, len(coefs)):
        total += coefs[i] * vars[i]
    # End for

    return total
# End f

def fmin(idv):
    fminCoefs = [3.9, 3.0, 3.6, 4.3, 3.65, 4.35]
    return multiplyAndSumVarsForCoefs(idv, fminCoefs)
# End f

def validateRestriction(idv, coefs, op, compareTo):
    val = multiplyAndSumVarsForCoefs(idv, coefs)
    return op(val, compareTo)
# End validateRestriction

def countValidRestrictions(idv):
    totalValid = 0

    totalValid += 0 | validateRestriction(idv, [4, 4, 0, 0, 0, 0], operator.le, 8800) # Dpto D1
    totalValid += 0 | validateRestriction(idv, [1, 1, 3, 3, 3, 3], operator.le, 8800) # Dpto D2
    totalValid += 0 | validateRestriction(idv, [6, 0, 2, 2, 0, 0], operator.le, 8800) # Dpto E1
    totalValid += 0 | validateRestriction(idv, [0, 2, 0, 0, 3, 3], operator.le, 8800) # Dpto E2
    totalValid += 0 | validateRestriction(idv, [0, 0, 6, 0, 6, 0], operator.le, 8800) # Dpto F1
    totalValid += 0 | validateRestriction(idv, [4, 4, 0, 4, 0, 4], operator.le, 8800) # Dpto F2
    
    totalValid += 0 | validateRestriction(idv, [0.1, 0.1, 0.5, 0.5, 0.5, 0.5], operator.le, 2400) # Dpto F2
    totalValid += 0 | validateRestriction(idv, [0, 0, 1, 1, 1, 1], operator.eq, 2000) # Dpto F2
    totalValid += 0 | validateRestriction(idv, [1, 1, 0, 0, 0, 0], operator.eq, 1000) # Dpto F2

    return totalValid

# End validateAllRestrictions


'''
GENETIC ALGORITHM
'''

bestValue = 0
bestCountValidations = 0
bestAllTime = None

def orderAscMaxValidRestrictionsAndDescMinValue(population):
    sortCriteria = lambda idv:(countValidRestrictions(idv), -fmin(idv))
    population.sort(key = sortCriteria, reverse = True)
# End orderByMinValueAndMaxValidRestrictions

FIRST_PART_GENOTYPE_ALLOWED = 1000
SECOND_PART_GENOTYPE_ALLOWED = 2000

MUTATION_THRESHOLD = 0.8
CROSSOVER_THRESHOLD = 0.7
SAMPLE_SIZE = 10 # This must be pair
def getPopulationForNewGeneration(population):
    newPop = []

    sample = population[:SAMPLE_SIZE]
    for i in range(0, SAMPLE_SIZE // 2):
        kids = crossoverIndividuals(sample[i*2], sample[(i+1)*2 - 1])

        if len(kids) > 0: # Proceed with mutation
            kids = mutateIndividuals(kids)
            newPop += punishIndividuals(kids)
        # End if
    # End for

    return newPop + population[len(newPop):]
# End crossoverPopulation

def crossoverIndividuals(dad, mom):

    lenParent = len(dad)
    idx = 1
    while idx < lenParent:
        rdm = random.random()
        if (rdm >= CROSSOVER_THRESHOLD): break
        idx += 1
    # End while

    newIdvs = []
    if (idx < lenParent): # crossover happens
        first = dad[0:idx] + mom[idx:]
        second = mom[0:idx] + dad[idx:]
        newIdvs = [first, second]
    # End if
    
    return newIdvs
# End crossoverIndividuals

def mutateIndividuals(idvs):
    for idv in idvs:

        lenIdv = len(idv)
        idx = 0
        while idx < lenIdv:
            rdm = random.random()
            if (rdm >= MUTATION_THRESHOLD): break
            idx += 1
        # End while

        if (idx < lenIdv): mutateIndividualAtIdx(idv, idx)
        ensureMinimunConditionsAreReached(idv)
    # End for

    return idvs
# End mutateIndividuals

def mutateIndividualAtIdx(idv, idx):
    tot = comparableValue = 0

    if (idx < 2):
        tot = sum(idv[:2])
        comparableValue != FIRST_PART_GENOTYPE_ALLOWED
    else:
        tot = sum(idv[2:])
        comparableValue != SECOND_PART_GENOTYPE_ALLOWED
    # End if

    if tot > comparableValue:
        idv[idx] -= tot - comparableValue
    # End if

    return idv
# End mutateIndividualAtIdx

def ensureMinimunConditionsAreReached(idv):
    opt = list(idv)
    if sum(idv[:2]) != FIRST_PART_GENOTYPE_ALLOWED: 
        mutateToKeepSumFromTo(idv, FIRST_PART_GENOTYPE_ALLOWED, 0, 1)
    # End if

    if sum(idv[2:]) != SECOND_PART_GENOTYPE_ALLOWED: 
        mutateToKeepSumFromTo(idv, SECOND_PART_GENOTYPE_ALLOWED, 2, 5)
    # End if

    return idv
# End ensureMinimunConditionsAreReached


def mutateToKeepSumFromTo(idv, tot, start, end):
    for i in range(start, end):
        rdm = random.randint(0, tot)
        idv[i] = rdm
        tot -= rdm
    # End for

    idv[end] = tot
    return idv
# End mutateToKeepSumFromTo


def punishIndividuals(idvs):
    validIdvs = []

    for idv in idvs:
        filtered = list(filter(lambda g: g < 0, idv))
        if (len(filtered) == 0): validIdvs.append(idv)
    # End for

    return validIdvs
# End punishIndividuals

def init():
    global bestValue, bestCountValidations, bestAllTime, population

    orderAscMaxValidRestrictionsAndDescMinValue(population)

    bestAllTime = population[0]
    bestValue = fmin(bestAllTime)
    bestCountValidations = countValidRestrictions(bestAllTime)

    for gen in range(0, 1000000):
        # print("Running generation:", gen)
        population = getPopulationForNewGeneration(population)
        orderAscMaxValidRestrictionsAndDescMinValue(population)
        
        bestGeneration = population[0]
        minValue = fmin(bestGeneration)
        counValidations = countValidRestrictions(bestGeneration)
        # print("Best result for current gen", bestGeneration, minValue, counValidations , "\n")

        if (bestCountValidations < counValidations 
            or (bestCountValidations == counValidations and bestValue >= minValue)):

            bestCountValidations = counValidations
            bestValue = minValue
            bestAllTime = bestGeneration
        # End if

    # End for
# End init
start = time.time()
init()
print("BEST OF ALL generarions for current gen", bestAllTime, bestValue, bestCountValidations, "\n")
print('Finished in: ' + str(time.time() - start) + ' sec')