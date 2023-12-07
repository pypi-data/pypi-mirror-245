def BFS():
    print(
"""
BFS:
def bfs_traverse(visited, graph, start):
    visited.append(start)
    queue.append(start)

    while queue:
        m = queue.pop(0)
        print(m)

        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)




if __name__ == "__main__":

    Graph = {
        "versova" : ["kamdhenu signal", "juhu link rd (1)", "dn nagar"],
        "kamdhenu signal" : ["jay maharashtra stationary", "juhu link rd (2)"],
        "juhu link rd (1)" : ["orion sayi consultant pvt ltd"],
        "dn nagar" : ["rossoneri pizza", "ajay stationary"],
        "jay maharashtra stationary" : ["n dutta marg"],
        "juhu link rd (2)" : ["juhu circle"],
        "orion sayi consultant pvt ltd" : ["juhu circle"],
        "rossoneri pizza" : ["indian oil nagar"],
        "ajay stationary" : ["wonder kitchen corner"],
        "n dutta marg" : ["wonder kitchen corner"],
        "indian oil nagar" : ["juhu circle"],
        "wonder kitchen corner" : ["juhu circle"],
        "juhu circle" : []
    }

    visited = []
    queue = []
    start = "versova"

    bfs_traverse(visited, Graph, start)




BFS2:
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            queue.extend(graph[node] - visited)

# Example graph represented as an adjacency list
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F', 'G'},
    'D': {'B'},
    'E': {'B'},
    'F': {'C'},
    'G': {'C'}
}

# Starting node for BFS
start_node = 'A'

print("BFS starting from node", start_node)
bfs(graph, start_node)
"""
        )


def BFS2():
    print(
"""
BFS2:
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            queue.extend(graph[node] - visited)

# Example graph represented as an adjacency list
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F', 'G'},
    'D': {'B'},
    'E': {'B'},
    'F': {'C'},
    'G': {'C'}
}

# Starting node for BFS
start_node = 'A'

print("BFS starting from node", start_node)
bfs(graph, start_node)
"""
        )

def IDFS():
    print(
"""
IDFS:
from collections import deque

def iterativeDFS(graph, start, destination):
    stack = deque()
    visited = []
    stack.appendleft(start)

    while stack:
        node = stack.popleft()

        if node in visited:
            continue

        visited.append(node)
        print(node)

        if node == destination:
            return

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.appendleft(neighbor)




if __name__ == "__main__":

    Graph = {
        "versova" : ["kamdhenu signal", "juhu link rd (1)", "dn nagar"],
        "kamdhenu signal" : ["jay maharashtra stationary", "juhu link rd (2)"],
        "juhu link rd (1)" : ["orion sayi consultant pvt ltd"],
        "dn nagar" : ["rossoneri pizza", "ajay stationary"],
        "jay maharashtra stationary" : ["n dutta marg"],
        "juhu link rd (2)" : ["juhu circle"],
        "orion sayi consultant pvt ltd" : ["juhu circle"],
        "rossoneri pizza" : ["indian oil nagar"],
        "ajay stationary" : ["wonder kitchen corner"],
        "n dutta marg" : ["wonder kitchen corner"],
        "indian oil nagar" : ["juhu circle"],
        "wonder kitchen corner" : ["juhu circle"],
        "juhu circle" : []
    }

    start = "versova"
    destination = "juhu circle"

    iterativeDFS(Graph, start, destination)



IDFS2:
def iterative_dfs(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            stack.extend(graph[node] - visited)

# Example graph represented as an adjacency list
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F', 'G'},
    'D': {'B'},
    'E': {'B'},
    'F': {'C'},
    'G': {'C'}
}

# Starting node for DFS
start_node = 'A'

print("Iterative DFS starting from node", start_node)
iterative_dfs(graph, start_node)
"""
        )

def IDFS2():
    print(
"""
IDFS2:
def iterative_dfs(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            stack.extend(graph[node] - visited)

# Example graph represented as an adjacency list
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F', 'G'},
    'D': {'B'},
    'E': {'B'},
    'F': {'C'},
    'G': {'C'}
}

# Starting node for DFS
start_node = 'A'

print("Iterative DFS starting from node", start_node)
iterative_dfs(graph, start_node)
"""
        )



def A_Star():
    print(
"""
A_Star:
import heapq

def a_star_search(graph, heuristic_graph, start, destination):
    open_list = [(0, start)]
    closed_list = set()
    g_scores = {node: float('inf') for node in graph}
    g_scores[start] = 0
    parents = {}
    total_distance = 0

    while open_list:
        _, current_node = heapq.heappop(open_list)
        closed_list.add(current_node)

        if current_node == destination:
            path = []
            while current_node in parents:
                path.append(current_node)
                total_distance += graph[parents[current_node]][current_node]
                current_node = parents[current_node]
            path.append(start)
            path.reverse()
            return path, total_distance

        for neighbor, distance in graph[current_node].items():
            if neighbor in closed_list:
                continue

            tentative_g_score = g_scores[current_node] + distance
            if tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic_graph[neighbor] # f(n) = g(n) + h(n)
                heapq.heappush(open_list, (f_score, neighbor))
                parents[neighbor] = current_node

    return None


if __name__ == "__main__":
    Graph = {
        "versova": {"kamdhenu signal": 476, "juhu link rd (1)": 106, "dn nagar": 864},
        "kamdhenu signal": {"jay maharashtra stationary": 436, "juhu link rd (2)": 628},
        "juhu link rd (1)": {"orion sayi consultant pvt ltd": 1740},
        "dn nagar": {"rossoneri pizza": 178, "ajay stationary": 728},
        "jay maharashtra stationary": {"n dutta marg": 463},
        "juhu link rd (2)": {"juhu circle": 1100},
        "orion sayi consultant pvt ltd": {"juhu circle": 148},
        "rossoneri pizza": {"indian oil nagar": 206},
        "ajay stationary": {"wonder kitchen corner": 222},
        "n dutta marg": {"wonder kitchen corner": 306},
        "indian oil nagar": {"juhu circle": 1180},
        "wonder kitchen corner": {"juhu circle": 620},
        "juhu circle": {}
    }

    heuristic_graph = {
        "versova": 1820,
        "kamdhenu signal": 1560,
        "juhu link rd (1)": 1760,
        "dn nagar": 1390,
        "jay maharashtra stationary": 1160,
        "juhu link rd (2)": 1080,
        "orion sayi consultant pvt ltd": 146,
        "rossoneri pizza": 1220,
        "ajay stationary": 708,
        "n dutta marg": 708,
        "indian oil nagar": 1180,
        "wonder kitchen corner": 622,
        "juhu circle": 0
    }

    start = "versova"
    destination = "juhu circle"

    path, total_distance = a_star_search(Graph, heuristic_graph, start, destination)
    if path:
        print(f"Shortest path from '{start}' to '{destination}': {path}")
        print(f"Total distance of the path: {total_distance}")
    else:
        print("No path found.")




A_Star2:
import heapq

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar(graph, start, goal):
    heap = [(0, start)]
    visited = set()

    while heap:
        cost, current = heapq.heappop(heap)

        if current == goal:
            print("Path found:", current)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + heuristic(neighbor, goal), neighbor))

# Example grid-based graph
grid_graph = {
    (0, 0): {(0, 1), (1, 0)},
    (0, 1): {(0, 0), (1, 1)},
    (1, 0): {(0, 0), (1, 1), (2, 0)},
    (1, 1): {(0, 1), (1, 0), (2, 1)},
    (2, 0): {(1, 0), (2, 1)},
    (2, 1): {(1, 1), (2, 0)}
}

# Starting and goal positions
start_position = (0, 0)
goal_position = (2, 1)

print("A* algorithm from", start_position, "to", goal_position)
astar(grid_graph, start_position, goal_position)
"""
        )

def A_Star2():
    print(
"""
A_Star2:
import heapq

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar(graph, start, goal):
    heap = [(0, start)]
    visited = set()

    while heap:
        cost, current = heapq.heappop(heap)

        if current == goal:
            print("Path found:", current)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + heuristic(neighbor, goal), neighbor))

# Example grid-based graph
grid_graph = {
    (0, 0): {(0, 1), (1, 0)},
    (0, 1): {(0, 0), (1, 1)},
    (1, 0): {(0, 0), (1, 1), (2, 0)},
    (1, 1): {(0, 1), (1, 0), (2, 1)},
    (2, 0): {(1, 0), (2, 1)},
    (2, 1): {(1, 1), (2, 0)}
}

# Starting and goal positions
start_position = (0, 0)
goal_position = (2, 1)

print("A* algorithm from", start_position, "to", goal_position)
astar(grid_graph, start_position, goal_position)

"""
        )


def Best_First_Search():
    print(
"""
Best_First_Search:
import heapq

def bestfirstsearch_iterative(graph, heuristic_graph, start, destination):
    visited = set()
    priority_queue = [(heuristic_graph[start], start, 0)]
    total_distance = 0

    while priority_queue:
        _, current_node, dist = heapq.heappop(priority_queue)
        visited.add(current_node)
        print(current_node)
        total_distance += dist

        if current_node == destination:
            return total_distance

        for neighbor, distance in graph[current_node].items():
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(priority_queue, (heuristic_graph[neighbor], neighbor, distance))

    return total_distance

def bestfirstsearch_recursive(graph, heuristic_graph, visited, priority_queue, destination, total_distance):
    if not priority_queue:
        return total_distance

    _, current_node, dist = heapq.heappop(priority_queue)
    visited.add(current_node)
    print(current_node)
    total_distance += dist

    if current_node == destination:
        return total_distance

    for neighbor, distance in graph[current_node].items():
        if neighbor not in visited:
            visited.add(neighbor)
            heapq.heappush(priority_queue, (heuristic_graph[neighbor], neighbor, distance))

    return bestfirstsearch_recursive(graph, heuristic_graph, visited, priority_queue, destination, total_distance)

def bestfirstsearch_traverse(graph, heuristic_graph, start, destination, traverse):
    visited = set()
    priority_queue = [(heuristic_graph[start], start, 0)]
    total_distance = 0

    if traverse == "iterative":
        total_distance = bestfirstsearch_iterative(graph, heuristic_graph, start, destination)
    elif traverse == "recursive":
        total_distance = bestfirstsearch_recursive(graph, heuristic_graph, visited, priority_queue, destination, total_distance)

    print(f"The final distance from '{start}' to '{destination}' is: {total_distance}")


if __name__ == "__main__":
    Graph = {
        "versova": {"kamdhenu signal": 476, "juhu link rd (1)": 106, "dn nagar": 864},
        "kamdhenu signal": {"jay maharashtra stationary": 436, "juhu link rd (2)": 628},
        "juhu link rd (1)": {"orion sayi consultant pvt ltd": 1740},
        "dn nagar": {"rossoneri pizza": 178, "ajay stationary": 728},
        "jay maharashtra stationary": {"n dutta marg": 463},
        "juhu link rd (2)": {"juhu circle": 1100},
        "orion sayi consultant pvt ltd": {"juhu circle": 148},
        "rossoneri pizza": {"indian oil nagar": 206},
        "ajay stationary": {"wonder kitchen corner": 222},
        "n dutta marg": {"wonder kitchen corner": 306},
        "indian oil nagar": {"juhu circle": 1180},
        "wonder kitchen corner": {"juhu circle": 620},
        "juhu circle": {}
    }

    heuristic_graph = {
        "versova": 1820,
        "kamdhenu signal": 1560,
        "juhu link rd (1)": 1760,
        "dn nagar": 1390,
        "jay maharashtra stationary": 1160,
        "juhu link rd (2)": 1080,
        "orion sayi consultant pvt ltd": 146,
        "rossoneri pizza": 1220,
        "ajay stationary": 708,
        "n dutta marg": 708,
        "indian oil nagar": 1180,
        "wonder kitchen corner": 622,
        "juhu circle": 0
    }

    start = "versova"
    destination = "juhu circle"

    bestfirstsearch_traverse(Graph, heuristic_graph, start, destination, traverse="recursive")


Best_First_Search2:
def best_first_search(graph, start, goal):
    queue = [(0, start)]
    visited = set()

    while queue:
        _, current = queue.pop(0)

        if current == goal:
            print("Path found:", current)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((heuristic(neighbor, goal), neighbor))
                queue.sort()

# Example graph
simple_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B'],
    'F': ['C'],
    'G': ['C']
}

# Starting and goal nodes
start_node = 'A'
goal_node = 'G'

print("Best-First Search algorithm from", start_node, "to", goal_node)
best_first_search(simple_graph, start_node, goal_node)

"""
        )


