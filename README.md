#Automata.py
####Simple program to construct automata (theory of computation) and check if strings are accepted by it

 Usage: `./Automata.py -h` (for help) or  
 `./Automata.py -i inputfile.txt -c checkfile.txt`  
 Both -i and -c arguments are optional.  
 Input file is a file with Automata.py prompt commands (one command per line)  
 Check file is a file with strings to be checked by current automaton (one strig per line)  
 for help while in program prompt run program and type 'help'  

After executing Automata.py a prompt appears.  
Prompt commands:  

**add** node1 node2 ...  
**conn** node_from node_to transitionchar1 transitionchar2 ...  
**start** node (makes node starting node)  
**end** node (makes node an ending node)  
**check** string (checks if string is accepted)  
**reset** (makes a new automaton)  
**file** myfile.txt (loads a file with commands)  
**checkfile** myfile.txt (loads a file with one string per line and checks them with current automaton)  
**dump** myfile.txt (saves current state to file to be loaded with file command)  
**print** (prints current state)  
**exit** (exits program)  
**help** (displays this information)  


Example of input file:
```
add q0 q1 q2 q3
conn q0 q0 0
conn q0 q1 1 4 7
conn q0 q2 2 5 8
conn q0 q3 3 6 9
conn q1 q2 1 4 7
conn q1 q1 0 3 6 9
conn q1 q3 2 5 8
conn q2 q2 0 3 6 9
conn q2 q1 2 5 8
conn q2 q3 1 4 7
conn q3 q3 0 3 6 9
conn q3 q1 1 4 7
conn q3 q2 2 5 8
start q0
end q3
```
