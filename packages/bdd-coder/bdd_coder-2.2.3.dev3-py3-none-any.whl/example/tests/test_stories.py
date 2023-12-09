from . import base


def teardown_module():
    """
    Called by Pytest at teardown of the test module, employed here to
    log final scenario results
    """
    base.BddTester.gherkin.log()


class NewGame(base.BddTester):
    """
    As a codebreaker
    I want to start a new Mastermind game of B boards of G guesses
    In order to play
    """

    @base.BddTester.gherkin()
    def test_odd_boards(self):
        """
        When I request a new `game` with $(9) boards
        Then I get a 400 response saying it must be even
        """

    @base.BddTester.gherkin()
    def even_boards(self):
        """
        When I request a new `game` with $(8) boards
        Then a game is created with boards of $guess_count guesses
        """

    def i_request_a_new_game_with_boards(self):
        return 'game',

    def i_get_a_400_response_saying_it_must_be_even(self):
        pass

    def a_game_is_created_with_boards_of_guess_count_guesses(self, guess_count):
        pass


class TestClearBoard(NewGame):
    """
    As a codebreaker
    I want a clear board with a new code
    In order to start making guesses on it
    """

    @base.BddTester.gherkin()
    def test_start_board(self):
        """
        Given even boards
        When I request a clear `board` in my new game
        Then the first board is added to the game
        """

    def i_request_a_clear_board_in_my_new_game(self):
        return 'board',

    def the_first_board_is_added_to_the_game(self):
        pass
