<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="/media/logo.png" alt="Project logo"></a>
</p>

<h3 align="center">Simultaneous Multi-Way Linked-list</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

[!Custom License](/LICENSE)

</div>

---

<p align="center"> A multi-way linked-list approach with multi-threaded search algorithms
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage ](#-usage-)
- [✍️ Authors ](#️-authors-)

## 🧐 About <a name = "about"></a>

Simultaneous Multi-Way Linked-List is a data structure designed for efficient storage and retrieval of multiple sequences of data. It is an extension of the classic linked-list data structure, which allows nodes to be linked together in a linear fashion. In contrast, the Simultaneous Multi-Way Linked-List allows nodes to be linked together in multiple directions, enabling the creation of multiple sequences of data that can be searched, accessed and modified simultaneously.

The Simultaneous Multi-Way Linked-List data structure is ideal for applications that require the management of multiple sequences of data, such as in database management, file systems, and scheduling systems. But there are a few topics that inspired the project. Actually, the project was initially developed for logistics mapping and finding optimal routes ([MeanMachineProject](https://gitlab.com/msaidbilgehan/MeanMachineProject)), and the algorithm found in this step was documented in an article ([Connection World in Robot Mind](https://www.researchgate.net/publication/353793701_Connection_World_in_Robot_Mind)). Then, it was restructured, taking inspiration from neural networks because of its resemblance to neural connections. There are many areas that need to be further developed, but it is clear that it is more successful than the linked-list approaches found in the literature. With its ability to support multiple sequences of data, the Simultaneous Multi-Way Linked-List allows for efficient storage and retrieval of data, reducing the time and resources required for complex operations.

One of the key benefits of the Simultaneous Multi-Way Linked-List data structure is its ability to handle concurrent access by multiple processes. It provides an efficient mechanism for synchronization of multiple concurrent accesses, ensuring consistency and data integrity.

The Simultaneous Multi-Way Linked-List data structure is implemented using a combination of linked lists and trees. Nodes are organized into a hierarchical structure, with each node containing a pointer to its parent and one or more pointers to its children. This structure allows for efficient traversal and manipulation of the data, while maintaining the integrity of the multiple sequences of data.

In summary, the Simultaneous Multi-Way Linked-List is a powerful data structure that provides efficient storage and retrieval of multiple sequences of data, while allowing for concurrent access by multiple processes. Its hierarchical structure and efficient synchronization mechanism make it an ideal choice for complex applications that require the management of large amounts of data.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

```
python
```

### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
install python
create virtual environment
activate virtual environment
install requirements.txt (not necessary)
```

And run

```
python example.py
```

## 🎈 Usage <a name="usage"></a>

Add notes about how to use the system.

"Container" class contains useful features as creating nodes, connecting nodes, two different search algorithms, and so on...

"Node" class is a node for storing data or running some task simultaneously wih other nodes. 

"Gate" class contains input gate node and output gate node for creating an input and output connections to other nodes

"Search_History" class contains a struct that prevents race condition between threads at any search operation.

"Neuron" is a node type which is still at development. Please do not use it.
## ✍️ Authors <a name = "authors"></a>

- [@msaidbilgehan](https://github.com/msaidbilgehan) - Idea & Initial work