def Best_First_Search2():
    print(
"""
Best_First_Search2:
def best_first_search(graph, start, goal):
    queue = [(0, start)]
    visited = set()

    while queue:
        _, current = queue.pop(0)

        if current == goal:
            print("Path found:", current)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((heuristic(neighbor, goal), neighbor))
                queue.sort()

# Example graph
simple_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B'],
    'F': ['C'],
    'G': ['C']
}

# Starting and goal nodes
start_node = 'A'
goal_node = 'G'

print("Best-First Search algorithm from", start_node, "to", goal_node)
best_first_search(simple_graph, start_node, goal_node)
"""
        )



def Blue_ScreenGP():
    print(
"""

In visual studio 2019:
Step 1: Create new project, and select “Windows Forms Application”, select .NET Framework as 2.0 in
Visuals C#.
Step 2: Right Click on properties Click on open click on build Select Platform Target and Select x86.
Step 3: Click on View Code of Form 1.
Step 4: Go to Solution Explorer, right click on project name, and select Add Reference. Click on Browse
and select the given .dll files which are “Microsoft.DirectX”, “Microsoft.DirectX.Direct3D”, and
“Microsoft.DirectX.DirectX3DX”.
Step 5: Go to Properties Section of Form, select Paint in the Event List and enter as Form1_Paint.
Step 6: Edit the Form’s C# code file.
Step 7: When you run this code you get exception for LoaderLock. To solve this exception go in
exception thrown window go to open exception setting ... select and expand managed debugging
assistant ....and uncheck loader lock option then run your program.








Blue_ScreenGP:
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Microsoft.DirectX;
using Microsoft.DirectX.Direct3D;
namespace WindowsFormsApplication5
{
    public partial class Form1 : Form
    {
        Microsoft.DirectX.Direct3D.Device device;
        public Form1()
        {
            InitializeComponent();
            InitDevice();
            Console.WriteLine("Printing Form1 method1");
        }
        private void InitDevice()
        {
            PresentParameters pp = new PresentParameters(); //CREATE OBJECT
            pp.Windowed = true;
            pp.SwapEffect = SwapEffect.Discard;
            device = new Device(0, DeviceType.Hardware, this, CreateFlags.HardwareVertexProcessing,
            pp);
            Console.WriteLine("Printing Form1 Init");
        }
        private void Render()
        {
            device.Clear(ClearFlags.Target, Color.CornflowerBlue, 0, 1);
            device.Present();
            Console.WriteLine("Printing Form1 Render Method call");
        }
        
        private void Form1_Paint_1(object sender, PaintEventArgs e)
        {
            Console.WriteLine("Printing Form1 Render Method call paint");
            Render();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Console.WriteLine("Printing Form1 Render Method call load");
        }
    }
}

"""
        )



def ImageWindowGP():
    print(
"""
ImageWindowGP:
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Microsoft.DirectX;
using Microsoft.DirectX.Direct3D;
namespace WindowsFormsApplication10
{
    public partial class Form1 : Form
    {
        Microsoft.DirectX.Direct3D.Device device;
        Microsoft.DirectX.Direct3D.Texture texture;
        Microsoft.DirectX.Direct3D.Font font;
        public Form1()
        {
            InitializeComponent();
            InitDevice();
            InitFont();
            LoadTexture();
        }
        private void InitFont()
        {
            System.Drawing.Font f = new System.Drawing.Font("Arial", 16f, FontStyle.Regular);
            font = new Microsoft.DirectX.Direct3D.Font(device, f);
        }
        private void LoadTexture()
        {
            texture = TextureLoader.FromFile(device, "C:/Users/91885/Downloads/imgtest.jpg", 551,310, 1, 0, Format.A8B8G8R8, Pool.Managed, Filter.Point, Filter.Point, Color.Transparent.ToArgb());
        }
        private void InitDevice()
        {
            PresentParameters pp = new PresentParameters();
            pp.Windowed = true;
            pp.SwapEffect = SwapEffect.Discard;
            device = new Device(0, DeviceType.Hardware, this, CreateFlags.HardwareVertexProcessing, pp);

        }
        private void Render()
        {
            device.Clear(ClearFlags.Target, Color.CornflowerBlue, 0, 1);
            device.BeginScene();
            using (Sprite s = new Sprite(device))
            {
                s.Begin(SpriteFlags.AlphaBlend);
                s.Draw2D(texture, new Rectangle(0, 0, 0, 0), new Rectangle(0, 0, device.Viewport.Width,device.Viewport.Height), new Point(0, 0), 0f, new Point(0, 0), Color.White);
                font.DrawText(s, "Vaibhav T095", new Point(0, 0), Color.White);
                s.End();
            }
            device.EndScene();
            device.Present();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void Form1_Paint(object sender, PaintEventArgs e)
        {
            Render();
        }
    }
}

"""
        )



def TraingleDrawGP():
    print(
"""
TraingleDrawGP:
using Microsoft.DirectX.Direct3D;

using Microsoft.DirectX;
using Microsoft.DirectX.Direct3D;
using System.Drawing;
using System.Windows.Forms;
namespace DxPrac1
{
    public partial class Form1 : Form
    {
        Device d;
        public Form1()
        {
            InitializeComponent();
            InitDevice();
        }
        void InitDevice()
        {
            PresentParameters presentParameters = new
            PresentParameters();
            presentParameters.Windowed = true;
            presentParameters.SwapEffect =
            SwapEffect.Discard;
            d = new Device(0, DeviceType.Hardware, this,
            CreateFlags.HardwareVertexProcessing,
            presentParameters);
        }
        void Render()
        {
            CustomVertex.TransformedColored[] vertex = new
            CustomVertex.TransformedColored[3];
            vertex[0].Position = new Vector4(200, 75, 0,
            0);
            vertex[0].Color = Color.Red.ToArgb();
            vertex[1].Position = new Vector4(300, 250, 0,
            0);
            vertex[1].Color = Color.Green.ToArgb();
            vertex[2].Position = new Vector4(100, 250, 0,
            0);
            vertex[2].Color = Color.Blue.ToArgb();
            d.Clear(ClearFlags.Target, Color.White, 0, 1);
            d.BeginScene();
            d.VertexFormat =
            CustomVertex.TransformedColored.Format;
            d.DrawUserPrimitives(PrimitiveType.TriangleList
            , 1, vertex);
            d.EndScene();
            d.Present();
        }



        private void Form1_Load(object sender, System.EventArgs e)
        {

        }

        private void Form1_Paint_1(object sender, PaintEventArgs e)
        {
            Render();
        }
    }
}

"""
        )




def PyGameShapes():
    print(
"""
PyGameShapes:
import pygame  
from math import pi  
pygame.init()  
# size variable is using for set screen size  
size = [900, 550]  
screen = pygame.display.set_mode(size)  
pygame.display.set_caption("Example program to draw geometry")  
# done variable is using as flag   
done = False  
clock = pygame.time.Clock()  
while not done:  
    # clock.tick() limits the while loop to a max of 10 times per second.  
    clock.tick(10)
  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True 
    screen.fill((0, 0, 0))  

    pygame.draw.line(screen, (0, 255, 0), [0, 0], [50, 30], 5)  
    pygame.draw.lines(screen, (0, 0, 0), False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5) 
    pygame.draw.rect(screen, (0, 0, 0), [75, 10, 50, 20], 2)
    pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])
    pygame.draw.ellipse(screen, (255, 0, 0), [225, 10, 50, 20], 2)
    pygame.draw.ellipse(screen, (255, 0, 0), [300, 10, 50, 20])
    pygame.draw.polygon(screen, (0, 0, 0), [[100, 100], [0, 200], [200, 200]], 5)
    pygame.draw.circle(screen, (0, 0, 255), [60, 250], 40)
    pygame.draw.arc(screen, (0, 0, 0), [210, 75, 150, 125], 0, pi / 2, 2)
    pygame.display.flip()  
  
# Quite the execution when clicking on close  
pygame.quit()

"""
        )


def PyGameImageWindow():
    print(
"""
PyGameImageWindow:
import pygame  
pygame.init()  
white = (255, 255, 255)  
# assigning values to height and width variable   
height = 550 
width = 900
# creating the display surface object   
# of specific dimension..e(X, Y).   
display_surface = pygame.display.set_mode((width, height))  
  
# set the pygame window name   
pygame.display.set_caption('Image')  
  
# creating a surface object, image is drawn on it.   
image = pygame.image.load(r'Practical 02\assets\gaming-virtual-blue-adobestock.webp')  
  
# infinite loop   
while True:  
    display_surface.fill(white)  
    display_surface.blit(image, (0, 0))  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            # quit the program.   
            quit()  
        # Draws the surface object to the screen.   
        pygame.display.update()
"""
        )



def PyGameKeyDown():
    print(
"""
PyGameKeyDown:
import pygame  
pygame.init()  
# sets the window title  
pygame.display.set_caption(u'Keyboard events')  
# sets the window size  
pygame.display.set_mode((900, 550))  
  
while True:  
    # gets a single event from the event queue  
    event = pygame.event.wait()  
    # if the 'close' button of the window is pressed  
    if event.type == pygame.QUIT:  
        # stops the application  
        break  
    # Detects the 'KEYDOWN' and 'KEYUP' events  
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):  
        # gets the key name  
        key_name = pygame.key.name(event.key)  
        # converts to uppercase the key name  
        key_name = key_name.upper()  
        # if any key is pressed  
        if event.type == pygame.KEYDOWN:  
            # prints on the console the key pressed  
            print(u'"{}" key pressed'.format(key_name))  
        # if any key is released  
        elif event.type == pygame.KEYUP:  
            # prints on the console the released key  
            print(u'"{}" key released'.format(key_name))

"""
        )






def PyGameRect():
    print(
"""
PyGameRect:
import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((900, 550))  
done = False  
  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
    pygame.draw.rect(screen, (0, 125, 255), pygame.Rect(30, 30, 60, 60))    
  
    pygame.display.flip()  

"""
        )



def PyGameTextFont():
    print(
"""
PyGameTextFont:
import pygame  
pygame.init()  
screen = pygame.display.set_mode((900, 550))  
done = False  
  
#load the fonts  
font = pygame.font.SysFont("Times new Roman", 72)  
# Render the text in new surface  
text = font.render("Hello, Game Programmers", True, (200, 16, 16))  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  
            done = True  
    screen.fill((255, 255, 255))  
    #We will discuss blit() in the next topic  
    screen.blit(text,(450 - text.get_width() // 2, 240 - text.get_height() // 2))  
  
    pygame.display.flip()
"""
        )



def PyGameWindow():
    print(
"""
PyGameWindow:
import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((600,400))  
done = False  
  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
    pygame.display.flip()

"""
        )


