# Initialising arrays for the connections coming from:
# Learning Objectives, Assessments, Content and Learning Exercises
LOLines = []
AssessmentLines = []
ContentLines = []
LELines = []

LOLines = [[0, 1], 
            [0, 0],
            [1, 1],
            [0, 1]]

AssessmentLines = [[0, 1, 1, 0, 0, 1], 
                    [0, 0, 1, 1, 1, 1]]

ContentLines = [[1, 0, 0, 0], 
                [0, 1, 0, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 0, 0, 0]]

LELines = [[1, 1, 0, 0], 
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [1, 0, 1, 0]]

# Number of elements in each area
LOArr = ["LO1", "LO2", "LO3", "LO4"]
AssessmentArr = ["Ass1", "Ass2"]
ContentArr = ["Con1", "Con2", "Con3", "Con4", "Con5", "Con6"]
LEArr = ["LE1", "LE2", "LE3", "LE4"]

# Creates an matrix of all 0s for each set of relations
def EmptyMatrices():
    for i in range(len(LOArr)):
        newArr = []
        for j in range(len(AssessmentArr)):
            newArr.append(0)
        LOLines.append(newArr)

    for i in range(len(AssessmentArr)):
        newArr = []
        for j in range(len(ContentArr)):
            newArr.append(0)
        AssessmentLines.append(newArr)

    for i in range(len(ContentArr)):
        newArr = []
        for j in range(len(LEArr)):
            newArr.append(0)
        ContentLines.append(newArr)

    for i in range(len(LEArr)):
        newArr = []
        for j in range(len(LOArr)):
            newArr.append(0)
        LELines.append(newArr)

# Prints raw data in the form of a matrix
def PrintMatrices():
    print("\nLearning objectives to assessments")
    for i in range(len(LOArr)):
        for j in range(len(AssessmentArr)):
            # print("i:", i, "j:", j)
            # print(len(LOLines))
            print(LOLines[i][j],  end=" ")
        print("")

    print("\nAssessments to content")
    for i in range(len(AssessmentArr)):
        for j in range(len(ContentArr)):
            print(AssessmentLines[i][j], end=" ")
        print("")

    print("\nContent to learning exercises")
    for i in range(len(ContentArr)):
        for j in range(len(LEArr)):
            print(ContentLines[i][j],  end=" ")
        print("")

    print("\nLearning exercises to learning objectives")
    for i in range(len(LEArr)):
        for j in range(len(LOArr)):
            print(LELines[i][j],  end=" ")
        print("")

def LORelations():
    print("\nLearning objective to assessment relations:")
    for i in range(len(LOArr)):
        for j in range(len(AssessmentArr)):
            if (LOLines[i][j] == 1):
                print(LOArr[i], "is connected to", AssessmentArr[j])

def AssessmentRelations():
    print("\nAssessment to content relations:")
    for i in range(len(AssessmentArr)):
        for j in range(len(ContentArr)):
            if (AssessmentLines[i][j] == 1):
                print(AssessmentArr[i], "is connected to", ContentArr[j])

def ContentRelations():
    print("\nContent to learning exercise relations:")
    for i in range(len(ContentArr)):
        for j in range(len(LEArr)):
            if (ContentLines[i][j] == 1):
                print(ContentArr[i], "is connected to", LEArr[j])

def LERelations():
    print("\nLearning exercise to learning outcome relations:")
    for i in range(len(LEArr)):
        for j in range(len(LOArr)):
            if (LELines[i][j] == 1):
                print(LEArr[i], "is connected to", LOArr[j])

# EmptyMatrices()

PrintMatrices()

LORelations()
AssessmentRelations()
ContentRelations()
LERelations()