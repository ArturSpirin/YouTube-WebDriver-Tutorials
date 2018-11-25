import sys

screen = Screen(1)

input_field = "1543113516688.png"
accept_button = Pattern("accept_button.png").similar(0.65)
decline_button = Pattern("decline_button.png").similar(0.88)

should_accept = sys.argv[1] == "1"
screen.type(input_field, sys.argv[2])
screen.click(accept_button if should_accept else decline_button)