def PYGAME():
    print(
"""
PYGAME:
1
import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((400,500))  
done = False  
  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
    pygame.display.flip()  


2
import pygame  
pygame.init()  
white = (255, 255, 255)  
# assigning values to height and width variable   
height = 400  
width = 400  
# creating the display surface object   
# of specific dimension..e(X, Y).   
display_surface = pygame.display.set_mode((height, width))  
  
# set the pygame window name   
pygame.display.set_caption('Image')  
  
# creating a surface object, image is drawn on it.   
image = pygame.image.load(r'D:/Game programming/1.jpg')  
  
# infinite loop   
while True:  
    display_surface.fill(white)  
    display_surface.blit(image, (0, 0))  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            # quit the program.   
            quit()  
        # Draws the surface object to the screen.   
        pygame.display.update()   

3
import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((400, 300))  
done = False  
  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
    pygame.draw.rect(screen, (0, 125, 255), pygame.Rect(30, 30, 60, 60))    
  
    pygame.display.flip()  

4
import pygame  
pygame.init()  
# sets the window title  
pygame.display.set_caption(u'Keyboard events')  
# sets the window size  
pygame.display.set_mode((400, 400))  
  
while True:  
    # gets a single event from the event queue  
    event = pygame.event.wait()  
    # if the 'close' button of the window is pressed  
    if event.type == pygame.QUIT:  
        # stops the application  
        break  
    # Detects the 'KEYDOWN' and 'KEYUP' events  
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):  
        # gets the key name  
        key_name = pygame.key.name(event.key)  
        # converts to uppercase the key name  
        key_name = key_name.upper()  
        # if any key is pressed  
        if event.type == pygame.KEYDOWN:  
            # prints on the console the key pressed  
            print(u'"{}" key pressed'.format(key_name))  
        # if any key is released  
        elif event.type == pygame.KEYUP:  
            # prints on the console the released key  
            print(u'"{}" key released'.format(key_name))  


5
import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((400, 300))  
done = False  
is_blue = True  
x = 30  
y = 30  
  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
            is_blue = not is_blue  
  
    pressed = pygame.key.get_pressed()  
    if pressed[pygame.K_UP]: y -= 3  
    if pressed[pygame.K_DOWN]: y += 3  
    if pressed[pygame.K_LEFT]: x -= 3  
    if pressed[pygame.K_RIGHT]: x += 3  
  
    if is_blue:  
        color = (0, 128, 255)  
    else:   
        color = (255, 100, 0)  
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))  
  
    pygame.display.flip()  

6
import pygame
from math import pi
pygame.init()

size = [400, 300]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Example program to draw geometry")

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill((0, 0, 0))
    
    pygame.draw.line(screen, (0, 255, 0), [0, 0], [50, 30], 5)
    pygame.draw.lines(screen, (0, 0, 0), False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
    pygame.draw.rect(screen, (0, 0, 0), [75, 10, 50, 20], 2)
    pygame.draw.rect(screen, (0, 0, 0), [150, 10, 50, 20])
    pygame.draw.ellipse(screen, (255, 0, 0), [225, 10, 50, 20], 2)
    pygame.draw.ellipse(screen, (255, 0, 0), [300, 10, 50, 20])
    pygame.draw.polygon(screen, (0, 0, 0), [[100, 100], [0, 200], [200, 200]], 5)
    pygame.draw.circle(screen, (0, 0, 255), [60, 250], 40)
    pygame.draw.arc(screen, (0, 0, 0), [210, 75, 150, 125], 0, pi / 2, 2)
    
    pygame.display.flip()

pygame.quit()


7
import pygame  
pygame.init()  
screen = pygame.display.set_mode((640, 480))  
done = False  
  
#load the fonts  
font = pygame.font.SysFont("Times new Roman", 72)  
# Render the text in new surface  
text = font.render("Hello, Pygame", True, (158, 16, 16))  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  
            done = True  
    screen.fill((255, 255, 255))  
    #We will discuss blit() in the next topic  
    screen.blit(text,(320 - text.get_width() // 2, 240 - text.get_height() // 2))  
  
    pygame.display.flip()  

8
import pygame  
import sys  
#Sprite class   
class Sprite(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.image.fill((255, 0, 255))  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  
def main():  
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 50  
    bg = [0, 0, 0]  
    size =[300, 300]  
    screen = pygame.display.set_mode(size)  
    player = Sprite([40, 50])  
    # Define keys for player movement  
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
    player.vx = 5  
    player.vy = 5  
  
    wall = Sprite([100, 60])  
  
    wall_group = pygame.sprite.Group()  
    wall_group.add(wall)  
  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False  
        key = pygame.key.get_pressed()  
        for i in range(2):  
            if key[player.move[i]]:  
                player.rect.x += player.vx * [-1, 1][i]  
  
        for i in range(2):  
            if key[player.move[2:4][i]]:  
                player.rect.y += player.vy * [-1, 1][i]  
        screen.fill(bg)  
        # first parameter takes a single sprite  
        # second parameter takes sprite groups  
        # third parameter is a kill command if true  
        hit = pygame.sprite.spritecollide(player, wall_group, True)  
        if hit:  
        # if collision is detected call a function to destroy  
            # rect  
            player.image.fill((255, 255, 255))  
        player_group.draw(screen)  
        wall_group.draw(screen)  
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  
if __name__ == '__main__':
    main()

9
import pyglet  
window = pyglet.window.Window()  
lable = pyglet.text.Label('Hello world', font_name='Times New Roman', font_size=36,  
                          x= window.width//2,y=window.height//2,anchor_x='center', anchor_y='center')  
@window.event  
def on_draw():  
    window.clear()  
    lable.draw()  
pyglet.app.run()

"""
        )



def Caesar_Cipher():
    print(
"""
Caesar_Cipher:
def encrypt(text, s):
  result = ""
  for i in range(len(text)):
    char = text[i]
    # Encrypt uppercase characters
    if (char.isupper()):
      result += chr((ord(char) + s-65) % 26 + 65)
    # Encrypt lowercase characters
    else:
      result += chr((ord(char) + s - 97) % 26 + 97)
  return result

#check the above function
text=input("Enter the text to encrypt: ")
s = 3
print("Text :" + text)
str(s)
print("Cipher: " + encrypt(text,s))
"""
        )

def RSA():
    print(
"""
RSA:
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
keyPair = RSA.generate(1024)
pubKey = keyPair.publickey()
print(f"Public key: (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))
print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))
#encryption
msg = 'Vaibhav Patel'
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(bytes(msg,"utf-8"))
print("Encrypted:", binascii.hexlify(encrypted))
"""
        )


def MD5():
    print(
"""
MD5:
import hashlib
result = hashlib.md5(b'Ismile')
result1 = hashlib.md5(b'Esmile')
# printing the equivalent byte value.
print("The byte equivalent of hash is : ", end ="")
print(result.digest())
print("The byte equivalent of hash is : ", end ="")
print(result1.digest())

"""
        )


def SHA():
    print(
"""
SHA:
import hashlib
str = input("Enter the value to encode ")
result = hashlib.sha1(str.encode())
print("The hexadecima equivalent if SHA1 is : ")
print(result.hexdigest())
"""
        )

def SHA2():
    print(
"""
SHA2:
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
# Generate RSA key pair
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
# Simulated document content
original_document = b"This is the original document content."
modified_document = b"This is the modified document content."
# Hash the document content
original_hash = SHA256.new(original_document)
modified_hash = SHA256.new(modified_document)
# Create a signature using the private key
signature = pkcs1_15.new(RSA.import_key(private_key)).sign(original_hash)
# Verify the signature using the public key with the modified content
try:
    pkcs1_15.new(RSA.import_key(public_key)).verify(modified_hash, signature)
    print("Signature is valid.")
except (ValueError, TypeError):
    print("Signature is invalid.")
"""
        )

def DiffieHellman():
    print(
"""
DiffieHellman:
from random import randint
if __name__ == '__main__':
    P = 23
    G = 9
    print('The Value of P is :%d'%(P))
    print('The Value of G is :%d'%(G))
    a = 4
    print('Secret Number for Alice is :%d'%(a))
    x = int(pow(G,a,P))
    b = 6
    print('Secret Number for Bob is :%d'%(b))
    y = int(pow(G,b,P))
    ka = int(pow(y,a,P))
    kb = int(pow(x,b,P))
    print('Secret key for the Alice is : %d'%(ka))
    print('Secret Key for the Bob is : %d'%(kb))
"""
        )


def Railfence():
    print(
"""
public class railfence {
public static void main(String args[])
{
String input = "vaibhav";
String output = "";
int len = input.length(),flag = 0;
System.out.println("Input String : " + input);
for(int i=0;i<len;i+=2) {
    output += input.charAt(i);
}
for(int i=1;i<len;i+=2) {
    output += input.charAt(i);
}
    System.out.println("Ciphered Text : "+output);
}
}
"""
        )

def Railfence2():
    print(
"""
Railfence2:
def rail_fence_encrypt(text, rails):
    fence = [[' ' for _ in range(len(text))] for _ in range(rails)]
    direction = -1  # Direction to move along the rails (up or down)
    row, col = 0, 0  # Initial position on the rail fence

    for char in text:
        fence[row][col] = char
        if row == 0 or row == rails - 1:
            direction *= -1  # Change direction at the top or bottom rail
        row += direction
        col += 1

    encrypted_text = ''.join([''.join(row) for row in fence]).replace(" ", "")  # Remove spaces
    return encrypted_text

def rail_fence_decrypt(encrypted_text, rails):
    fence = [[' ' for _ in range(len(encrypted_text))] for _ in range(rails)]
    direction = -1  # Direction to move along the rails (up or down)
    row, col = 0, 0  # Initial position on the rail fence

    for _ in range(len(encrypted_text)):
        fence[row][col] = 'X'  # Mark the positions on the fence
        if row == 0 or row == rails - 1:
            direction *= -1  # Change direction at the top or bottom rail
        row += direction
        col += 1

    decrypted_text = ''
    text_index = 0

    for row in range(rails):
        for col in range(len(encrypted_text)):
            if fence[row][col] == 'X':
                fence[row][col] = encrypted_text[text_index]
                text_index += 1

    direction = -1  # Reset the direction for reading
    row, col = 0, 0

    for _ in range(len(encrypted_text)):
        decrypted_text += fence[row][col]
        if row == 0 or row == rails - 1:
            direction *= -1  # Change direction at the top or bottom rail
        row += direction
        col += 1

    return decrypted_text

if __name__ == "__main__":
    text = input("Enter the text to encrypt: ")
    rails = int(input("Enter the number of rails: "))

    encrypted_text = rail_fence_encrypt(text, rails)
    print("Cipher: " + encrypted_text)

    decrypted_text = rail_fence_decrypt(encrypted_text, rails)
    print("Decrypted Text: " + decrypted_text)

"""
        )





def ClientServerINSClient1():
    print(
"""
ClientServerINSClient1:
import urllib.request
import ssl

# Define the URL to fetch
url = "https://localhost:4443/"

# Create an SSL context with certificate validation
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cafile=r'practical 07\certificate_&_Key\server_cert.pem')  # Load the server certificate

try:
    while True:
        user_input = input("Enter text to send to the server ('q' to quit): ")
        
        if user_input.lower() == 'q':
            break

        print("Sent to server:", user_input)
        
        # Encode the input as bytes
        user_input_bytes = user_input.encode('utf-8')
        
        # Create a POST request and send the input as the request body
        req = urllib.request.Request(url, data=user_input_bytes, method='POST')
        
        try:
            with urllib.request.urlopen(req, context=ssl_context) as response:
                print(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            print("Error:", e.reason)

except KeyboardInterrupt:
    print("Client disconnected.")

"""
        )


