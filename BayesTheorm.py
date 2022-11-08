class TextProcessor:

    def __init__(self, text):
        self.text = text
        self.stopWordsList = []
        populated_yes_list = []
        self.noDocs = float(14.0)


    def setStopWords(self, received):
        ''' set stop words as recieved in the parameters '''
        # CODE HERE #
        self.stopWordsList = received

    def getStopWords(self):
        ''' return stop words '''
        # CODE HERE #
        return self.stopWordsList

    def getUniqWords(self):
        ''' return unique words in a document corpus '''
        # CODE HERE #
        emptyList = []
        populatedList = self.text.split(" ")
        for word in populatedList:
            if word not in emptyList:
                emptyList.append(word)
        return emptyList

    def getFilteredText(self):
        ''' remove filter words from the text
            return filtered text
        '''
        # CODE HERE #
        wordList = self.text.split(" ")
        filteredText = []
        stopWordsList = self.getStopWords()
        for word in wordList:
            if word not in stopWordsList:
                filteredText.append(word)
        return filteredText


class TextAnalyzer(TextProcessor):
    def __init__(self, text):
        ''' Construct the class '''
        # CODE HERE #
        super().__init__(text)

    def getWordFrequency(self):
        ''' Call the getFilteredText() method
            Create a dictionary of words
            key = word and value= frequency
            return the dictionary
        '''
        # CODE HERE #
        wordFrequency = dict()
        filtered_text = TextProcessor.getFilteredText(self)
        for word in filtered_text:
            if word in wordFrequency.keys():
                wordFrequency[word] += 1
            else:
                wordFrequency[word] = 1

        return wordFrequency

class TextClassifier(TextProcessor):
    def __init__(self, text):
        ''' Construct the class '''
        ## CODE HERE ##
        super().__init__(text)

    def loadCorpus(self):
        ''' read documents into a dictionary such that
            keys of the dictionary are class ids
            and values are list of documents

            {1 : ['text of doc1', 'text of doc2'],
             2 : ['text of doc3', 'text of doc4']
            }

        '''
        # CODE HERE #
        my_dict = dict()
        populated_nos = []
        populated_yes = []
        for i in range(1, 15):

            with open(f'row{i}.txt', 'r') as row1:
                row_txt = row1.read()

                txt_list = row_txt.split(" ")

                for item in txt_list:
                    if item.lower() == 'no':
                        txt_list.pop(-1)
                        txt_list.pop(0)
                        populated_nos.append(txt_list)
                        my_dict['Play = No'] = populated_nos
                    if item.lower() == 'yes':
                        txt_list.pop(-1)
                        txt_list.pop(0)
                        populated_yes.append(txt_list)
                        my_dict['Play = Yes'] = populated_yes

        return my_dict



    def getDocumentProbabilityGivenClass(self, listDoc, givenClass):

        '''Calculate conditional probability of a document given its class '''
        # CODE HERE #
        yesList = list()
        noList = list()
        listDocWord_frequency = dict()
        access_my_dict = self.loadCorpus()
        play_count = float(len(access_my_dict['Play = Yes']))
        noPlay_count = float(len(access_my_dict['Play = No']))
        prob_doc_given_doc = 1

        if givenClass.lower() == 'yes':
            for word in listDoc:
                for value in access_my_dict['Play = Yes']:
                    if word in value:
                        if word in listDocWord_frequency.keys():
                            listDocWord_frequency[word] += 1

                        else:
                            listDocWord_frequency[word]= 1
            print(listDocWord_frequency)

            for value in listDocWord_frequency.values():
                yesList.append(round(float(value/play_count),2))
            print(yesList)
            for value in yesList:
                prob_doc_given_doc = prob_doc_given_doc * value
            return  round(prob_doc_given_doc,3)


        elif givenClass.lower() == 'no':
            for word in listDoc:
                for value in access_my_dict['Play = No']:
                    if word in value:
                        if word in listDocWord_frequency.keys():
                            listDocWord_frequency[word] += 1
                        else:
                            listDocWord_frequency[word]= 1
            print(listDocWord_frequency)

            for value in listDocWord_frequency.values():
                noList.append(round(float(value/noPlay_count),2))
            print(noList)
            for value in noList:
                prob_doc_given_doc = prob_doc_given_doc * value
            return  round(prob_doc_given_doc,3)

        else:
            return "Please enter either a \"yes\" or \"no\" for class parameter."



    def getPriorProbability(self, prior_prob_class):
        ''' return prior probability of a text class
        '''
        ## CODE HERE #

        access_my_dict = self.loadCorpus()

        if prior_prob_class.lower() == "yes":
            return float(len(access_my_dict['Play = Yes'])/ self.noDocs)

        if prior_prob_class.lower() == "no":
            return float(len(access_my_dict['Play = No'])/self.noDocs)


    def getClassProbabilityGivenDocument(self, listDoc, givenClass):
        ''' return class probability given a document
        '''
        # CODE HERE #
        access_getdocprob_givenclass = self.getDocumentProbabilityGivenClass(listDoc, givenClass)
        return round(float(access_getdocprob_givenclass * self.getPriorProbability(givenClass)),4)


    def getClassGivenDocument(self, listDoc):
        ''' return class probability given a document
        '''
        # CODE HERE #
        access_classProbGivenDocYes = self.getClassProbabilityGivenDocument(listDoc, 'yes')
        access_classProbGivenDocNo = self.getClassProbabilityGivenDocument(listDoc, 'no')
        print("prob yes", access_classProbGivenDocYes)
        print("prob no", access_classProbGivenDocNo)
        if access_classProbGivenDocYes > access_classProbGivenDocNo:
            return "Play"
        else:
            return "No Play"




