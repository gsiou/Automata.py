#!/usr/bin/python

# author: gsiou
#
#
# simple program to check if string is accepted by given automata
#         
# Usage: ./Automata.py -h (for help) or
# ./Automata.py -i inputfile.txt -c checkfile.txt
# Both -i and -c arguments are optional.
# Input file is a file with Automata.py prompt commands (one command per line)
# Check file is a file with strings to be checked by current automaton (one string per line)
# for help while in program prompt run program and type 'help'
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function
import sys
import getopt

class Connection:
        def __init__(self, to, conditions):
                self.to = to
                self.conditions = [i for i in conditions]

class Node:
        def __init__(self, node_id):
                self.connections = []
                self.node_id = node_id
                self.ending = False

        def add_connection(self, to, conditions):
                self.connections.append(Connection(to, conditions))

        def set_ending(self):
                self.ending = True

class Automata:
        def __init__(self):
                self.nodes = {}
                self.start_node = None

        def create_node(self, node_id):
                self.nodes[node_id] = Node(node_id)

        def create_connection(self, node_from, node_to, conditions):
                if node_from not in self.nodes:
                        print("Node {0} does not exist.".format(node_from))
                        return False
                if node_to not in self.nodes:
                        print("Node {0} does not exist.".format(node_to))
                        return False
                self.nodes[node_from].add_connection(
                        self.nodes[node_to], conditions)
                return True

        def set_start(self, start_id):
                if start_id not in self.nodes:
                        print("Node {0} does not exist.".format(start_id))
                        return False
                self.start_node = self.nodes[start_id]

        def check_string(self, string):
                if self.start_node is None:
                        print("There is no starting node.")
                        return False
                else:
                        current_char = 0
                        current_node = self.start_node # entry point
                        while current_char < len(string):
                                for i in current_node.connections: # check all outgoing connections
                                        found = False
                                        for j in i.conditions: #check if conditions are met
                                                if j == string[current_char]:
                                                        # We go to the next node
                                                        current_node = i.to
                                                        found = True
                                                        break # We found a path
                                        if(found):
                                                break # we found a path to move
                                current_char += 1 #check next character
                        if current_node.ending:
                                print("String {0} matches automata.".format(string))
                                return True
                        else:
                                print("String {0} does not match automata.".format(string))
                                return False

        def make_ending(self, node_id):
                if node_id not in self.nodes:
                        print("Node {0} does not exist.".format(node_id))
                        return False
                self.nodes[node_id].set_ending()

        def print_automata(self):
                for i in self.nodes:
                        print(self.nodes[i].node_id, end=" ")
                        for j in self.nodes[i].connections:
                                print("({0}): {1}".format(j.to.node_id, j.conditions), end = " ")
                        print("")

        def get_dump(self):
                if len(self.nodes) == 0:
                        return "\n"
                creation_txt = "add"
                connection_txt = ""
                start_txt = ""
                end_txt = ""
                for i in self.nodes:
                        creation_txt += " " + self.nodes[i].node_id
                        if self.nodes[i].ending:
                                end_txt += "end " + self.nodes[i].node_id + "\n"
                        for j in self.nodes[i].connections:
                                connection_txt += "conn {0} {1}".format(
                                        self.nodes[i].node_id,
                                        j.to.node_id
                                )
                                for c in j.conditions:
                                        connection_txt += " {0}".format(c)
                                connection_txt += "\n"
                creation_txt += "\n"
                if self.start_node:
                        start_txt = "start {0}\n".format(self.start_node.node_id)
                return creation_txt + connection_txt + start_txt + end_txt

def parse_cmd(command, auto):
        split_cmd = command.split(" ")
        if split_cmd[0] == "add":
                for i in command.split(" ")[1:]:
                        auto.create_node(i)
        elif split_cmd[0] == "conn":
                auto.create_connection(split_cmd[1],
                                       split_cmd[2], split_cmd[3:])
        elif split_cmd[0] == "start":
                auto.set_start(split_cmd[1])
        elif split_cmd[0] == "end":
                auto.make_ending(split_cmd[1])
        elif split_cmd[0] == "check":
                auto.check_string(split_cmd[1])
        elif split_cmd[0] == "checkfile":
                with open(split_cmd[1]) as f:
                        for i in f.readlines():
                                auto.check_string(i[:-1])
        elif split_cmd[0] == "reset":
                auto = Automata()
        elif split_cmd[0] == "file":
                with open(split_cmd[1]) as f:
                        for i in f.readlines():
                                parse_cmd(i[:-1], auto)
        elif split_cmd[0] == "dump":
                with open(split_cmd[1], "w") as f:
                        f.write(auto.get_dump())
                print(auto.get_dump(), end="")
                print("Dump printed to file")
        elif split_cmd[0] == "print":
                auto.print_automata()
        elif split_cmd[0] == "exit":
                sys.exit()
        elif split_cmd[0] == "help":
                print("Available commands: ")
                print("add node1 node2 ...")
                print("conn node_from node_to transitionchar1 transitionchar2 ...")
                print("start node (makes node starting node)")
                print("end node (makes node an ending node)")
                print("check string (checks if string is accepted)")
                print("reset (makes a new automaton)")
                print("file myfile.txt (loads a file with commands)")
                print("checkfile myfile.txt (loads a file with one string per line and checks them with current automaton)")
                print("dump myfile.txt (saves current state to file to be loaded with file command)")
                print("print (prints current state)")
                print("exit (exits program)")
                print("help (displays this information)")
        else:
                print("Invalid command.")

def usage():
        print("Usage: ./Automata.py -h (for help) or")
        print("./Automata.py -i inputfile.txt -c checkfile.txt")
        print("Both -i and -c arguments are optional.")
        print("Input file is a file with Automata.py prompt commands (one command per line)")
        print("Check file is a file with strings to be checked by current automaton (one string per line)")

def main(argv):
        inputfile = ""
        checkfile = ""

        #handle command line arguments
        try:
                opts, args = getopt.getopt(argv, "hi:c:", ["input=","check="])                
        except getopt.GetoptError:
                parse_cmd("help", None)
                sys.exit(2)
        for opt, arg in opts:
                if opt == "-h":
                        usage()
                        parse_cmd("help", None)
                        sys.exit()
                elif opt in ("-i", "--input"):
                        inputfile = arg
                elif opt in ("-c", "--check"):
                        checkfile = arg

        auto = Automata()

        if inputfile: #load commands from file
                parse_cmd("file " + inputfile, auto)
        if checkfile: #load check strings from file
                parse_cmd("checkfile " + checkfile, auto)

        while True:
                print("% ", end="")
                command = raw_input()
                parse_cmd(command, auto)

if __name__ == "__main__":
        main(sys.argv[1:])