def ClientServerINSServer1():
    print(
"""
ClientServerINSServer1:
import http.server
import ssl

class CustomRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the request data
        content_length = int(self.headers['Content-Length'])
        # Read the request data
        response_message = self.rfile.read(content_length).decode('utf-8')

        # Print the received message from the client
        print("Response from client:", response_message)

        # Send a message to the client
        user_input = input("Enter text to send to the client ('q' to quit): ")

        if user_input.lower() == 'q':
            return

        # acknowledging a sended message to the client 
        print("Sent to client:", user_input)

        # Send the response back to the client
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(("Response from server: " + user_input).encode('utf-8'))

# Define the server address and port
server_address = ('localhost', 4443)

# Load SSL/TLS certificates
certfile = r'practical 07\certificate_&_Key\server_cert.pem'
keyfile = r'practical 07\certificate_&_Key\server_key.pem'

# Configure SSL/TLS settings
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile, keyfile)

# Create a custom HTTP server with SSL/TLS
httpd = http.server.HTTPServer(server_address, CustomRequestHandler)
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print("Server started at", server_address)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
"""
        )


def INSClient1():
    print(
"""
INSClient1:
import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {
        Socket socket = null;
        InputStreamReader inputStreamReader = null;
        OutputStreamWriter outputStreamWriter = null;
        BufferedReader bufferedReader = null;
        BufferedWriter bufferedWriter = null;

        try {
            socket = new Socket("localhost", 5000);
            inputStreamReader = new InputStreamReader(socket.getInputStream());
            outputStreamWriter = new OutputStreamWriter(socket.getOutputStream());
            bufferedReader = new BufferedReader(inputStreamReader);
            bufferedWriter = new BufferedWriter(outputStreamWriter);

            Scanner scanner = new Scanner(System.in);
            String msgToSend;

            while (true) {
                System.out.print("Client: ");
                msgToSend = scanner.nextLine();
                bufferedWriter.write(msgToSend);
                bufferedWriter.newLine();
                bufferedWriter.flush();

                String response = bufferedReader.readLine();
                System.out.println("Server: " + response);

                if (msgToSend.equalsIgnoreCase("BYE"))
                    break;
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (socket != null)
                    socket.close();
                if (inputStreamReader != null)
                    inputStreamReader.close();
                if (outputStreamWriter != null)
                    outputStreamWriter.close();
                if (bufferedReader != null)
                    bufferedReader.close();
                if (bufferedWriter != null)
                    bufferedWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

"""
        )


def INSServer1():
    print(
"""
INSServer1:
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(5000);

        while (true) {
            try {
                Socket socket = serverSocket.accept();

                InputStreamReader inputStreamReader = new InputStreamReader(socket.getInputStream());
                OutputStreamWriter outputStreamWriter = new OutputStreamWriter(socket.getOutputStream());
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                BufferedWriter bufferedWriter = new BufferedWriter(outputStreamWriter);

                String msgFromClient;
                while ((msgFromClient = bufferedReader.readLine()) != null) {
                    System.out.println("Client: " + msgFromClient);
                    bufferedWriter.write("MSG Received");
                    bufferedWriter.newLine();
                    bufferedWriter.flush();

                    if (msgFromClient.equalsIgnoreCase("BYE"))
                        break;
                }

                socket.close();
                inputStreamReader.close();
                outputStreamWriter.close();
                bufferedReader.close();
                bufferedWriter.close();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

"""
        )




def PyGameHello():
    print(
"""
PyGameHello:
import pygame  
pygame.init()  
screen = pygame.display.set_mode((640, 480))  
done = False  
  
#load the fonts  
font = pygame.font.SysFont("Times new Roman", 72)  
# Render the text in new surface  
text = font.render("Hello, Pygame", True, (158, 16, 16))  
while not done:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  
            done = True  
    screen.fill((255, 255, 255))  
    #We will discuss blit() in the next topic  
    screen.blit(text,(320 - text.get_width() // 2, 240 - text.get_height() // 2))  
  
    pygame.display.flip()  
"""
        )


def SnakeGame():
    print(
"""
SnakeGame:
import pygame, time, random
 
pygame.init()
 
score_color = (8, 6, 154)
snake_color = (0, 0, 0)
red = (213, 50, 80)
green = (4, 216, 2)
food_color = (218, 93, 0)
 
width = 700
height = 500
 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Python Snake Game by Etutorialspoint')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
msg_font = pygame.font.SysFont("Courier", 20)
score_font = pygame.font.SysFont("Times New Roman", 30)
 
# Draw Snake 
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, snake_color, [x[0], x[1], snake_block, snake_block])

# Get Total Score
def total_score(score):
    value = score_font.render("Total Score: " + str(score), True, score_color)
    screen.blit(value, [0, 0])        

# Display message when Game Over 
def message(msg, color):
    mesg = msg_font.render(msg, True, color)
    screen.blit(mesg, [width / 10, height / 3])

# Draw Food
def draw_food(x, y, radius):
    pygame.draw.circle(screen, food_color, [int(x), int(y)], radius)
 
# Main Game Loop 
def main():
    game_over = False
    game_close = False
 
    x1 = width / 2
    y1 = height / 2
 
    x1_move = 0
    y1_move = 0
 
    snake_list = []
    snake_length = 1
 
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10
 
    while not game_over:
 
        while game_close == True:
            screen.fill(green)
            message("You Lost The Game! Press A to Play Again OR Q to Quit", red)
            total_score(snake_length - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_a:
                        main()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_move = -snake_block
                    y1_move = 0
                elif event.key == pygame.K_RIGHT:
                    x1_move = snake_block
                    y1_move = 0
                elif event.key == pygame.K_UP:
                    y1_move = -snake_block
                    x1_move = 0
                elif event.key == pygame.K_DOWN:
                    y1_move = snake_block
                    x1_move = 0
 
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_move
        y1 += y1_move

        # Fill Screen Background
        screen.fill(green)
        
        draw_food(foodx, foody, 6)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
 
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
 
        snake(snake_block, snake_list)
        total_score(snake_length - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
# Call Main Game Loop 
main()
"""
        )


def Infinite_Scroll():
    print(
"""
Infinite_Scroll
Code:
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InfinteScroll : MonoBehaviour
{
    public float horizontal_speed = 0.2f;

    public float vertical_speed = 0.2f;

    private Renderer re;

    // Start is called before the first frame update
    void Start()
    {
        re = GetComponent<Renderer>();
    }

    // Update is called once per frame
    void Update()
    {
        Vector2 offset = new Vector2(Time.time * horizontal_speed, Time.time * vertical_speed);
        re.material.mainTextureOffset = offset;
    }
}
"""
        )


def Decision_Tree1():
    print(
"""
Decision_Tree1:
# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Decision Tree classifier
clf = DecisionTreeClassifier(random_state=42)

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

"""
        )

def Feed_Forward_Backpropogation1():
    print(
"""
Feed_Forward_Backpropogation1:
# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Convert labels to one-hot encoding
y_one_hot = to_categorical(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42)

# Standardize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a Feedforward Neural Network
model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=5, verbose=1)

# Make predictions on the test data
y_pred_prob = model.predict(X_test)
y_pred = [round(prob.argmax()) for prob in y_pred_prob]

# Evaluate the model
accuracy = accuracy_score(y_test.argmax(axis=1), y_pred)
report = classification_report(y_test.argmax(axis=1), y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)
"""
        )

def SVM1():
    print(
"""
SVM1:
# Import necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create an SVM classifier
svm_classifier = SVC(kernel='linear', C=1)

# Train the SVM model
svm_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = svm_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

"""
        )



def AdaBoost1():
    print(
"""
AdaBoost1:
# Import necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a base decision tree classifier
base_classifier = DecisionTreeClassifier(max_depth=1)

# Create an AdaBoost classifier
adaboost_classifier = AdaBoostClassifier(base_classifier, n_estimators=50, random_state=42)

# Train the AdaBoost model
adaboost_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = adaboost_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)
"""
        )

def Naive_Bayes1():
    print(
"""
Naive_Bayes1:
# Import necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Gaussian Naive Bayes classifier
naive_bayes_classifier = GaussianNB()

# Train the Naive Bayes model
naive_bayes_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = naive_bayes_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

"""
        )



def KNN1():
    print(
"""
KNN1:
# Import necessary libraries
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose the number of neighbors (you can experiment with different values)
k_neighbors = 3

# Create a KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=k_neighbors)

# Train the KNN model
knn_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = knn_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

"""
        )





def Apriori1():
    print(
"""
Apriori1:
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn import datasets

# Mapping between bin labels, item names, and corresponding category labels
item_mapping = {
    '0-1': {'item': 'alcohol', 'label': 'A'},
    '0-5': {'item': 'flavanoids', 'label': 'B'},
    '1-2': {'item': 'flavanoids', 'label': 'C'},
    '12-13': {'item': 'color_intensity', 'label': 'D'},
    '13-14': {'item': 'color_intensity', 'label': 'E'},
    '2-3': {'item': 'flavanoids', 'label': 'F'},
    '3-4': {'item': 'flavanoids', 'label': 'G'},
    '5-10': {'item': 'color_intensity', 'label': 'H'},
    '10-15': {'item': 'color_intensity', 'label': 'I'},
    '15-20': {'item': 'color_intensity', 'label': 'J'}
}

# Load the wine dataset
wine = datasets.load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Binning numerical features into categories to create a transaction-like dataset
df['alcohol'] = pd.cut(df['alcohol'], bins=[11, 12, 13, 14, 15], labels=['11-12', '12-13', '13-14', '14-15'])
df['flavanoids'] = pd.cut(df['flavanoids'], bins=[0, 1, 2, 3, 4], labels=['0-1', '1-2', '2-3', '3-4'])
df['color_intensity'] = pd.cut(df['color_intensity'], bins=[0, 5, 10, 15, 20], labels=['0-5', '5-10', '10-15', '15-20'])

# Keep only the categorical columns
df = df[['alcohol', 'flavanoids', 'color_intensity']]

# Convert all values to strings
df = df.applymap(str)

# Convert the dataframe to a list of lists (transactions)
transactions = df.values.tolist()

# Convert the transactions to a one-hot encoded format
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_encoded, min_support=0.2, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Convert the bin labels to item names and category labels in frequent itemsets
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: [f"{item_mapping[item]['item']} ({item_mapping[item]['label']})" for item in x])

# Convert the bin labels to item names and category labels in association rules
rules['antecedents'] = rules['antecedents'].apply(lambda x: [f"{item_mapping[item]['item']} ({item_mapping[item]['label']})" for item in x])
rules['consequents'] = rules['consequents'].apply(lambda x: [f"{item_mapping[item]['item']} ({item_mapping[item]['label']})" for item in x])

# Print the results
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)
"""
        )