"""
Verify the correctness of your code using the following steps:

    Instantiate the TextAnalyzer class by creating an object called ta as follows:

ta = TextAnalyzer("a quick brown fox " + "a quick brown fox jumps " + "a quick brown fox jumps over " + "a quick brown 
fox jumps
 over the " + "a quick brown fox jumps over the lazy " + "a quick brown fox jumps over the lazy dog")

    Assign a list of stop words using the setStopWords() method: ta.setStopWords(['a', 'the'])

    Count the occurrences of each word using the getWordFrequency() method: ta.getWordFrequency()

    The output should be as follows {'quick': 6, 'brown': 6, 'fox': 6, 'jumps': 5, 'over': 4, 'lazy': 2, 'dog': 1}}

    Use the following table to verify your TextClassifier class functionality. Take each row of the table as one 
    document. The class of the document is value of Play column. Prepare data files by converting each row of the table 
    as a seperate file. Then read those files in loadCorpus() method.


"""


ta = TextAnalyzer("a quick brown fox " + "a quick brown fox jumps " + "a quick brown fox jumps over " +
                  "a quick brown fox jumps over the " + "a quick brown fox jumps over the lazy " +
                  "a quick brown fox jumps over the lazy dog")

ta.setStopWords(['a', 'the'])

print(ta.getWordFrequency())
print(ta.getUniqWords())
ta = TextClassifier('a quick brown fox jumps over the lazy')

print (120 * '*')
print(ta.loadCorpus())
print(ta.getPriorProbability('yes'))
print(ta.getPriorProbability('No'))

# should print noPlay
print(ta.getDocumentProbabilityGivenClass(['Rain', 'Hot', 'High', 'Weak'], 'no'))
print(ta.getDocumentProbabilityGivenClass(['Rain', 'Hot', 'High', 'Weak'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Rain', 'Hot', 'High', 'Weak'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Rain', 'Hot', 'High', 'Weak'], 'no'))
print(ta.getClassGivenDocument(['Rain', 'Hot', 'High', 'Weak']))

print(120 * '*')

# should print noPlay
print(ta.getDocumentProbabilityGivenClass(['Sunny', 'Hot', 'High', 'Weak'], 'no'))
print(ta.getDocumentProbabilityGivenClass(['Sunny', 'Hot', 'High', 'Weak'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Sunny', 'Hot', 'High', 'Weak'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Sunny', 'Hot', 'High', 'Weak'], 'no'))
print(ta.getClassGivenDocument(['Sunny', 'Hot', 'High', 'Weak']))

print(120 * '*')

# should print Play
print(ta.getDocumentProbabilityGivenClass(['Sunny', 'Mild', 'Normal', 'Strong'], 'no'))
print(ta.getDocumentProbabilityGivenClass(['Sunny', 'Mild', 'Normal', 'Strong'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Sunny', 'Mild', 'Normal', 'Strong'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Sunny', 'Mild', 'Normal', 'Strong'], 'no'))
print(ta.getClassGivenDocument(['Sunny', 'Mild', 'Normal', 'Strong']))

print(120 * '*')

# should print Play
print(ta.getDocumentProbabilityGivenClass(['Cloudy', 'Cool', 'Normal', 'Strong'], 'no'))
print(ta.getDocumentProbabilityGivenClass(['Cloudy', 'Cool', 'Normal', 'Strong'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Cloudy', 'Cool', 'Normal', 'Strong'], 'yes'))
print(ta.getClassProbabilityGivenDocument(['Cloudy', 'Cool', 'Normal', 'Strong'], 'no'))
print(ta.getClassGivenDocument(['Cloudy', 'Cool', 'Normal', 'Strong']))
