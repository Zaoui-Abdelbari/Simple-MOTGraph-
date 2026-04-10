# 🧠 Motif — MOT Knowledge Model Visual Editor

> A visual editor for building and exploring MOT (Modélisation par Objets Typés) knowledge models.

---

## ✨ Features

- **6 Knowledge Node Types** — Concept, Procédure, Principe, Exemple, Trace, Énoncé, each with distinct shapes and colors
- **7 Relation Types** — Spécialisation, Instanciation, Intrant/Produit, Précédence, Régulation, Composition, Application
- **Grammar Validation** — Enforces MOT grammar rules in real-time; invalid relations are rejected with helpful feedback
- **Interactive Canvas** — Drag-and-drop nodes, zoom in/out, scroll, and fit-to-view
- **Node Editor** — Click any node to edit its label and stereotype inline
- **Save & Load** — Export/import models as JSON for persistence
- **Text Export** — Export a plain-text summary of your model
- **Grammar Reference** — Built-in window displaying the full MOT relation grammar table

---

## 🖥️ Screenshot

> *(Add a screenshot of the application here)*

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Tkinter (included with standard Python on most platforms)

### Installation

```bash
git clone https://github.com/your-username/motif-mot-editor.git
cd motif-mot-editor
python mot.py
```

No external dependencies required — runs on the Python standard library only.

---

## 🧩 How to Use

### 1. Add Nodes
- Select **Node mode** (default)
- Choose a knowledge type from the sidebar (e.g. *Concept*, *Procédure*)
- Click anywhere on the canvas to place a node
- Click a node to select it and edit its label or stereotype

### 2. Add Relations
- Switch to **Relation mode**
- Choose a relation type (e.g. *C - Composition*)
- Click a source node, then a destination node
- The grammar validator will accept or reject the relation automatically

### 3. Save & Load
- **Save (JSON)** — Saves the full model to a `.json` file
- **Load (JSON)** — Restores a previously saved model
- **Export (Text)** — Saves a human-readable `.txt` summary

### 4. Navigate the Canvas
| Action | How |
|---|---|
| Scroll | Mouse wheel |
| Zoom | `Ctrl + Mouse wheel` or `+` / `−` buttons |
| Fit to view | Click **📐 Tout Voir** |
| Reset zoom | Click **🔄 Réinitialiser** |
| Move a node | Drag it in Node mode |

---

## 📐 MOT Knowledge Types

| Type | Shape | Color | Represents |
|---|---|---|---|
| **Concept** | Rectangle | 🔵 Blue | The *what* — essence of a concrete object |
| **Procédure** | Ellipse | 🟢 Green | The *how* — operations and actions |
| **Principe** | Hexagon | 🟡 Amber | The *why / when / who* — strategic relations |
| **Exemple** | Rectangle | 🟣 Purple | A concrete instance of a concept |
| **Trace** | Ellipse | 🩷 Pink | Facts obtained during procedure execution |
| **Énoncé** | Hexagon | 🔴 Red | Instantiation of a principle on concrete objects |

---

## 🔗 MOT Relation Types

| Code | Name | Description |
|---|---|---|
| `S` | Spécialisation | Taxonomic (is-a) relationship |
| `I` | Instanciation | Links abstract knowledge to a fact |
| `I/P` | Intrant/Produit | Input or output of a procedure |
| `P` | Précédence | Temporal sequence |
| `R` | Régulation | Constraint or rule |
| `C` | Composition | Components of a knowledge unit |
| `A` | Application | Link between a fact and an abstraction |

---

## 💾 File Format

Models are saved as JSON:

```json
{
  "nodes": [
    { "id": 1, "type": "Concept", "label": "Concept 1", "x": 300, "y": 200, "stereotype": "" }
  ],
  "relations": [
    { "id": 12345, "from": 1, "to": 2, "type": "C" }
  ],
  "metadata": {
    "node_counter": 2,
    "version": "2.0"
  }
}
```

---

## 🛠️ Project Structure

```
motif-mot-editor/
├── mot.py          # Main application (single-file)
└── README.md
```

---

## 📚 Background

MOT (Modélisation par Objets Typés) is a knowledge modeling language developed at **LICEF Research Center (Télé-université, Montréal)**. It provides a structured way to represent and relate different types of knowledge objects, commonly used in instructional design and educational technology.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.