def Apriori2():
    print(
"""
Apriori2:
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn import datasets

# Mapping between bin labels and item names
item_mapping = {'0-1': 'A', '0-5': 'B', '1-2': 'C', '12-13': 'D', '13-14': 'E', '2-3': 'F', '3-4': 'G', '5-10': 'H', '10-15': 'I', '15-20': 'J'}

# Load the wine dataset
wine = datasets.load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Binning numerical features into categories to create a transaction-like dataset
df['alcohol'] = pd.cut(df['alcohol'], bins=[11, 12, 13, 14, 15], labels=['11-12', '12-13', '13-14', '14-15'])
df['flavanoids'] = pd.cut(df['flavanoids'], bins=[0, 1, 2, 3, 4], labels=['0-1', '1-2', '2-3', '3-4'])
df['color_intensity'] = pd.cut(df['color_intensity'], bins=[0, 5, 10, 15, 20], labels=['0-5', '5-10', '10-15', '15-20'])

# Keep only the categorical columns
df = df[['alcohol', 'flavanoids', 'color_intensity']]

# Convert all values to strings
df = df.applymap(str)

# Convert the dataframe to a list of lists (transactions)
transactions = df.values.tolist()

# Convert the transactions to a one-hot encoded format
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_encoded, min_support=0.2, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Convert the bin labels to item names in frequent itemsets
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: [item_mapping[item] for item in x])

# Convert the bin labels to item names in association rules
rules['antecedents'] = rules['antecedents'].apply(lambda x: [item_mapping[item] for item in x])
rules['consequents'] = rules['consequents'].apply(lambda x: [item_mapping[item] for item in x])

# Print the results
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)
Apriori2:
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn import datasets

# Mapping between bin labels and item names
item_mapping = {'0-1': 'A', '0-5': 'B', '1-2': 'C', '12-13': 'D', '13-14': 'E', '2-3': 'F', '3-4': 'G', '5-10': 'H', '10-15': 'I', '15-20': 'J'}

# Load the wine dataset
wine = datasets.load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Binning numerical features into categories to create a transaction-like dataset
df['alcohol'] = pd.cut(df['alcohol'], bins=[11, 12, 13, 14, 15], labels=['11-12', '12-13', '13-14', '14-15'])
df['flavanoids'] = pd.cut(df['flavanoids'], bins=[0, 1, 2, 3, 4], labels=['0-1', '1-2', '2-3', '3-4'])
df['color_intensity'] = pd.cut(df['color_intensity'], bins=[0, 5, 10, 15, 20], labels=['0-5', '5-10', '10-15', '15-20'])

# Keep only the categorical columns
df = df[['alcohol', 'flavanoids', 'color_intensity']]

# Convert all values to strings
df = df.applymap(str)

# Convert the dataframe to a list of lists (transactions)
transactions = df.values.tolist()

# Convert the transactions to a one-hot encoded format
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_encoded, min_support=0.2, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Convert the bin labels to item names in frequent itemsets
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: [item_mapping[item] for item in x])

# Convert the bin labels to item names in association rules
rules['antecedents'] = rules['antecedents'].apply(lambda x: [item_mapping[item] for item in x])
rules['consequents'] = rules['consequents'].apply(lambda x: [item_mapping[item] for item in x])

# Print the results
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)

"""
        )




def Apriori3():
    print(
"""
Apriori3:
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn import datasets

# Load the wine dataset
wine = datasets.load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Binning numerical features into categories to create a transaction-like dataset
df['alcohol'] = pd.cut(df['alcohol'], bins=[11, 12, 13, 14, 15], labels=['11-12', '12-13', '13-14', '14-15'])
df['flavanoids'] = pd.cut(df['flavanoids'], bins=[0, 1, 2, 3, 4], labels=['0-1', '1-2', '2-3', '3-4'])
df['color_intensity'] = pd.cut(df['color_intensity'], bins=[0, 5, 10, 15, 20], labels=['0-5', '5-10', '10-15', '15-20'])

# Keep only the categorical columns
df = df[['alcohol', 'flavanoids', 'color_intensity']]

# Convert all values to strings
df = df.applymap(str)

# Convert the dataframe to a list of lists (transactions)
transactions = df.values.tolist()

# Convert the transactions to a one-hot encoded format
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_encoded, min_support=0.2, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Print the results
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)
"""
        )


def TensorFlow1():
    print(
"""
TensorFlow1:
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the Iris dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Preprocess the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Convert labels to one-hot encoding
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
y = tf.keras.utils.to_categorical(y, 3)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1)

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f'\nTest Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')
"""
        )



def Decision_tree2():
    print(
"""
Decision_tree2:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print("Libraries imported ")

df = pd.read_csv('data.csv')
print("dataframe of dataset created")

df.head()

df = df[['diagnosis','radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','compactness_mean','concavity_mean','concave points_mean','radius_worst','texture_worst','perimeter_worst','area_worst','smoothness_worst','compactness_worst','concavity_worst','concave points_worst','symmetry_worst','fractal_dimension_worst']]


df.tail()


df.isnull().sum()

from sklearn.preprocessing import LabelEncoder


le = LabelEncoder()


df['diagnosis'] = le.fit_transform(df.diagnosis)

df.head()



df.tail()

df['radius_mean'] = le.fit_transform(df.radius_mean)

df.tail()


# X- Features  y- Label
X = df[['radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','compactness_mean','concavity_mean','concave points_mean','radius_worst','texture_worst','perimeter_worst','area_worst','smoothness_worst','compactness_worst','concavity_worst','concave points_worst','symmetry_worst','fractal_dimension_worst']]
y= df['diagnosis']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0,criterion='gini')
clf.fit(X_train,y_train)


from sklearn.metrics import accuracy_score
import math
predictions_test=clf.predict(X_test)
print("Accuracy : ",accuracy_score(y_test, predictions_test)*100)



predictions_train = clf.predict(X_train)
accuracy_score(y_train,predictions_train)


from sklearn import tree
plt.figure(figsize=(15,10))
tree.plot_tree(clf,filled=True)
plt.show()


from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,predictions_test))
print(confusion_matrix(y_test,predictions_test))

#Can stop

from sklearn.metrics import roc_curve,auc
from sklearn.metrics import roc_auc_score
dt_probs = clf.predict_proba(X_test)[:,1]
fpr_dt, tpr_dt, thresholds_dt = roc_curve(y_test,dt_probs)
print("FPR :",fpr_dt)
print("TPR :",tpr_dt)
print("Threshold :",thresholds_dt)


path = clf.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities


fig, ax = plt.subplots(figsize=(8,5))
ax.plot(ccp_alphas[:-1], impurities[:-1], marker='o', drawstyle="steps-post")
ax.set_xlabel("effective alpha")
ax.set_ylabel("total impurity of leaves")
ax.set_title("Total Impurity vs effective alpha for training set")


clfs = []
for ccp_alpha in ccp_alphas:
    clf = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    clf.fit(X_train, y_train)
    clfs.append(clf)
print("Number of nodes in the last tree is: {} with ccp_alpha: {}".format(
      clfs[-1].tree_.node_count, ccp_alphas[-1]))


clfs = clfs[:-1]
ccp_alphas = ccp_alphas[:-1]

node_counts = [clf.tree_.node_count for clf in clfs]
depth = [clf.tree_.max_depth for clf in clfs]
fig, ax = plt.subplots(2, 1,figsize=(10,8))
ax[0].plot(ccp_alphas, node_counts, marker='o', drawstyle="steps-post")
ax[0].set_xlabel("alpha")
ax[0].set_ylabel("number of nodes")
ax[0].set_title("Number of nodes vs alpha")
ax[1].plot(ccp_alphas, depth, marker='o', drawstyle="steps-post")
ax[1].set_xlabel("alpha")
ax[1].set_ylabel("depth of tree")
ax[1].set_title("Depth vs alpha")
fig.tight_layout()


train_scores = [clf.score(X_train, y_train) for clf in clfs]
test_scores = [clf.score(X_test, y_test) for clf in clfs]

fig, ax = plt.subplots(figsize=(10,8))
ax.set_xlabel("alpha")
ax.set_ylabel("accuracy")
ax.set_title("Accuracy vs alpha for training and testing sets")
ax.plot(ccp_alphas, train_scores, marker='o', label="train",
        drawstyle="steps-post")
ax.plot(ccp_alphas, test_scores, marker='o', label="test",
        drawstyle="steps-post")
ax.legend()
plt.grid()
plt.show()




clf = DecisionTreeClassifier(random_state=0, ccp_alpha=0.016)
clf.fit(X_train,y_train)


from sklearn.metrics import accuracy_score
pred=clf.predict(X_test)
accuracy_score(y_test, pred)



pred_1 = clf.predict(X_train)
accuracy_score(y_train,pred_1)


from sklearn import tree
plt.figure(figsize=(15,10))
tree.plot_tree(clf,filled=True)

"""
        )



def FeedForwardBackpropgation2():
    print(
"""
FeedForwardBackpropgation2:
import numpy as np

#sigmoid activation function
def sigmoid(x):
    return 1 / (1+np.exp(-x))
import numpy as np

# Load the training data
training_data = np.loadtxt('mnist_train.csv', delimiter=',', dtype=np.float32, skiprows=1)

# Load the test data
test_data = np.loadtxt('mnist_test.csv', delimiter=',', dtype=np.float32, skiprows=1)


print("training_data.shape = ", training_data.shape, " ,  test_data.shape = ", test_data.shape)

class NeuralNetwork:

    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):

        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Weight Initialization with Xavier/He : W2
        self.W2 = np.random.randn(self.input_nodes, self.hidden_nodes) / np.sqrt(self.input_nodes/2)
        self.b2 = np.random.rand(self.hidden_nodes)

        # Weight Initialization Xavier/He : W3
        self.W3 = np.random.randn(self.hidden_nodes, self.output_nodes) / np.sqrt(self.hidden_nodes/2)
        self.b3 = np.random.rand(self.output_nodes)

        # Initialization A3,Z3 : A3 is the result of sigmoid function about Z2
        self.Z3 = np.zeros([1,output_nodes])
        self.A3 = np.zeros([1,output_nodes])

        # Initialization A2,Z2
        self.Z2 = np.zeros([1,hidden_nodes])
        self.A2 = np.zeros([1,hidden_nodes])

        # Initialization A1,Z1
        self.Z1 = np.zeros([1,input_nodes])
        self.A1 = np.zeros([1,input_nodes])

        # Learning rate Initialization
        self.learning_rate = learning_rate

    def feed_forward(self):

        delta = 1e-7    # log Infinite Divergence Prevention

        # Calculate Z1,A1 in the input layer
        self.Z1 = self.input_data
        self.A1 = self.input_data

        # Calculate Z2,A2 in the hidden layer
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = sigmoid(self.Z2)

        # Calculate Z3,A3 in the ouput layer
        self.Z3 = np.dot(self.A2, self.W3) + self.b3
        self.A3 = sigmoid(self.Z3)

        # Calculate the loss function value (error) : cross entropy
        return  -np.sum( self.target_data*np.log(self.A3 + delta) + (1-self.target_data)*np.log((1 - self.A3)+delta ) )

    # For external printing
    def loss_val(self):

        delta = 1e-7    # log Infinite Divergence Prevention

        # Calculate Z1,A1 in the input layer
        self.Z1 = self.input_data
        self.A1 = self.input_data

        # Calculate Z2,A2 in the hidden layer
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = sigmoid(self.Z2)

        # Calculate Z3,A3 in the ouput layer
        self.Z3 = np.dot(self.A2, self.W3) + self.b3
        self.A3 = sigmoid(self.Z3)

        # Calculate the loss function value : cross entropy
        return  -np.sum( self.target_data*np.log(self.A3 + delta) + (1-self.target_data)*np.log((1 - self.A3)+delta ) )

    def train(self, input_data, target_data):   # input_data : 784 , target_data : 10

        self.target_data = target_data
        self.input_data = input_data

        # Calculate an error with the feed foward
        loss_val = self.feed_forward()

        # Calculate loss_3
        loss_3 = (self.A3-self.target_data) * self.A3 * (1-self.A3)

        # Update W3, b3
        self.W3 = self.W3 - self.learning_rate * np.dot(self.A2.T, loss_3)

        self.b3 = self.b3 - self.learning_rate * loss_3

        # Caculate loss_2
        loss_2 = np.dot(loss_3, self.W3.T) * self.A2 * (1-self.A2)

        # Update W2, b2
        self.W2 = self.W2 - self.learning_rate * np.dot(self.A1.T, loss_2)

        self.b2 = self.b2 - self.learning_rate * loss_2

    def predict(self, input_data):        # Shape of input_data is (1, 784) matrix

        Z2 = np.dot(input_data, self.W2) + self.b2
        A2 = sigmoid(Z2)

        Z3 = np.dot(A2, self.W3) + self.b3
        A3 = sigmoid(Z3)

        predicted_num = np.argmax(A3)

        return predicted_num

    # Accuracy measurement
    def accuracy(self, test_data):

        matched_list = []
        not_matched_list = []

        for index in range(len(test_data)):

            label = int(test_data[index, 0])

            # Data normalize for one-hot encoding
            data = (test_data[index, 1:] / 255.0 * 0.99) + 0.01


            # Vector -> Matrix (for the prediction)
            predicted_num = self.predict(np.array(data, ndmin=2))

            if label == predicted_num:
                matched_list.append(index)
            else:
                not_matched_list.append(index)

        print("Current Accuracy = ", 100*(len(matched_list)/(len(test_data))), " %")

        return matched_list, not_matched_list


# Define variables
input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.3
epochs = 1

nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

for i in range(epochs):

    for step in range(len(training_data)):  # train

        # input_data, target_data normalize
        target_data = np.zeros(output_nodes) + 0.01
        target_data[int(training_data[step, 0])] = 0.99
        input_data = ((training_data[step, 1:] / 255.0) * 0.99) + 0.01

        nn.train( np.array(input_data, ndmin=2), np.array(target_data, ndmin=2) )


        # Print the error once every 400 times
        if step % 400 == 0:
            print("step = ", step,  ",  loss_val = ", nn.loss_val())

nn.accuracy(test_data)
"""
        )




