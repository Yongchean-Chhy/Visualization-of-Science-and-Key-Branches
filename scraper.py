import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 
import networkx as nx

class TopicNode:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_sub_topic(self, sub_topic):
        self.children.append(sub_topic)
    
    def remove_sub_topic(self, name):
        for i, sub_top in enumerate(self.children):
            if sub_top.name == name:
                del self.children[i]
                break

def getUrl(topic):
    return f'https://en.wikipedia.org/wiki/{topic}'
    

def branchGeneratetor(root):
    headers = {'User_Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    for branch in root.children:
        # if branch.name == 'Applied_science':
        #     branch_url = 'https://en.wikipedia.org/wiki/Outline_of_applied_science'
        #     req = requests.get(branch_url, headers=headers)
        #     s = BeautifulSoup(req.text, 'lxml')
        #     sub_root4 = TopicNode(branch.name)
        #     sub_top4 = s.find('div', {'class' : 'mw-content-ltr mw-parser-output'}).find('ul').find_all('li')
        #     titles = [title.find('a')['title'] for title in sub_top4 if title.find('a')]
        #     for title in titles:
        #         sub_root4.add_sub_topic(TopicNode(title))
        #     root.add_sub_topic(sub_root4)
        #     root.remove_sub_topic(branch)
        #     continue  
        branch_url = getUrl(branch.name)
        req = requests.get(branch_url, headers=headers)
        s = BeautifulSoup(req.text, 'lxml')
        if branch.name == 'Natural_science':
            main_top1 = s.find('h1', {'id' : 'firstHeading'}).text
            sub_root1 = TopicNode(main_top1)
            sub_top1 = s.find('div', {'class' : 'mw-content-ltr mw-parser-output'}).find_all('div', {'class' : 'mw-heading mw-heading3'})
            for sub_top_ele in sub_top1[:5]:
                new_sub = sub_top_ele.text.split('[edit]')[0]
                sub_root1.add_sub_topic(TopicNode(new_sub))
            root.add_sub_topic(sub_root1)
            root.remove_sub_topic(branch) 
        elif branch.name == 'Social_science':
            main_top2 = s.find('h1', {'id' : 'firstHeading'}).text
            sub_root2 = TopicNode(main_top2)
            sub_top2 = s.find('div', {'class' : 'mw-content-ltr mw-parser-output'}).find_all('ul')[9]
            for sub_top_ele in sub_top2.text.splitlines():
                sub_root2.add_sub_topic(TopicNode(sub_top_ele))
            root.add_sub_topic(sub_root2)
            root.remove_sub_topic(branch)
        elif branch.name == 'Formal_science':
            main_top3 = s.find('h1', {'id' : 'firstHeading'}).text
            sub_root3 = TopicNode(main_top3)
            sub_top3 = s.find('div', {'class' : 'mw-content-ltr mw-parser-output'}).find('ol').find_all('li')
            for sub_top_ele in sub_top3:
                sub_root3.add_sub_topic(TopicNode(sub_top_ele.text))
            root.add_sub_topic(sub_root3)
            root.remove_sub_topic(branch)
    return root

def printTree(node, level=0):
    indent = '  ' *level
    print(f'{indent}- {node.name}')
    for child in node.children:
        printTree(child, level + 1)

def addEdge(graph, node):
    for branch in node.children:
        graph.add_edge(node.name, branch.name)
        addEdge(graph, branch)

def getNodeSize(node, cur_dept = 0, node_sizes = None):
    if node_sizes is None:
        node_sizes = {}
    node_sizes[node.name] = max(3000, cur_dept * 400, 500)
    for branch in node.children:
        getNodeSize(branch, cur_dept +1, node_sizes)
    return node_sizes

def graphVisualizer(root):
    g = nx.DiGraph()
    addEdge(g, root)
    
    pos = nx.spring_layout(g, seed=42)

    node_size = getNodeSize(root)
    plt.figure(figsize=(12, 8))

    nx.draw(g, pos, with_labels=True, 
            node_size = [node_size[node] for node in g.nodes()], 
            node_color = 'lightblue', font_size = 8)
    plt.title('Sceicne')
    plt.show()


def main():
    headers = {'User_Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    url = getUrl('Science')
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')


    topic = soup.find('h1', {'id' : 'firstHeading'}).text
    root = TopicNode(topic)

    subtitle = soup.find('div', {'class' : 'mw-content-ltr mw-parser-output'}).find_all('div', {'class' : 'mw-heading mw-heading3'})
    for i in range(8, 13):
        root.add_sub_topic(TopicNode(subtitle[i].text))
    
    root.children = [TopicNode(sub_top.name.replace(' ', '_')) for sub_top in root.children]
    new_root = branchGeneratetor(root)
    graphVisualizer(new_root)

if __name__ == '__main__' :
    main()

            




