from networkx import *

email = nx.read_edgelist("email_network.txt",create_using=DiGraph())
num_nodes = float(len(email.nodes()))

# Get SCCs
sccs = strongly_connected_component_subgraphs(email)
big_scc = sccs[0] # first one is largest, based on networkx docs
big_component = set(big_scc.nodes())

# Helper function to find predecessors or successors of a set of nodes
def get_new_nodes(nodeset,func,graph):
    new_nodes = set()
    for n in nodeset:
        new_nodes.update(func(graph,n))
    return new_nodes.difference(nodeset) 

in_component = get_new_nodes(big_component,DiGraph.predecessors,email)
while True:
    new_nodes = get_new_nodes(in_component,DiGraph.predecessors,email)
    if len(new_nodes) > 0:
        in_component.update(new_nodes)
    else:
        break

out_component = get_new_nodes(big_component,DiGraph.successors,email)
while True:
    new_nodes = get_new_nodes(out_component,DiGraph.successors,email)
    if len(new_nodes) > 0:
        out_component.update(new_nodes)
    else:
        break
        
# Calculate sizes and percentages
components = len(big_component)+len(in_component)+len(out_component)
print "Big SCC component:",100*len(big_component)/num_nodes
print "In component:",100*len(in_component)/num_nodes
print "Out component:",100*len(out_component)/num_nodes
print "Disconnected components:",100*components/num_nodes
