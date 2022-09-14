from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse as urlparse
from urllib.parse import parse_qs
import requests
import stdiomask
import time
import sys
from collections import Counter

# Developed By Daniel Vaxman
# 3rd Year Computer Science Student - University of Windsor
# February 3rd - May 18th 2021
# IMPORTANT: Tool currently not functioning properly due to LMS update (Will fix)


URL = 'https://blackboard.uwindsor.ca'
redirectionURL = '/webapps/bb-mygrades-BBLEARN/myGrades?course_id=_'
courseNames = []
courseIDs = []
courseNav = {}
courseList = []

with requests.Session() as s:

    def nextUserInput(driver):
        option = input('\nWhat would you like to do now?\n1. Check grades for another course\n2. Exit\n\n')
        while not option.isdigit() or (int(option) != 1 and int(option) != 2):
            option = (input('\nInvalid Input!\nWhat would you like to do now?\n\n1. Check grades for another course\n2. Exit\n\n'))
        while int(option) == 1:
            for i in range(len(courseNames)):  # Prints course names
                print(f'{i + 1}. {courseNames[i]}')
            gradesOfCourse(driver)
            option = (input('\nWhat do you want to do now?\n\n1. Check grades for another course\n2. Exit\n\n'))
        else:
            exit(0)

    def displayCourseList(soup):
        for courses in soup.findAll('a'):  # Gets all course names
            fullCourseName = (''.join(courses.findAll(text=True)))
            indexOfSpace = fullCourseName.find(' ', 0, len(fullCourseName))
            courseCode = fullCourseName[0:indexOfSpace]
            courseNames.append(courseCode)
        courseNames.remove('Open')
        courseNames.remove('All')
        courseNames.remove('Last')
        print('Course List:\n')
        for i in range(len(courseNames)):  # Prints course names
            print(f'{i + 1}. {courseNames[i]}')
            courseList.append(f'{i + 1}. {courseNames[i]}')


    def gradesOfCourse(driver):

        markNames = ['Assignment', 'Lab', 'Quiz', 'Test', 'Midterm', 'Final Exam', 'Bonus', 'Other']
        gradeCategories = []
        achievedPointsOfCategory = []
        maxPointsOfCategory = []
        gradePercentageAsFloat = []
        gradePercentageAsString = []
        finalGradeCalculation = []
        nameOfGradeCategory = ""
        totalPossibleMarksOfGradeCategory = ""
        courseSelection = input("\nPlease enter course number for calculating grades: ")
        while not courseSelection.isdigit() or int(courseSelection) < 1 or int(courseSelection) > len(courseNames):
            courseSelection = input(f'Invalid Input! Please enter a number from 1-{len(courseNames)}: ')
        print('\nPlease input the total mark weight for each category: ')
        print('\nAssignments: \nLabs: \nQuizzes: \nMidterm Exam(s): \nFinal Exam: \nBonus (Optional): \nOther: \n')
        assignmentWeight = int(input('Assignments: '))
        labWeight = int(input('Labs: '))
        quizWeight = int(input('Quizzes: '))
        midtermExamWeight = int(input('Midterm Exam(s): '))
        finalExamWeight = int(input('Final Exam: '))
        bonusWeight = int(input('Bonus (Optional): '))
        otherWeight = int(input('Other: '))
        sumOfMarks = assignmentWeight + labWeight + quizWeight + midtermExamWeight + finalExamWeight + bonusWeight + otherWeight
        for i in range(1, len(courseNames) + 1): # Needs update
            if int(courseSelection) == i:
                time.sleep(1)
                driver.get(str(URL + redirectionURL + courseNav.get(courseNames[i - 1]) + '_1&stream_name=mygrades'))
                grades = driver.page_source
                displayGrades = BeautifulSoup(grades, 'html.parser')
                testArray = ['Assignment\n', 'Lab\n', 'Test\n', 'Discussion\n']
                gradeNames = []
                counter = 0
                test = "return document.querySelector('#grades_wrapper')" #IMPORTANT
                testOutput = driver.execute_script(test).text.replace('\n/', '/') #IMPORTANT
                indices = [x for x in range(len(testOutput)) if testOutput.startswith("/", x)]
                for j in range(len(indices)):
                    while testOutput[indices[8] + counter] != '\n':
                        if testOutput[indices[8] + counter] == '\n':
                            break
                        counter += 1
                    counter = 0


                nextUserInput(driver)
                for name in displayGrades.find_all('div', {'class': 'cell gradable'}):
                    for j in range(len(markNames)):
                        if name.find_all('a'):
                            nameOfGradeCategory += str(name.find_all('a')) # Have to fix this for future
                            if markNames[j] in nameOfGradeCategory:
                                gradeCategories.append(markNames[j])
                        elif name.find_all('div', {'class': 'itemCat'}):
                            nameOfGradeCategory += str(name.find_all('div', {'class': 'itemCat'}))
                            if markNames[j] in nameOfGradeCategory:
                                gradeCategories.append(markNames[j])
                        nameOfGradeCategory = ''

                for grade in displayGrades.find_all('div', {'class': 'cell grade'}):
                    if grade.find_all('span', {'class': 'grade'}):
                        marksOfGradeCategory = str(grade.find_all('span', {'class': 'grade'}))
                        endIndex = 0
                        for i in range(marksOfGradeCategory.find('>'), len(marksOfGradeCategory)):
                            if marksOfGradeCategory[i].__eq__('<'):
                                endIndex += i
                                temp = marksOfGradeCategory[marksOfGradeCategory.find('>') + 1: endIndex]
                                if temp.replace('.', '').isdigit():
                                    achievedPointsOfCategory.append(temp)
                                break
                startIndex = 1
                endIndex = 1
                for maxGrade in displayGrades.find_all('div', {'class': 'cell grade'}):
                    if maxGrade.find_all('span', {'class': 'pointsPossible clearfloats'}):
                        totalPossibleMarksOfGradeCategory += str(maxGrade.find_all('span', {'class': 'pointsPossible clearfloats'}))
                        while totalPossibleMarksOfGradeCategory[startIndex] != '>':
                            startIndex += 1
                        endIndex = startIndex
                        if totalPossibleMarksOfGradeCategory[startIndex] == '>':
                            while totalPossibleMarksOfGradeCategory[endIndex] != '<':
                                endIndex += 1
                    temp = totalPossibleMarksOfGradeCategory[startIndex + 1: endIndex].replace('/', '')
                    if temp.replace('.', '').isdigit():
                        maxPointsOfCategory.append(
                            totalPossibleMarksOfGradeCategory[startIndex + 1: endIndex].replace('/', ''))
                    totalPossibleMarksOfGradeCategory = ''

        for i in range(len(achievedPointsOfCategory)):
            percentageAsString = ''
            unformattedPercentage = (float(achievedPointsOfCategory[i])) / float(maxPointsOfCategory[i]) * 100
            percentage = '{:.2f}'.format(unformattedPercentage)  # Gets and converts each mark percentage to 2 decimal places
            percentageAsString += percentage
            gradePercentageAsString.append(percentageAsString + '%')
            gradePercentageAsFloat.append(percentage)

        numOfAssignments = 0
        numOfLabs = 0
        numOfQuizzes = 0
        numOfMidtermExamWithSpace = 0
        numOfMidtermExams = 0
        numOfFinalExams = 0
        numOfBonuses = 0
        numOfOther = 0

        for i in range(len(gradeCategories)):  # Determining amount of same elements (Only works for specific case have to change in future)
            if gradeCategories[i] in markNames[0]:
                numOfAssignments += 1
            elif gradeCategories[i] in markNames[1]:
                numOfLabs += 1
            elif gradeCategories[i] in markNames[2]:
                numOfQuizzes += 1
            elif gradeCategories[i] in markNames[3]:
                numOfMidtermExamWithSpace += 1
            elif gradeCategories[i] in markNames[4]:
                numOfMidtermExams += 1
            elif gradeCategories[i] in markNames[5]:
                numOfFinalExams += 1
            elif gradeCategories[i] in markNames[6]:
                numOfBonuses += 1
            elif gradeCategories[i] in markNames[7]:
                numOfOther += 1

        for i in range(len(gradeCategories)):  # Adds element names to list for later
            finalGradeCalculation.append(gradeCategories[i])
        numOfSameElements = Counter(gradeCategories)

        if(len(finalGradeCalculation).__eq__(0)):
            print('No grades detected!')
            gradesOfCourse(driver)
            
        # Var declaration for counting amount of times each element appears
        assignmentCounter = 0
        labCounter = 0
        quizCounter = 0
        midtermExamWithSpaceCounter = 0
        midtermExamCounter = 0
        finalExamCounter = 0
        bonusCounter = 0
        otherCounter = 0

        for name in numOfSameElements:  # Calculates the occurrence amount of each element
            if name in markNames[0]:
                assignmentCounter += numOfSameElements[name]
            elif name in markNames[1]:
                labCounter += numOfSameElements[name]
            elif name in markNames[2]:
                quizCounter += numOfSameElements[name]
            elif name in markNames[3]:
                midtermExamWithSpaceCounter += numOfSameElements[name]
            elif name in markNames[4]:
                midtermExamCounter += numOfSameElements[name]
            elif name in markNames[5]:
                finalExamCounter += numOfSameElements[name]
            elif name in markNames[6]:
                bonusCounter += numOfSameElements[name]
            elif name in markNames[7]:
                otherCounter += numOfSameElements[name]

        # Var declaration for individual weight of each element
        individualAssignmentWeight = 0
        individualLabWeight = 0
        individualQuizWeight = 0
        individualMidtermWithSpaceWeight = 0
        individualMidtermWeight = 0
        individualFinalWeight = 0
        individualBonusWeight = 0
        individualOtherWeight = 0
        elementCounter = [assignmentCounter, labCounter, quizCounter, midtermExamWithSpaceCounter, midtermExamCounter,
                          finalExamCounter, bonusCounter, otherCounter]
        elementNumCounter = dict(zip(markNames, elementCounter))  # Initializes dictionary where key = markNames[x], value = otherCounter[x]

        for key, value in list(elementNumCounter.items()):  # Removes all elements if their value (counter) equals 0 as it is impossible to divide by 0
            if value == 0:
                elementNumCounter.pop(key)

        for key, value in list(elementNumCounter.items()):  # Calculates weight of each individual element
            if key in markNames[0]:
                individualAssignmentWeight += assignmentWeight / assignmentCounter
            elif key in markNames[1]:
                individualLabWeight += labWeight / labCounter
            elif key in markNames[2]:
                individualQuizWeight += quizWeight / quizCounter
            elif key in markNames[3]:
                individualMidtermWithSpaceWeight += midtermExamWeight / midtermExamWithSpaceCounter
            elif key in markNames[4]:
                individualMidtermWeight += midtermExamWeight / midtermExamCounter
            elif key in markNames[5]:
                individualFinalWeight += finalExamWeight / finalExamCounter
            elif key in markNames[6]:
                individualBonusWeight += bonusWeight / bonusCounter
            elif key in markNames[7]:
                individualOtherWeight += otherWeight / otherCounter

        for i in range(len(gradeCategories)):  # Concatenates numbers to elements with same name (may not work as expected)
            if gradeCategories[i] in markNames[0]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfAssignments))
                numOfAssignments -= 1
            elif gradeCategories[i] in markNames[1]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfLabs))
                numOfLabs -= 1
            elif gradeCategories[i] in markNames[2]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfQuizzes))
                numOfQuizzes -= 1
            elif gradeCategories[i] in markNames[3]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfMidtermExamWithSpace))
                numOfMidtermExamWithSpace -= 1
            elif gradeCategories[i] in markNames[4]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfMidtermExams))
                numOfMidtermExams -= 1
            elif gradeCategories[i] in markNames[5]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfFinalExams))
                numOfFinalExams -= 1
            elif gradeCategories[i] in markNames[6]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfBonuses))
                numOfBonuses -= 1
            elif gradeCategories[i] in markNames[7]:
                gradeCategories[i] = gradeCategories[i] + ' ' + str(int(numOfOther))
                numOfOther -= 1

        gradeNameCategory = dict(zip(gradeCategories, gradePercentageAsString))
        print('\nMarks For Each Category: \n')
        for key, value in gradeNameCategory.items(): #Bug: Outputs wrong grade category
            print(key + ': ' + value)

        # Var declaration for total grade of each element
        totalAssignmentMark = 0
        totalLabMark = 0
        totalQuizMark = 0
        totalMidtermExamWithSpaceMark = 0
        totalMidtermExamMark = 0
        totalFinalExamMark = 0
        totalBonusMark = 0
        totalOtherMark = 0

        for i in range(len(finalGradeCalculation)): # Basic Grade Calculation 
                if finalGradeCalculation[i] in markNames[0]:
                    totalAssignmentMark += (individualAssignmentWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[1]:
                    totalLabMark += (individualLabWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[2]:
                    totalQuizMark += (individualQuizWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[3]:
                    totalMidtermExamWithSpaceMark += (individualMidtermWithSpaceWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[4]:
                    totalMidtermExamMark += (individualMidtermWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[5]:
                    totalFinalExamMark += (individualFinalWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[6]:
                    totalBonusMark += (individualBonusWeight * float(gradePercentageAsFloat[i])) / 100
                elif finalGradeCalculation[i] in markNames[7]:
                    totalOtherMark += (individualOtherWeight * float(gradePercentageAsFloat[i])) / 100

        finalMarkOfGrade = '{:.2f}'.format(((totalAssignmentMark + totalLabMark + totalQuizMark + totalMidtermExamWithSpaceMark + totalMidtermExamMark + totalFinalExamMark + totalBonusMark + totalOtherMark) / sumOfMarks) * 100)
        print('\nYour total grade is ' + str(finalMarkOfGrade) + '%')

    def courseLister(user, pwd):
        #Setting Selenium webdriver options
        loadingMessage = 'Loading Please Wait...'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        driver.minimize_window()
        print('')
        for char in loadingMessage:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        print('\n')
        #Course Navigation
        filterChoice = 'filterChoice__'
        driver.get("https://blackboard.uwindsor.ca/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")
        time.sleep(2)
        driver.find_element_by_id('agree_button').click()
        driver.find_element_by_link_text("Alternate Sign-In Method").click()
        username = driver.find_element_by_id("username")
        username.clear()
        username.send_keys(user)
        password = driver.find_element_by_id("password")
        password.clear()
        password.send_keys(pwd)
        driver.find_element_by_name('_eventId_proceed').click()
        driver.get('https://blackboard.uwindsor.ca/webapps/streamViewer/streamViewer?cmd=view&streamName=mygrades&&override_stream=mygrades&globalNavigation=false')
        time.sleep(3)
        displayCourseNames = driver.page_source
        soup = BeautifulSoup(displayCourseNames, 'html.parser')
        a = soup.find_all('ul')
        idOfCourses = str(a)
        displayCourseList(soup)
        for i, _ in enumerate(idOfCourses):  # Gets all course ID codes
            j = 1
            if idOfCourses[i:i + len(filterChoice)] == filterChoice:
                while idOfCourses[i + len(filterChoice) + j].isdigit():
                    j += 1
                courseIDs.append(idOfCourses[i + len(filterChoice): i + len(filterChoice) + j])
        for course in courseNames:  # Combining course name/ID lists into dict
            for courseID in courseIDs:
                courseNav[course] = courseID
                courseIDs.remove(courseID)
                break
        gradesOfCourse(driver)
        nextUserInput(driver)

    def blackboardUserAuthentication():

        URL = 'https://blackboard.uwindsor.ca'

        username = input('Username: ')
        password = stdiomask.getpass('Password: ')
        userData = {
            'j_username': username,
            'j_password': password,
            '_eventId_proceed': ''
        }

        blackboardLoginPage = s.get(URL)
        loginPage = BeautifulSoup(blackboardLoginPage.text, 'html.parser')
        a = loginPage.find_all('a')
        URL += (a[13]['href'])  # Gets the href element that leads to the student login page
        loginSite = s.get(URL)
        parsed = urlparse.urlparse(loginSite.url)
        execution = (parse_qs(parsed.query))['execution'] # Parses execution code at end of url to allow for successful link redirect 
        executionCode = ''.join(execution)
        response = s.post('https://login.net.uwindsor.ca/idp/profile/cas/login?execution=' + executionCode,
                          data=userData)
        studentHomepage = BeautifulSoup(response.text, 'html.parser')
        blackboardName = studentHomepage.find('button', {'class': 'nav-link u_floatThis-right'})
        try:
            successCode = blackboardName.find(username)
        except AttributeError:
            print('\nInvalid Username/Password! Please Try Again\n')
            blackboardUserAuthentication()
        if successCode != -1:
            blackboardName = str(studentHomepage.find('title'))
            endOfName = blackboardName.find(' ', 16, len(blackboardName)) 
            name = blackboardName[16:endOfName] 
            print(f'\nWelcome {name}!')
            option = input('\nWhat would you like to do?\n\n1. Check Your Grades\n2. Exit\n\n')
            while not option.isdigit() or (int(option) != 1 and int(option) != 2):
                option = (input('\nInvalid Input!\nWhat would you like to do?\n\n1. Check Your Grades\n2. Exit\n\n'))
            if int(option) == 1:
                courseLister(username, password)
            else:
                exit(0)

    print('Application Developed by Daniel Vaxman\n3rd Year Computer Science Student - University of Windsor\nFebruary 3rd - May 18th 2021\n')
    blackboardUserAuthentication()
