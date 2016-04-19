import sys
from calculator import History, Expression, Calc


class Menu:
    """Display a menu and respond to choices when run."""

    def __init__(self):

        self.history = History()
        self.expression = Expression()
        self.calc = Calc()
        self.choices = {
            "1": self.full_solve,
            "2": self.show_expr_history,
            "3": self.conversion,
            "4": self.quit
        }

    def display_menu(self):
        print("""
            RPN Calculator Menu
            1. Add & solve a new expression
            2. Display all previous expressions
            3. Convert an expression (prefix->postfix)
            4. Quit
            """)

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(str(choice))
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_expr_history(self, expr_history=None):
        """Shows the history of all executed expressions in the current session."""
        expr_history = self.history.expr_history
        if expr_history is not None:
            print("Previous expressions:")
            for expression in expr_history:
                print(expression.expr)

        elif expr_history is None:

            print("There are no previous expressions.")

    def add_expr(self):
        """Adds and expression from input"""
        expr = input("Enter an expression: ")
        self.history.new_expr(expr)
        print("Your expression has been added.")
        return expr

    def full_solve(self):
        """Converts an expression from standard to postfix notation and solves it."""
        expr = self.add_expr()
        expr = self.calc.calculate(self.calc.infix_to_postfix(expr))
        print("Result: " + str(expr))

    def conversion(self):
        """Converts an expression from standard to postfix notation"""
        expr = self.add_expr()
        expr = self.calc.infix_to_postfix(expr)
        print("Result: " + " ".join(expr))

    """def solve_postfix(self):  #Solves a postfix expression
        expr = self.add_expr()
        expr = self.calc.calculate(expr)
        print("Result: " + str(expr))
    """

    def quit(self):
        """Quits the current session"""
        print("Thank you for using our calculator.")
        sys.exit(0)

if __name__ == "__main__":
    Menu().run()
