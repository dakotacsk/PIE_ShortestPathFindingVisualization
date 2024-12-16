# **Project Overview**

## Table of Contents

1. [Budget and Components](#budget-and-components)
2. [Media](#media)
3. [Mechanical Design](#mechanical-design)
4. [Electrical and Firmware Design](#electrical-and-firmware-design)
5. [Software Design](#software-design)
6. [Energy Flow & System Diagrams](#diagrams)

---

## **Budget and Components**

### Spending Breakdown

Provide a table listing all components, their costs, and sources.

**PLACEHOLDER**: Fill in actual component data in the table below.

| **Component/Material** | **Cost (USD)**        | **Source**          |
| ---------------------- | --------------------- | ------------------- |
| Example Component 1    | $XX                   | Example Source      |
| Example Component 2    | Free (Estimated: $XX) | Donated or Provided |
| Example Component 3    | $XX                   | Purchased/Online    |

**Total Estimated Cost**: **PLACEHOLDER**: Add total value.

---

## **Media**

### Final System in Action

Add images and videos of the final project setup.

**PLACEHOLDER**: Replace this with images and videos of your system in action.

**Example**:
![Final System](assets/img/game-homepage.png)  
_Figure: Completed arcade machine showcasing the game._

### Demo Video

Link to a video demo of the project.

**PLACEHOLDER**: Add demo video link here.

**Example**:  
[Watch the Demo Video](https://your-demo-link.com)

---

## **Final Designs**

### **Mechanical Design**

Provide a detailed description of the mechanical design, including materials, construction methods, and analysis.

**PLACEHOLDER**: Add description of mechanical components.

- **Include details on the design process, materials used, and fabrication methods.**
- **Describe any stress testing, simulations, or structural analysis performed.**
- Replace this placeholder with relevant CAD images, renderings, or diagrams if available.

**Example**:  
![CAD Rendering](PLACEHOLDER)  
_Figure: CAD rendering showing the structure and layout of the arcade machine._

**Design Highlights**:

- **Materials**: Specify materials used (e.g., MDF, 3D-printed PLA, aluminum) and their purpose.
- **Fabrication Methods**: Describe how parts were cut, assembled, and finished (e.g., laser cutting, 3D printing, spray painting).
- **Modularity**: Explain how the design allows for future upgrades or ease of assembly.

**Analysis**:

- **Structural Analysis**: Summarize results from stress tests or simulations to verify durability.
- **User Interaction**: Describe ergonomic considerations, such as button placement, screen height, and accessibility.

---

### Electrical and Firmware Design

Provide a description of the electrical system, including connections, power requirements, and analysis.

**PLACEHOLDER**: Add description of electrical components.

- **Include details on power supply, wiring, and voltage/current analysis.**
- Replace this placeholder with actual circuit diagrams and notes.

**Example**:  
![Electronics Schematic](PLACEHOLDER)  
_Figure: Circuit schematic showing connections between components._

---

### Software Design

The software for **Hatchling's Quest: Pathfinding Trials** is designed to deliver an intuitive, engaging, and educational gaming experience while visualizing pathfinding algorithms in action.

#### **Software Architecture**

### Software Structure and Key Modules

#### Overview:

The software is divided into three main areas:

- **Game Interface**: Handles the GUI, animations, and user input using **Pygame**.
- **Pathfinding Algorithms**:
  - **Dijkstra's Algorithm** (Level 1): Computes shortest paths.
  - **Q-Learning** (Level 2): Enables reward-based navigation.
- **Game Logic**: Manages screens, game states, and leaderboards.

#### Key Modules:

- **`run_game.py`**: Coordinates game flow.
- **`grid/grid.py`**: Defines the pathfinding grid.
- **Pathfinding Modules**:
  - **`sprites/DijkstraSprite.py`**: Implements Dijkstra’s Algorithm.
  - **`sprites/QLearningSprite.py`**: Implements Q-Learning.
- **Screens**: Main menu, instructions, and interactive gameplay feedback.
- **Leaderboard**: Tracks and displays high scores via **`leaderboard/leaderboard.py`**.

#### **Dependencies**

The software relies on the following external libraries:

- **Python 3.11.7**: Core language used for development.
- **NumPy (2.2.0)**: Used for matrix operations in Q-Learning, including Q-table computations.
- **Pygame (2.6.1)**: Provides the framework for rendering the game interface and managing user input.

---

#### **Flow Diagram for Game**

The following flow diagram illustrates the architecture and flow of the game, showing transitions between levels, screens, and algorithms:

![Flow Diagram](../assets/img/pathfinders_flow.png)  
_Figure: Flow diagram representing game architecture and flow._

---

#### **UML Diagram**

The UML diagram below showcases the architecture and relationships within the game. It highlights key components, such as the flow between screens, sprite classes, and grid interactions, as well as how algorithms like Dijkstra's and Q-Learning are integrated:

![UML Diagram](../assets/img/uml.png)  
_Figure: UML diagram representing the game architecture and component relationships._

---

#### **Link to Source Code**

The complete source code for the project is hosted on GitHub:  
[GitHub Repo Link](https://github.com/dakotacsk/pie_shortestpathfindingvisualization)

---

## **Diagrams**

### Data and Energy Flow Diagram

Insert a high-level diagram showing how energy and data move through the system.

**PLACEHOLDER**: Add data and energy flow diagram.

**Example**:  
![Energy Flow Diagram](../assets/img/energy_flow.png)  
_Figure: Data and energy flow in the arcade system._

---

### Subsystem Diagrams

Include additional diagrams that illustrate subsystem connections or component relationships.

**PLACEHOLDER**: Add subsystem diagrams (e.g., mechanical, electrical, or software).

**Example**:  
![Subsystem Diagram](PLACEHOLDER)  
_Figure: Subsystem relationships across hardware, software, and firmware._

---

## **Conclusion**

**PLACEHOLDER**: Add a brief conclusion summarizing the project's success, challenges overcome, and key learnings.
