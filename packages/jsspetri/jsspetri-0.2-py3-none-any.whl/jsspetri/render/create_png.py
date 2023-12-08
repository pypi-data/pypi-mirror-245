import os
from graphviz import Digraph

def create_png(gui,action):
    
  action=gui.jssp.action_map[action]
  dot = Digraph(comment=f"Petri Net for jssp {gui.jssp.instanceID}", format='jpg' )
  dot.graph_attr['dpi'] = '100' 
  
  dot.attr(label=f'reward : {0}')
  
  palette = [
    
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse"
    ]
  
  # Add places to the graph
  for place in gui.jssp.places.values():    
      if len (place.token_container)>0:
          
          if place.uid in gui.jssp.filter_nodes("machine") :
              elapsed=place.token_container[0].logging[list(place.token_container[0].logging.keys())[-1]][2]
              label = str(place.token_container[0].process_time-elapsed)
          else :
               label = str(len(place.token_container))
          dot.node(place.uid, shape="circle",  color=palette[place.token_container[0].color[0]] , label=label, xlabel=place.label, fontsize="10", style="filled")  
    
      else :
          dot.node(place.uid, shape="circle",  color="aliceblue", label="0", xlabel=place.label, fontsize="10", style="filled")
 
  # Add transitions to the graph
  for transition in gui.jssp.transitions.values():
      
      if transition.color==action[0] and transition.uid in gui.jssp.filter_nodes("allocate"):
          dot.node(transition.uid, shape="box", height="0.2", color="red", label="", xlabel=transition.label, fontsize="10", style="filled")  
      else :
          dot.node(transition.uid, shape="box", height="0.2", color="lightgray", label="", xlabel=transition.label, fontsize="10", style="filled")  
          
  # Add arcs (edges) to represent connections between places and transitions
  for place in gui.jssp.places.values():
      for transition in place.children:
          dot.edge(place.uid, transition.uid)
  
  for transition in gui.jssp.transitions.values():
      for place in transition.children:
          dot.edge(transition.uid, place.uid)

  filename=os.path.join(gui.current_render_path,f"{gui.jssp.internal_clock}")     
  dot.render(filename, cleanup=True)
  return dot    
    