def SVM2():
    print(
"""
SVM2:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]
df = pd.read_csv("magic04.data", names=cols)
df.head()

df["class"] = (df["class"] == "g").astype(int)


df.head()

for label in cols[:-1]:
  plt.hist(df[df["class"]==1][label], color='blue', label='gamma', alpha=0.7, density=True)
  plt.hist(df[df["class"]==0][label], color='red', label='hadron', alpha=0.7, density=True)
  plt.title(label)
  plt.ylabel("Probability")
  plt.xlabel(label)
  plt.legend()
  plt.show()


train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])


def scale_dataset(dataframe, oversample=False):
  X = dataframe[dataframe.columns[:-1]].values
  y = dataframe[dataframe.columns[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  if oversample:
    ros = RandomOverSampler()
    X, y = ros.fit_resample(X, y)

  data = np.hstack((X, np.reshape(y, (-1, 1))))

  return data, X, y


train, X_train, y_train = scale_dataset(train, oversample=True)
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)
test, X_test, y_test = scale_dataset(test, oversample=False)



from sklearn.svm import SVC

svm_model = SVC()
svm_model = svm_model.fit(X_train, y_train)


y_pred = svm_model.predict(X_test)
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

"""
        )






def AdaBoost2():
    print(
"""
AdaBoost2:
# Load libraries
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets
# Import train_test_split function
from sklearn.model_selection import train_test_split
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics


from sklearn.datasets import load_breast_cancer
dataset = load_breast_cancer()

X = dataset.data
y = dataset.target



# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test



# Create adaboost classifer object
abc = AdaBoostClassifier(n_estimators=50,
                         learning_rate=1)
# Train Adaboost Classifer
model = abc.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = model.predict(X_test)





# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
"""
        )


def Naive_Bayes2():
    print(
"""
Naive_Bayes2:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler



cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]
df = pd.read_csv("magic04.data", names=cols)
df.head()

df["class"] = (df["class"] == "g").astype(int)


df.head()


for label in cols[:-1]:
  plt.hist(df[df["class"]==1][label], color='blue', label='gamma', alpha=0.7, density=True)
  plt.hist(df[df["class"]==0][label], color='red', label='hadron', alpha=0.7, density=True)
  plt.title(label)
  plt.ylabel("Probability")
  plt.xlabel(label)
  plt.legend()
  plt.show()




train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])


def scale_dataset(dataframe, oversample=False):
  X = dataframe[dataframe.columns[:-1]].values
  y = dataframe[dataframe.columns[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  if oversample:
    ros = RandomOverSampler()
    X, y = ros.fit_resample(X, y)

  data = np.hstack((X, np.reshape(y, (-1, 1))))

  return data, X, y



train, X_train, y_train = scale_dataset(train, oversample=True)
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)
test, X_test, y_test = scale_dataset(test, oversample=False)



from sklearn.metrics import classification_report


from sklearn.naive_bayes import GaussianNB



nb_model = GaussianNB()
nb_model = nb_model.fit(X_train, y_train)


y_pred = nb_model.predict(X_test)
print(classification_report(y_test, y_pred))

"""
        )




def KNN2():
    print(
"""
KNN2:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

cols = ["fLength", "fWidth", "fSize", "fConc", "fConc1", "fAsym", "fM3Long", "fM3Trans", "fAlpha", "fDist", "class"]
df = pd.read_csv("magic04.data", names=cols)
df.head()

df["class"] = (df["class"] == "g").astype(int)




df.head()



for label in cols[:-1]:
  plt.hist(df[df["class"]==1][label], color='blue', label='gamma', alpha=0.7, density=True)
  plt.hist(df[df["class"]==0][label], color='red', label='hadron', alpha=0.7, density=True)
  plt.title(label)
  plt.ylabel("Probability")
  plt.xlabel(label)
  plt.legend()
  plt.show()


train, valid, test = np.split(df.sample(frac=1), [int(0.6*len(df)), int(0.8*len(df))])


def scale_dataset(dataframe, oversample=False):
  X = dataframe[dataframe.columns[:-1]].values
  y = dataframe[dataframe.columns[-1]].values

  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  if oversample:
    ros = RandomOverSampler()
    X, y = ros.fit_resample(X, y)

  data = np.hstack((X, np.reshape(y, (-1, 1))))

  return data, X, y



train, X_train, y_train = scale_dataset(train, oversample=True)
valid, X_valid, y_valid = scale_dataset(valid, oversample=False)
test, X_test, y_test = scale_dataset(test, oversample=False)


from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report


knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)



y_pred = knn_model.predict(X_test)

print(classification_report(y_test, y_pred))

"""
        )



def Apriori2():
    print(
"""
Apriori2:
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Importing the Dataset. My data has not header and I specify that header=None
data = pd.read_csv(r"store_data.csv", low_memory=False, header=None)

#Print top n rows from our dataset
data.head(2)

#Check how many rows and columns we have in our dataset
data.shape

#Let's create an empty list here
list_of_transactions = []
#Append the list
for i in range(0, 7501):
    list_of_transactions.append([str(data.values[i,j]) for j in range(0, 20)])



#Let's see the first element from our list of transactions. We should indicate 0 here because index in Pythn starts with 0
list_of_transactions[0]


# Training apiori algorithm on our list_of_transactions
from apyori import apriori
rules = apriori(list_of_transactions, min_support = 0.004, min_confidence = 0.2, min_lift = 3, min_length = 2)
#So we will train apriori algorithm on our list_of_transactions and get the rules where items appear together minimum 0





# Create a list of rules and print the results
results = list(rules)




#Here is the first rule in list or results
results[0]



#In order to visualize our rules better we need to extract elements from our results list, convert it to pd.data frame and sort strong rules by lift value.
#Here is the code for this. We have extracted left hand side and right hand side items from our rules above, also their support, confidence and lift value
def inspect(results):
    lhs     =  [tuple(result [2] [0] [0]) [0] for result in results]
    rhs     =  [tuple(result [2] [0] [1]) [0] for result in results]
    supports = [result [1] for result in results]
    confidences = [result [2] [0] [2]   for result in results]
    lifts = [result [2] [0] [3]   for result in results]
    return list(zip(lhs,rhs,supports,confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results),columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'] )
resultsinDataFrame.head(3)






#As we have our rules in pd.dataframe we can sort it by lift value using nlargest command. Here we are saying that we need top 6 rule by lift value
resultsinDataFrame.nlargest(n=6, columns='Lift')
"""
        )



def ShootPy():
    print(
"""
ShootPy:
import pygame
import random

# Screen
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vaibhav Patel T095")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Character
character_size = 50
character_speed = 5
character = pygame.Rect(width // 2 - character_size // 2, height - character_size,
                         character_size, character_size)

# Bullets (triangles) properties
bullet_size = 10
bullets = []

# Enemy (circle) properties
enemy_radius = 20
enemies = []

# Initialize score
score = 0

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Initialize score increment cooldown
score_increment_cooldown = 60  # Change this value to adjust the rate of score increment
current_cooldown = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(character.centerx - bullet_size // 2, character.top,
                                     bullet_size, bullet_size)
                bullets.append(bullet)

    # Move bullets
    for bullet in bullets:
        bullet.y -= 10
        if bullet.top < 0:
            bullets.remove(bullet)

    # Spawn enemies
    if random.randint(1, 100) <= 2:
        enemy_x = random.randint(enemy_radius, width - enemy_radius)
        enemy = pygame.Rect(enemy_x - enemy_radius, 0, enemy_radius * 2,
                            enemy_radius * 2)
        enemies.append(enemy)

    # Move enemies
    for enemy in enemies:
        enemy.y += 5
        if enemy.top > height:
            enemies.remove(enemy)
        else:
            # Increment the score when the character successfully dodges an enemy
            if current_cooldown == 0:
                score += 1
                current_cooldown = score_increment_cooldown
            else:
                current_cooldown -= 1

    # Move character
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.x -= character_speed
    if keys[pygame.K_RIGHT]:
        character.x += character_speed

    # Check for collisions
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                score += 1
                enemies.remove(enemy)
                bullets.remove(bullet)

    # Check for character collision with enemies
    for enemy in enemies:
        if character.colliderect(enemy):
            running = False

    # Clear the screen
    screen.fill(white)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.polygon(screen, blue, [(bullet.left, bullet.bottom), (bullet.centerx,
                                          bullet.top), (bullet.right, bullet.bottom)])

    # Draw character
    pygame.draw.rect(screen, red, character)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, red, enemy.center, enemy_radius)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, red)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Limit frame rate to 60 FPS
    clock.tick(60)

# Game over display
font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, red)
screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Wait for a few seconds before closing the game
pygame.time.wait(3000)

# Clean up
pygame.quit()
"""
        )



def ScreenShake():
    print(
"""
ScreenShake.cs:
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScreenShake : MonoBehaviour
{
    public float shakeIntensity = 0.1f;
    public float shakeDuration = 0.2f;
    public KeyCode keyToStopShaking = KeyCode.Space;

    private Vector3 initialPosition;
    private float currentShakeDuration = 0f;

    void Start()
    {
        initialPosition = transform.localPosition;
    }

    void Update()
    {
        if (currentShakeDuration > 0f)
        {
            Vector3 randomOffset = Random.insideUnitSphere * shakeIntensity;
            transform.localPosition = initialPosition + randomOffset;

            currentShakeDuration -= Time.deltaTime;
        }
        else
        {
            transform.localPosition = initialPosition;
        }

        // Keep the shaking effect going until the key is pressed
        if (Input.GetKey(keyToStopShaking))
        {
            currentShakeDuration = shakeDuration;
        }
    }

    public void StartShake()
    {
        currentShakeDuration = shakeDuration;
    }

    public void StopShake()
    {
        currentShakeDuration = 0f;
    }
}
"""
        )



