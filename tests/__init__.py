import sys
import os

if __package__:
    current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    current_path = os.path.abspath(os.path.dirname(__file__)) + "/"

current_path = current_path + '/tests'

if os.path.isdir(current_path):
    sys.path.insert(0, current_path)

