### Source: https://zulko.github.io/easyAI/examples/integrate.html
### Source Code: https://github.com/Zulko/easyAI/blob/master/easyAI/games/TicTacToe-Flask.py

from flask import Blueprint, render_template, request, make_response, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

ai_algo = Negamax(6)
games = Blueprint('games', __name__)

@games.route('/game', methods=['GET', 'POST'])
@login_required
def game():

    return render_template("game.html", user=current_user) 

@games.route('/game/tic-tac-toe', methods=['GET', 'POST'])
@login_required
def game_tic_tac_toe():
    ttt = TicTacToe([Human_Player(), AI_Player(ai_algo)])
    game_cookie = request.cookies.get('game_board')
    if game_cookie:
        ttt.board = [int(x) for x in game_cookie.split(",")]
    if "choice" in request.form:
        ttt.play_move(request.form["choice"])
        if not ttt.is_over():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)
    if "reset" in request.form:
        ttt.board = [0 for i in range(9)]
    if ttt.is_over():
        msg = ttt.winner()
    else:
        msg = "Play move"
    resp = make_response(render_template("game-tictactoe.html", ttt=ttt, msg=msg, user=current_user))
    c = ",".join(map(str, ttt.board))
    resp.set_cookie("game_board", c)
    return resp

TEXT = '''
<!doctype html>
<html>
  <head><title>Tic Tac Toe</title></head>
  <body>
    <h1>Tic Tac Toe</h1>
    <h2>{{msg}}</h2>
    <form action="" method="POST">
      <table>
        {% for j in range(2, -1, -1) %}
        <tr>
          {% for i in range(0, 3) %}
          <td>
            <button type="submit" name="choice" value="{{j*3+i+1}}"
             {{"disabled" if ttt.spot_string(i, j)!="_"}}>
              {{ttt.spot_string(i, j)}}
            </button>
          </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </table>
      <button type="submit" name="reset">Start Over</button>
    </form>
  </body>
</html>
'''

# ImportError: cannot import name 'TwoPlayersGame' from 'easyAI'
# Solution: https://stackoverflow.com/questions/73710889/how-can-i-resolve-import-errors

class TicTacToe(TwoPlayerGame):
    """ The board positions are numbered as follows:
            7 8 9
            4 5 6
            1 2 3
    """

    def __init__(self, players):
        self.players = players
        self.board = [0 for i in range(9)]
        #self.nplayer = 1  # player 1 starts.
        self.current_player = 1     # add this line to solve AttributeError: 'TicTacToe' object has no attribute 'current_player'

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    WIN_LINES = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # horiz.
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # vertical
        [1, 5, 9], [3, 5, 7]  # diagonal
    ]

    def lose(self, who=None):
        """ Has the opponent "three in line ?" """
        if who is None:
            who = self.opponent_index   # AttributeError: 'TicTacToe' object has no attribute 'nopponent'; Solution: Change to 'opponent_index'
        wins = [all(
            [(self.board[c - 1] == who) for c in line]
        ) for line in self.WIN_LINES]
        return any(wins)

    def is_over(self):
        return (self.possible_moves() == []) or self.lose() or \
            self.lose(who=self.current_player)

    def show(self):
        print ('\n' + '\n'.join([
            ' '.join(
                [['.', 'O', 'X'][self.board[3 * j + i]] for i in range(3)]
            )
            for j in range(3)
        ]))

    def spot_string(self, i, j):
        return ["_", "O", "X"][self.board[3 * j + i]]

    def scoring(self):
        opp_won = self.lose()
        i_won = self.lose(who=self.current_player)
        if opp_won and not i_won:
            return -100
        if i_won and not opp_won:
            return 100
        return 0

    def winner(self):
        if self.lose(who=2):
            return "AI Wins"
        return "Tie"
    