def CameraShake():
    print(
"""
CameraShake.cs:
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraShake : MonoBehaviour
{
    public Transform camTransform;
    public float camShakeDuration;
    public float camShakeAmount;
    public float decrementFactor;

    private Vector3 _camOriginalPosition;

    private void OnEnable()
    {
        _camOriginalPosition = camTransform.position;
    }

    private void Update()
    {
        if (camShakeDuration > 0)
        {
            camTransform.localPosition = _camOriginalPosition + Random.insideUnitSphere * camShakeAmount;

            camShakeDuration -= Time.deltaTime * decrementFactor;

        }
        else
        {
            camShakeDuration = 0f;
            camTransform.localPosition = _camOriginalPosition;
        }

    }
}

"""
        )


def AIChase():
    print(
"""
AIChase.cs:
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AIChase : MonoBehaviour
{
    public GameObject player;
    public float speed;

    private float distance;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        distance = Vector2.Distance(transform.position, player.transform.position);
        Vector2 direction = player.transform.position - transform.position;

        direction.Normalize();
        float angle = Mathf.Atan2(direction.x, direction.y) * Mathf.Rad2Deg;

        

        if (distance < 4 ) {

            transform.position = Vector2.MoveTowards(this.transform.position, player.transform.position, speed * Time.deltaTime);
            transform.rotation = Quaternion.Euler(Vector3.forward * angle);
        }
    }
}
"""
        )



def PlayerMovement():
    print(
"""
PlayerMovement.cs:
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float moveSpeed = 5.0f;

    private void Update()
    {
#if UNITY_EDITOR || UNITY_STANDALONE
        // PC Controls using arrow keys
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");
        Vector3 moveDirection = new Vector3(horizontalInput, verticalInput, 0);
        transform.Translate(moveDirection * moveSpeed * Time.deltaTime);
#elif UNITY_ANDROID
        // Android Touch Controls
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            Vector3 touchPos = Camera.main.ScreenToWorldPoint(touch.position);
            touchPos.z = 0; // Ensure the touch is on the same Z-plane as your player
            transform.position = Vector3.MoveTowards(transform.position, touchPos, moveSpeed * Time.deltaTime);
        }
#endif
    }
}

"""
        )


def SnowFall():
    print(
"""
SnowFall:

Create Snowfall Particle effect in Unity

---

**The steps to perform snowfall particle effect in Unity:**

1. Create a 2D Unity project.
2. Add a Particle System to your scene and rename it to "Snow."
3. Configure the "Snow" particle system:
    1. Set the shape to a box to define the snowfall area.
    2. Adjust the emission rate to around 100 particles per second.
4. Configure the Lifetime:
    1. Create a custom curve that starts at the bottom, rises up, and falls back down.
5. Adjust the Size:
    1. Set "Size over Lifetime" to "Random Between Two Constants" with values 0.05 and 0.2 to vary particle size.
6. Configure Velocity:
    1. Ensure the particles fall from top to bottom. Set the Y-axis velocity to a negative value.
7. Add Noise:
    1. Apply a Noise Module with a strength of 0.2 to add randomness to particle movement.

"""
        )



def DHCP():
    print(
"""
DHCP:
command: ifconfig
sudo nano /etc/default/isc-dhcp-server
add: INTERFACES = "ens33"(acc to ifconfig)

sudo nano /etc/dhcp/dhcpd.conf:
comment: option definitions (domain-name and domain-name-servers)
	option domain-name "example.org"
	option domain-name-servers ns1.example.org, ns.example.org;
remove comment: authoritative

change commented subnet configuration:
subnet 192.168.173.0 netmask 255.255.255.0 {
 range 192.168.173.100 192.168.173.200;
 #option domain-name-servers "ns1.internal.example.org";
 #option domain-name "internal.example.org"
 option subnet-mask 255.255.255.0;
 option routers 192.168.173.255;
 option broadcast-address 192.168.173.255;
 default-lease-time 600;
 max-lease-time 7200;
}

sudo systemctl start isc-dhcp-server
sudo systemctl status isc-dhcp-server
sudo systemctl enable isc-dhcp-server

DHCP Client:
sudo nano /etc/network/interfaces
in this check:
auto lo
iface lo inet loopback
auto ens33
iface ens33 inet dhcp

Check with:
sudo nano /var/lib/dhcp/dhcpd.leases

"""
        )

def DHCP_Client():
    print(
"""
DHCP Client:
sudo nano /etc/network/interfaces
in this check:
auto lo
iface lo inet loopback
auto ens33
iface ens33 inet dhcp

Check with:
sudo nano /var/lib/dhcp/dhcpd.leases
"""
        )


def Various_misc_fucn():
    print(
"""

Various_misc_fucn:
Specify primary IP address and netmask:
sudo ifconfig ens33 192.168.173.131 netmask 255.255.255.0
sudo ifconfig



Change to static IP address
1-Go to network connections
2-Edit connections in the wired settings
3-Add IP address for the system

Disable IPv6:
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
sudo nano /etc/sysctl.conf
add:
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1

sudo sysctl -p
cat /proc/sys/net/ipv6/conf/all/disable_ipv6


Configure services
systemctl start service-name
service --status-all
service --status-all|grep'\[+\]'
update-rc.d -f <servicename> remove
sudo apt install apache2
service --status-all
systemctl stop apache2
service --status-all

service --status-all | grep '\[+\]'

Super user:
sudo su


Add user: 
sudo adduser xyz

Add a user to sudo:
sudo usermod -aG sudo xyz
su -xyz
"""
        )


def NTP_Server():
    print(
"""
NTP_Server:
sudo apt update -y
sudo apt install ntp
sntp --version
sudo nano /etc/ntp.conf
vist: https://support.ntp.org/bin/view/Servers/NTPPoolServers
sudo gedit /etc/ntp.conf

comment the pool default list

copy paste ntp pool list like:
server 0.europe.pool.ntp.org
server 1.europe.pool.ntp.org
server 2.europe.pool.ntp.org
server 3.europe.pool.ntp.org


sudo systemctl restart ntp
sudo systemctl status ntp
sudo ufw allow ntp


NTP Client:
sudo apt install ntpdate
sudo nano /etc/hosts
Add server IP address and hostname;
192.168.173.131(IP address) ubuntu(hostname)

sudo ntpdate ubuntu(hostname)

sudo timedatectl set-ntp off
sudo apt install ntp

sudo nano /etc/ntp.conf
Add line at end:
server ubuntu(hostname) prefer iburst

sudo systemctl restart ntp

ntpq -p

"""
        )



def NTP_Client():
    print(
"""
NTP Client:
sudo apt install ntpdate
sudo nano /etc/hosts
Add server IP address and hostname;
192.168.173.131(IP address) ubuntu(hostname)

sudo ntpdate ubuntu(hostname)

sudo timedatectl set-ntp off
sudo apt install ntp

sudo nano /etc/ntp.conf
Add line at end:
server ubuntu(hostname) prefer iburst

sudo systemctl restart ntp

ntpq -p
"""
        )


def SSHSecure_Shell():
    print(
"""
SSHSecure_SHell
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install openssh-server

sudo nano /etc/ssh/ssh_config
Uncomment:
#Port 22
Add line:
MaxAuthTries 4

sudo service ssh status
sudo service ssh start

SSH Client(Windows):
ping 192.168.173.131(server IP)
Install putty
enter server IP address and port no specified(22)
enter username and password of remote server


SSH Client(Ubuntu):
ssh ubuntu@192.168.173.131(host@IP) -p22(port)
ls
touch demofile
ls
"""
        )


def SSH_ClientWindows():
    print(
"""
SSH Client(Windows):
ping 192.168.173.131(server IP)
Install putty
enter server IP address and port no specified(22)
enter username and password of remote server
"""
        )


def SSHClientUbuntu():
    print(
"""
SSH Client(Ubuntu):
ssh ubuntu@192.168.173.131(host@IP) -p22(port)
ls
touch demofile
ls
"""
        )




def DNS():
    print(
"""
DNS

sudo apt-get update
sudo apt-get install bind9 bind9utils
hostnamectl
set-hostname cs.example.com
hostnamectl
ifconfig
sudo nano /etc/network/interfaces 
add:
	auto ens33
	iface ens33 inet static
	address 192.168.173.132
	netmask 255.255.255.0

sudo cat /etc/hosts
sudo nano etc/hosts change:
	127.0.1.1 ubuntu to cs.example.com


sudo systemctl restart networking
ifconfig
cat /etc/bind/named.conf
sudo nano /etc/bind/named.conf.local 
add:
	zone "example.com" IN {
	type master;
	file "/etc/bind/forward.example.com";
	};
	#192.168.173.132


	zone "173.168.192.in-addr.arpa" IN {
	type master;
	file "/etc/bind/reverse.example.com";
	};

ls
sudo cp db.local forward.example.com
sudo nano /etc/bind/forward.example.com
change:
	localhost to cs.example.com
	127.0.0.1 to IP
add:
	@	IN	NS	cs.example.com.
	@	IN	A	192.168.173.132
	cs	IN	A	192.168.173.132
	host	IN	A	192.168.173.132
	client	IN	A	192.168.173.133
	www	IN	A	192.168.173.133

sudo cp forward.example.com reverse.example.com
sudo nano /etc/bind/reverse.example.com
change:
	localhost to cs.example.com
	127.0.0.1 to IP
add:
	@	IN	NS	cs.example.com.
	@	IN	PTR	example.com.
	cs	IN	A	192.168.173.132
	host	IN	A	192.168.173.132
	client	IN	A	192.168.173.133
	www	IN	A	192.168.173.133
	132	IN	PTR	cs.example.com.
	133	IN	PTR	client.example.com

sudo named-checkconf -z /etc/bind/named.conf
sudo named-checkconf -z /etc/bind/named.conf.local
sudo named-checkzone forward /etc/bind/forward.example.com
sudo named-checkzone reverse /etc/bind/reverse.example.com


sudo systemctl start bind9
sudo chown -R bind:bind /etc/bind
ll
sudo chmod -R 755 /etc/bind
sudo systemctl restart bind9
sudo systemctl status bind9
sudo systemctl enable bind9
sudo ufw allow bind9

sudo nano /etc/network/interfaces
add:
	dns-search example.com
	dns-nameserver 192.168.173.132

sudo systemctl restart networking
sudo nano /etc/resolv.conf
add or change:
	nameserver 192.168.173.132
	search example.com

sudo systemctl restart networking
sudo systemctl restart NetworkManager
ping cs
ping host
nslookup cs
nslookup host
nslookup client

On Client:
hostname
hostnamectl set-hostname client.example.com\
hostname
sudo nano /etc/network/interfaces
add:
	iface ens33 inet static
	address 192.168.173.133
	netmask 255.255.255.0
	dns-search example.com
	dns-nameserver 192.168.173.132

sudo nano /etc/hosts
change or add:
	username to client.example.com
sudo nano /etc/resolv.conf
add or change:
	nameserver 192.168.173.132
	search example.com

"""
        )


