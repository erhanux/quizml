''' Test cases for MultichoiceQuiz class '''

import unittest
import tempfile
from textx.exceptions import TextXSyntaxError

import testdata
from quiz import MultichoiceQuiz


class MultichoiceQuizTest(unittest.TestCase):
    '''
    Test cases for Multi-choice quiz metamodel.
    A quiz file is created on the fly by using the pre-defined strings in
    testdata module.
    '''

    def setUp(self):
        self.mc_quiz = MultichoiceQuiz()
        # temporary quiz data to be populated by each test case
        self.qml_file = tempfile.NamedTemporaryFile(delete=True)

    def tearDown(self):
        self.qml_file.close()

    def test_metamodel(self):
        ''' Assures that the metamodel is valid '''
        self.assertIsNotNone(self.mc_quiz.get_metamodel())

    def test_multichoice_noquestion(self):
        ''' No question in input quiz should raise TextXSyntaxError '''
        self.qml_file.write(testdata.model_invalid_no_question.encode())
        self.qml_file.flush()
        self.assertRaises(TextXSyntaxError, self.mc_quiz.load_model, self.qml_file.name)

    def test_multichoice_load_model(self):
        ''' Valid input, make sure that all fields initialized correctly '''
        self.qml_file.write(testdata.model_mc_q1.encode())
        self.qml_file.flush()
        self.assertIsNone(self.mc_quiz.get_model())
        model = self.mc_quiz.load_model(self.qml_file.name)
        self.assertIsNotNone(model)

        # check if the model loaded correctly
        self.assertEqual(model.title, 'this is a sample quiz')
        self.assertEqual(model.description, 'multi-choice quiz to to demonstrate qml')
        self.assertEqual(len(model.tags), 3)
        self.assertEqual(model.tags[1], 'tag with spaces')

        self.assertEqual(len(model.questions), 1)
        self.assertEqual(model.questions[0].question, 'This is the first question')
        self.assertEqual(len(model.questions[0].options), 2)
        self.assertEqual(model.questions[0].options[0].otype, '+')
        self.assertEqual(model.questions[0].options[0].otext, 'True')
        self.assertEqual(model.questions[0].options[1].otype, '-')
        self.assertEqual(model.questions[0].options[1].otext, 'False')


if __name__ == '__main__':
    unittest.main()
