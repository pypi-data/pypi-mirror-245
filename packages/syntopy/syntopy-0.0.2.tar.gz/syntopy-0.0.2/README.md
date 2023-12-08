# syntopy


# An Advanced Spatial Modelling and Analysis Software Library for Architecture, Engineering, and Construction

## Introduction
Welcome to syntopy (rhymes with symphony). Syntopy embodies the concept of elements harmoniously coexisting within a shared space. Just as different components seamlessly come together, Syntopy, with its roots in "syn" for synchronous, "top" for topology, and "py" for the Python programming language, unites these aspects to create a powerful tool for understanding architectural structures.

Imagine Syntopy as a digital architect that unveils the intricate tapestry of a building's layout. It takes raw architectural data and crafts a 3D model that represents how diverse elements interconnect within the same environment. This model delves beyond surface aesthetics, spotlighting how rooms, corridors, and structural features converge and interact synchronously.

Whether you're an architect analyzing spatial relationships or a curious individual intrigued by building design, Syntopy bridges the gap between complexity and comprehension. It serves as a virtual guide, untangling the intricate web of a building's inner workings, all within the familiar context of the Python programming language. Through Syntopy, the multifaceted language of architecture becomes accessible to all.

Syntopy's graph-based representation makes it a natural fit for integrating with Graph Machine Learning (GML), an exciting new branch of artificial intelligence. With GML, you can process vast amounts of connected data and extract valuable insights quickly and accurately. Syntopy's intelligent algorithms for graph and node classification take GML to the next level by using the extracted data to classify building typologies, predict associations, and complete missing information in building information models. This integration empowers you to leverage the historical knowledge embedded in your databases and make informed decisions about your current design projects. With Syntopy and GML, you can streamline your workflow, enhance your productivity, and achieve your project goals with greater efficiency and precision. With the integration of geometry, topology, information, and artificial intelligence, Syntopy enriches Building Information Models with Building *Intelligence* Models.

Syntopy's versatility extends to entities with mixed dimensionalities, enabling structural models, for example, to be represented coherently. Lines can represent columns and beams, surfaces can represent walls and slabs, and volumes can represent solids. Even non-building entities like structural loads can be efficiently attached to the structure. This approach creates mixed-dimensional models that are highly compatible with structural analysis simulation software.

Experience Syntopy's comprehensive and well-documented Application Protocol Interface (API) and enjoy the freedom and flexibility that it offers in your architectural design process. Syntopy uses cutting-edge C++-based non-manifold topology (NMT) core technology ([Open CASCADE](https://www.opencascade.com/)), and python bindings. Interacting with Syntopy is easily accomplished through a command-Line interface and scripts, visual data flow programming (VDFP) plugins for popular BIM software, and cloud-based interfaces through [Streamlit](https://streamlit.io/) and [Viktor](https://viktor.ai). You can easily interact with Syntopy in various ways to perform design and analysis tasks or even seamlessly customize and embed it in your own in-house software and workflows. Plus, Syntopy includes several industry-standard methods for data transport including IFC, OBJ, BREP, HBJSON, CSV, as well serializing through cloud-based services such as [Speckle](https://speckle.systems/).

Syntopy’s open-source philosophy and licensing ([AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)) enables you to achieve your design vision with minimal incremental costs, ensuring a high return on investment. You control and own your information outright, and nothing is ever trapped in an expensive subscription model. Syntopy empowers you to build and share data apps with ease, giving you the flexibility to choose between local or cloud-based options and the peace of mind to focus on what matters most. 

Join the revolution in architectural design with Syntopy. Try it today and see the difference for yourself.

## Installation
syntopy can be installed using the **pip** command as such:

`pip install syntopy --upgrade`

## Prerequisites

syntopy depends on the following python libraries which will be installed automatically from pip:

<details>
<summary>
<b>Expand to view dependencies</b>
</summary>
* [numpy](http://numpy.org) >= 1.24.0
* [scipy](http://scipy.org) >= 1.10.0
* [plotly](http://plotly.com/) >= 5.11.0
* [ifcopenshell](http://ifcopenshell.org/) >=0.7.9
* [ipfshttpclient](https://pypi.org/project/ipfshttpclient/) >= 0.7.0
* [web3](https://web3py.readthedocs.io/en/stable/) >=5.30.0
* [openstudio](https://openstudio.net/) >= 3.4.0
* [lbt-ladybug](https://pypi.org/project/lbt-ladybug/) >= 0.25.161
* [lbt-honeybee](https://pypi.org/project/lbt-honeybee/) >= 0.6.12
* [honeybee-energy](https://pypi.org/project/honeybee-energy/) >= 1.91.49
* [json](https://docs.python.org/3/library/json.html) >= 2.0.9
* [py2neo](https://py2neo.org/) >= 2021.2.3
* [pyvisgraph](https://github.com/TaipanRex/pyvisgraph) >= 0.2.1
* [specklepy](https://github.com/specklesystems/specklepy) >= 2.7.6
* [pandas](https://pandas.pydata.org/) >= 1.4.2
* [scipy](https://scipy.org/) >= 1.8.1
* [dgl](https://github.com/dmlc/dgl) >= 0.8.2

</details>

## How to start using Syntopy
1. Open your favourite python editor ([jupyter notebook](https://jupyter.org/) is highly recommended)
1. Type 'import syntopy'
1. Start using the API

## API Documentation
API documentation can be found at [https://topologic.app/syntopy_doc/](https://topologic.app/syntopy_doc/)

syntopy: &copy; 2023 Wassim Jabi