def DHCP2():
    print(
"""
DHCP:
command: ifconfig
sudo nano /etc/default/isc-dhcp-server
add: INTERFACES = "ens33"(acc to ifconfig)

sudo nano /etc/dhcp/dhcpd.conf:
comment: option definitions (domain-name and domain-name-servers)
	option domain-name "example.org"
	option domain-name-servers ns1.example.org, ns.example.org;
remove comment: authoritative

	A slightly different configuration for an internal subnet.
	change commented subnet configuration:
	subnet 192.168.173.0 netmask 255.255.255.0 {
 	range 192.168.173.100 192.168.173.200;
 	#option domain-name-servers "ns1.internal.example.org";
 	#option domain-name "internal.example.org"
 	option subnet-mask 255.255.255.0;
 	option routers 192.168.173.255;
 	option broadcast-address 192.168.173.255;
 	default-lease-time 600;
 	max-lease-time 7200;
	}

sudo systemctl start isc-dhcp-server
sudo systemctl status isc-dhcp-server
sudo systemctl enable isc-dhcp-server

DHCP Client:
sudo nano /etc/network/interfaces
in this check or add:
auto lo
iface lo inet loopback
auto ens33
iface ens33 inet dhcp

Check with in server:
sudo nano /var/lib/dhcp/dhcpd.leases

"""
        )

def NFS():
    print(
"""
NFS
sudo apt-get update
sudo apt-get install nfs-kernel-server

sudo mkdir /public
sudo mkdir /private
sudo chmod 755 /public/
sudo chmod 777 /private

sudo nano /etc/exports
add:
	/public		*(ro,sync,no_subtree_check)
	/private	192.168.173.100(rw,sync,no_subtree_check)

sudo exportfs -arvf
sudo systemctl start nfs-kernel-server
sudo systemctl enable nfs-kernel-server
sudo systemctl status nfs-kernel-server

NFS Client:

sudo apt-get update
sudo apt-get install nfs-common
showmount -e 192.168.173.132

sudo mkdir /mnt/public
sudo mkdir /mnt/private
sudo mount -t nfs 192.168.173.132:/public /mnt/public
sudo mount -t nfs 192.168.173.132:/private /mnt/private
mount

sudo nano /etc/fstab
add:
	192.168.173.132:/public /mnt/public nfs defaults,_netdev 0 0
	192.168.173.132:/private /mnt/private nfs defaults,netdev 0 0

sudo umount /mnt/public
sudo umount /mnt/private
sudo mount -a
cd /mnt/public
ls
touch file
cd ../private/
ls
touch file
ll

"""
        )


def NFS_Client():
    print(
"""
NFS Client:

sudo apt-get update
sudo apt-get install nfs-common
showmount -e 192.168.173.132

sudo mkdir /mnt/public
sudo mkdir /mnt/private
sudo mount -t nfs 192.168.173.132:/public /mnt/public
sudo mount -t nfs 192.168.173.132:/private /mnt/private
mount

sudo nano /etc/fstab
add:
	192.168.173.132:/public /mnt/public nfs defaults,_netdev 0 0
	192.168.173.132:/private /mnt/private nfs defaults,netdev 0 0

sudo umount /mnt/public
sudo umount /mnt/private
sudo mount -a
cd /mnt/public
ls
touch file
cd ../private/
ls
touch file
ll

"""
        )



def LDAP():
    print(
"""
LDAP


sudo apt-get update
sudo apt-get install slapd ldap-utils
sudo systemctl status slapd
sudo dpkg-reconfigure slapd
"Omit openLDAP conf": no
DNS domain name: "example.com"
Organization name: "Example"
Admin password same as before (Important!!!!)
Database backend: "MDB"
Do you want to remove the Database during purge? "No"
Move old DataBase? Yes
Allow LDAPv2 protocol? No
sudo ufw allow ldap
ldapwhoami -H ldap:// -x
sudo nano /etc/ldap/ldap.conf
Specify the base dn and URI of the openLDAP server that we configured
BASE dc=example,dc=com
URI ldap://localhost
ldapsearch -x

sudo apt install phpldapadmin
sudo nano /etc/phpldapadmin/config.php
# $config->custom->appearance['timezone'] = 'Asia/Kolkata';

Set the server name, Provide your ip address and set the hide template warning
to true.
below $servers->newServer('ldap_pla');

$servers->setValue('server','name','TestLdap LDAP Server');
$servers->setValue('server','host','192.168.173.11');
$config->custom->appearance['hide_template_warning'] = true;

By default, anonymous login is enabled. To disable it, you need to remove the
comment character (the two slashes) and change true to false. Save and close
the file.
$servers->setValue('login','anon_bind',false);

add or change:
	$servers->setValue('server','base',array('dc=example,dc=com'));
Login to your phpldapadmin UI.
your-ip-address/phpldapadmin
Ex 192.168.173.11/phpldapadmin
cn=admin,dc=example,dc=com

"""
        )



def NIS():
    print(
"""
NIS



sudo apt-get -y install nis
NIS domain: "cs.example.com"
sudo nano /etc/default/nis
change:
	NISSERVER=master
sudo nano /etc/ypserv.securenets
This line gives access to everybody. PLEASE ADJUST!
# comment out
# 0.0.0.0 0.0.0.0
# add to the end: IP range you allow to access
255.255.255.0 10.0.0.0
sudo nano /var/yp/Makefile
change:
	MERGE_PASSWD=true
	MERGE_GROUP=true

sudo nano /etc/hosts
add:
	127.0.0.1	cs
	192.168.173.132	cs.example.com cs

sudo systemctl restart nis
sudo /usr/lib/yp/ypinit -m
# Ctrl+D key – if don’t want to add


Client_NIS
Configure NIS Client
[1] Install nis packages.

sudo apt-get -y install nis
NIS domain: "cs.example.com"
sudo nano /etc/yp.conf
add:
	domain example.com server cs.example.com
sudo nano /etc/nsswitch.conf
passwd: compat nis # line 7; add
group: compat nis # add
shadow: compat nis # add
hosts: files dns nis # add
# set follows if needed (create home directory automatically if none)
root@www:~# vi /etc/pam.d/common-session
# add to the end
session optional pam_mkhomedir.so skel=/etc/skel umask=077

sudo systemctl restart rpcbind nis
To test that the client can connect to the Centrify Network Information Service,
run one or more NIS client request commands; for example:
ypwhich
ypwhich -m
ypcat -k mapname

"""
        )


def MySQLPHP():
    print(
"""
MySQLPHP:
Practical No. 9

Aim: Install MySQL to configure database server, Install phpMyAdmin to
operate MySQL on web browser from Clients.


sudo apt install apache2
goto computer in file manager
	var/www/html and create index.html
open localhost in browser
sudo service apache2 start

sudo chmod -R 777 /var/www/html
create test.html in var/www/html
write test in the file and goto localhost/test.html

sudo apt-get install php
create test.php in var/www/html and add:
	<?php
	phpinfo();
	?>
localhost/test.php
sudo apt install libapache2-mod-php
sudo apt-get install mysql-server mysql-client
root password:123456
mysql -u root -p
sql> show databases;
sudo apt-get install phpmyadmin
web server to reconfigure:"apache2"
Press space button, then tab and then press enter

configure database for phpmyadmin with dbconfig-common? : "NO"
sudo service apache2 restart
localhost/phpmyadmin/
username:root
password:123456
"""
        )




def SAMBA():
    print(
"""
SAMBA
sudo apt update -y
sudo apt-get install samba -y
sudo mkdir /share
sudo chmod 777 /share
sudo nano /etc/samba/smb.conf
	Press Ctrl+end to get to the end of file.
	Then we’ll write the shared definition
	[my-samba-share] - share name
	path = /share – directory which you want to share
	public = no – this samba server is not public which means to access this file its
	requires authentication
	valid users – tom jerry – users who can connect
	read list = tom – user tom will have read access to this directory
	write list = jerry – user jerry will have write access to this directory
	browseable = yes – in the client system all the users will be able to access
	network share
	comment = “My Samba File Server” - Any comment you can give


sudo testparm
sudo useradd tom -s /sbin/nologin
sudo useradd jerry -s /sbin/nologin
sudo smbpasswd -a tom
sudo smbpasswd -a jerry

sudo systemctl start smbd
sudo systemctl start nmbd
sudo systemctl enable smbd nmbd


Client Samba Side(Ubuntu):
1. open terminal and ping the server ip. If you are able to ping the server that
means you are in network with the server
Then open File Manager -> Other Locations -> connect to server ->
smb://192.168.173.132
add register user and login


Samba Windows Client Side:
1. Press window + R then enter cmd. And then ping the server to check
whether we are in the network or not.
in run enter:
	\\192.168.173.132

"""
        )


def Client_Samba_SideUbuntu():
    print(
"""
Client Samba Side(Ubuntu):
1. open terminal and ping the server ip. If you are able to ping the server that
means you are in network with the server
Then open File Manager -> Other Locations -> connect to server ->
smb://192.168.173.132
add register user and login
"""
        )



def Samba_Windows_Client_Side():
    print(
"""
Samba Windows Client Side:
1. Press window + R then enter cmd. And then ping the server to check
whether we are in the network or not.
in run enter:
	\\192.168.173.132
"""
        )



def HelpMe():
    print(
"""
BFS
BFS2
IDFS
IDFS2
A_Star
A_Star2
Best_First_Search
Best_First_Search2
Blue_ScreenGP
ImageWindowGP
TraingleDrawGP
PyGameShapes
PyGameImageWindow
PyGameKeyDown
PyGameRect
PyGameTextFont
PyGameWindow
PYGAME
Caesar_Cipher
RSA
MD5
SHA
SHA2
DiffieHellman
Railfence
Railfence2
ClientServerINSClient1
ClientServerINSServer1
INSClient1
INSServer1
PyGameHello
SnakeGame
Infinite_Scroll
Decision_Tree1
Feed_Forward_Backpropogation1
SVM1
AdaBoost1
Naive_Bayes1
KNN1
Apriori1
Apriori2
Apriori3
TensorFlow1
Decision_tree2
FeedForwardBackpropgation2
SVM2
AdaBoost2
Naive_Bayes2
KNN2
Apriori2
ShootPy
ScreenShake
CameraShake
AIChase
PlayerMovement
SnowFall


DHCP
DHCP Client
Various_misc_fucn
NTP_Server
NTP_Client
SSHSecure_Shell
SSH_ClientWindows
SSHClientUbuntu
DNS
NFS
NFS_Client
LDAP
NIS
Client_NIS
MySQLPHP
SAMBA
Client_Samba_SideUbuntu
Samba_Windows_Client_Side
"""
        )



def HelpAI():
    print(
"""
BFS
BFS2
IDFS
IDFS2
A_Star
A_Star2
Best_First_Search
Best_First_Search2
Decision_Tree1
Feed_Forward_Backpropogation1
SVM1
AdaBoost1
Naive_Bayes1
KNN1
Apriori1
Apriori2
Apriori3
TensorFlow1
Decision_tree2
FeedForwardBackpropgation2
SVM2
AdaBoost2
Naive_Bayes2
KNN2
Apriori2
"""
        )

def HelpGP():
    print(
"""
Blue_ScreenGP
ImageWindowGP
TraingleDrawGP
PyGameShapes
PyGameImageWindow
PyGameKeyDown
PyGameRect
PyGameTextFont
PyGameWindow
PYGAME
INSServer1
PyGameHello
SnakeGame
Infinite_Scroll
ShootPy
ScreenShake
CameraShake
AIChase
PlayerMovement
SnowFall
"""
        )


def HelpINS():
    print(
"""
Caesar_Cipher
RSA
MD5
SHA
SHA2
DiffieHellman
Railfence
Railfence2
ClientServerINSClient1
ClientServerINSServer1
INSClient1
INSServer1
"""
        )

def HelpLSA():
    print(
"""
DHCP
DHCP Client
Various_misc_fucn
NTP_Server
NTP_Client
SSHSecure_Shell
SSH_ClientWindows
SSHClientUbuntu
DNS
NFS
NFS_Client
LDAP
NIS
Client_NIS
MySQLPHP
SAMBA
Client_Samba_SideUbuntu
Samba_Windows_Client_Side
"""
        )

def test1():
    print("Hello from bency!")
