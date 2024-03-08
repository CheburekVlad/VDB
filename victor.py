%matplotlib inline
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D

int  = []       #
count = {}      #   dico qui contien le nombre d'occurences
G = nx.Graph()  #   objet a partir duquel tu crées ton graph avec les valeurs de  la liste int

type = {}       #   un dico qui permet de compter le nombre d'interactions physiques par prot (pas implementé, mais il est bon)
colo = []       #   liste des couleurs avec red pour les interactions physiques et gray pour les autres
with open('/home/cheburek/Desktop/jupyter_serie/data/proteins.mitab', 'r') as file:
    for line in file:
       
        parts = line.strip().split('\t')
        ty = parts[11]
        
        id1 = parts[0].split(':')[1]
        id2 = parts[1].split(':')[1]
        int.append((id1,id2))           
        if id1 not in type.keys():
            type[id1] = 0
        if id2 not in type.keys():
            type[id2] = 0
        if '(physical association)' in ty.split("\""):
            type[id1] = type.get(id2, 0) +1
            type[id2] = type.get(id2, 0) +1
            colo.append("red")
        else:
            colo.append("gray")
# jusqu'a la tu a 2 vecteurs, int et colo, avec les proteines en interaction et la couleur en fonction d'interaction associée

for i in int:
    prot1, prot2 = i
    count[prot1] = count.get(prot1, 0) + 1
    count[prot2] = count.get(prot2, 0) + 1
    G.add_edge(prot1,prot2)

#  ici j'ai créé ton G et conté le nombre d'interactions dont chaque prot fait partie


fig, ax = plt.subplots(figsize=(20,20))   #afffichage
size = []

for s in count:
    size.append(count[s] **1.8)                   # ca c'est juste pour avoir une taille des noeuds uin poil plus grand
node_counts = [count[node] for node in G.nodes]




# IMPORTANT j'ai pris celle la mais tu peut prendre celle par default ou 
pos = nx.kamada_kawai_layout(G) 

#pos = nx.fruchterman_reingold_layout(G)    ou   pos = nx.spring_layout(G) meme chose
#pos = nx.shell_layout(G) ou pos = nx.circular_layout(G)    - meme chose a peu pres, les deux sont bof utilisables
#pos = nx.random_layout(G)                si tu joues un peut tu peut avoir un truc vraiment pas degeu




nx.draw(G, pos, with_labels=True, node_color = 'green' , node_size=size, cmap = cmap,
       width=1.5,edge_color=colo, font_color='black', font_size = 10)   # ca c'est ta figure que tu rajoute sur le background
                                                                        # c'est le "CSS" de tout sauf la colormap, et la legende


fig.set_facecolor('#f0f0f0')  # fond

cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax)      # pour la colormap, bon courage a mettre un place, mais si jamas ca se rajoute comme ca
cbar.set_label('Number of experiences(normalized)', rotation=270, labelpad=15)

legend_labels = {
    'Interaction': 'gray',
    'Physical\ninteraction': 'red',
    'Protein': {'marker': 'o', 'color': 'green', 's': 500},
    'PXXXX - uniprotid': {'marker': '', 'color': 'black', 's': 0}  # Empty marker for text label
}   # les labels de ta legende, A MODIFIER ABSOLUMENT, au moins l'emplacement

# Create legend handles
legend_handles = [
    Line2D([0], [0], color=style, linewidth=2, label=label) if isinstance(style, str)
    else plt.Line2D([0], [0], marker=style['marker'], color=style['color'], markersize=8, label=label, linestyle='None')
    for label, style in legend_labels.items()    # aucune idée comment ca marche, merci GPT
]

plt.legend(handles=legend_handles, loc='upper right', fontsize='large')
plt.savefig('vdb',format='svg')   # sauvegarder l'image, je te conseille de garder le csv


