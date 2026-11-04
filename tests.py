import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)

    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert not question.choices[0].is_correct
    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_remove_all_choices():
    question = Question(title='q1')
    
    choice = question.add_choice('a', False)
    choice = question.add_choice('b', True)
    assert len(question.choices) == 2

    question.remove_all_choices()
    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    
    choice = question.add_choice('a', False)
    assert len(question.choices) == 1

    with pytest.raises(Exception):
        question.remove_choice('invalid_id')

def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)

    question.set_correct_choices([choice1.id, choice2.id])
    
    assert choice1.is_correct
    assert choice2.is_correct
    assert not choice3.is_correct

def test_set_correct_choices_with_invalid_id():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    with pytest.raises(Exception):
        question.set_correct_choices(['invalid_id'])

def test_correct_selected_choices_one_right_one_wrong():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)

    correct_choices = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert correct_choices == [choice1.id]

def test_correct_selected_choices_with_multiple_correct_choices():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)

    correct_choices = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert correct_choices == [choice1.id, choice2.id]

def test_correct_selected_choices_no_correct_choices_selected():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)

    correct_choices = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert correct_choices == []

def test_correct_selected_choices_with_too_many_selections():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', False)

    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id, choice3.id])

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    return question, [choice1, choice2, choice3]

def test_correct_selected_choices_with_fixture(question_with_choices):
    question, choices = question_with_choices
    choice1, choice2, choice3 = choices

    correct_choices = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert correct_choices == [choice1.id]

def test_correct_selected_choices_with_fixture_multiple_correct(question_with_choices):
    question, choices = question_with_choices
    choice1, choice2, choice3 = choices

    correct_choices = question.correct_selected_choices([choice1.id, choice3.id])
    
    assert correct_choices == [choice1.id, choice3.id]