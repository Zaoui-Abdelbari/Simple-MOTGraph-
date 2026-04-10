import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import math


# MOT Grammar Rules based on Tableau 3
MOT_GRAMMAR = {
    'Concept': {
        'Concept': ['C', 'S'],
        'Procédure': ['I/P'],
        'Principe': ['R'],
        'Exemple': ['I', 'C'],
        'Trace': [],
        'Énoncé': []
    },
    'Procédure': {
        'Concept': ['I/P'],
        'Procédure': ['C', 'S', 'P'],
        'Principe': ['C', 'P'],
        'Exemple': ['I', 'C'],
        'Trace': [],
        'Énoncé': []
    },
    'Principe': {
        'Concept': ['R'],
        'Procédure': ['C', 'R', 'P'],
        'Principe': ['C', 'S', 'P', 'R'],
        'Exemple': ['I', 'C'],
        'Trace': [],
        'Énoncé': []
    },
    'Exemple': {
        'Concept': ['A'],
        'Procédure': ['A'],
        'Principe': ['A'],
        'Exemple': ['A', 'C'],
        'Trace': ['A', 'I/P'],
        'Énoncé': ['A']
    },
    'Trace': {
        'Concept': ['A'],
        'Procédure': ['A'],
        'Principe': ['A'],
        'Exemple': ['A', 'I/P'],
        'Trace': ['A', 'C', 'P'],
        'Énoncé': ['A', 'C', 'P']
    },
    'Énoncé': {
        'Concept': ['A'],
        'Procédure': ['A'],
        'Principe': ['A'],
        'Exemple': ['A', 'R'],
        'Trace': ['A', 'C', 'R', 'P'],
        'Énoncé': ['A', 'C', 'R', 'P']
    }
}

# Knowledge type definitions
KNOWLEDGE_TYPES = {
    'Concept': {
        'color': '#3B82F6',
        'shape': 'rect',
        'abstract': True,
        'description': 'Représente le "quoi" des choses - l\'essence d\'un objet concret'
    },
    'Procédure': {
        'color': '#10B981',
        'shape': 'ellipse',
        'abstract': True,
        'description': 'Décrit le "comment" - opérations et actions à accomplir'
    },
    'Principe': {
        'color': '#F59E0B',
        'shape': 'hexagon',
        'abstract': True,
        'description': 'Désigne le "pourquoi", "quand" ou "qui" - relation stratégique'
    },
    'Exemple': {
        'color': '#8B5CF6',
        'shape': 'rect',
        'abstract': False,
        'description': 'Instance concrète d\'un concept'
    },
    'Trace': {
        'color': '#EC4899',
        'shape': 'ellipse',
        'abstract': False,
        'description': 'Faits concrets obtenus lors de l\'exécution d\'une procédure'
    },
    'Énoncé': {
        'color': '#EF4444',
        'shape': 'hexagon',
        'abstract': False,
        'description': 'Instanciation d\'un principe à propos d\'objets concrets'
    }
}

# Relation type definitions
RELATION_TYPES = {
    'S': {'label': 'Spécialisation', 'description': 'Relation de spécialisation (taxonomie)'},
    'I': {'label': 'Instanciation', 'description': 'Associe une connaissance abstraite à un fait'},
    'I/P': {'label': 'Intrant/Produit', 'description': 'Intrant ou produit d\'une procédure'},
    'P': {'label': 'Précédence', 'description': 'Séquence temporelle'},
    'R': {'label': 'Régulation', 'description': 'Contrainte ou règle'},
    'C': {'label': 'Composition', 'description': 'Composants d\'une connaissance'},
    'A': {'label': 'Application', 'description': 'Lien entre fait et abstraction'}
}


class Node:
    """Represents a MOT knowledge node"""
    def __init__(self, node_id, node_type, label, x, y, stereotype=''):
        self.id = node_id
        self.type = node_type
        self.label = label
        self.x = x
        self.y = y
        self.stereotype = stereotype
        self.canvas_id = None
        self.text_id = None
        self.stereotype_id = None
        self.delete_btn_id = None

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'label': self.label,
            'x': self.x,
            'y': self.y,
            'stereotype': self.stereotype
        }


class Relation:
    """Represents a MOT relation between nodes"""
    def __init__(self, from_node, to_node, rel_type, rel_id=None):
        self.id = rel_id if rel_id else id(self)
        self.from_node = from_node
        self.to_node = to_node
        self.type = rel_type
        self.line_id = None
        self.arrow_id = None
        self.label_bg_id = None
        self.label_text_id = None
        self.delete_btn_id = None

    def to_dict(self):
        return {
            'id': self.id,
            'from': self.from_node,
            'to': self.to_node,
            'type': self.type
        }


class GrammarValidator:
    """Validates MOT grammar rules"""
    @staticmethod
    def validate_relation(source_type, dest_type, rel_type):
        allowed_relations = MOT_GRAMMAR.get(source_type, {}).get(dest_type, [])
        return rel_type in allowed_relations

    @staticmethod
    def get_allowed_relations(source_type, dest_type):
        return MOT_GRAMMAR.get(source_type, {}).get(dest_type, [])


class GrammarInfoWindow:
    """Window to display grammar information"""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Grammaire des Relations MOT")
        self.window.geometry("900x600")
        self.window.transient(parent)
        
        # Make window responsive
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Title
        title = tk.Label(self.window, text="Grammaire des Relations MOT (Tableau 3)",
                        font=('Arial', 14, 'bold'), bg='#2563eb', fg='white', pady=10)
        title.grid(row=0, column=0, sticky='ew')
        
        # Frame with scrollbar
        frame = tk.Frame(self.window)
        frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Canvas for scrolling
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create grammar table
        self.create_grammar_table(scrollable_frame)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Close button
        close_btn = tk.Button(self.window, text="Fermer", command=self.window.destroy,
                             bg='#ef4444', fg='white', font=('Arial', 10, 'bold'), pady=8)
        close_btn.grid(row=2, column=0, pady=10)

    def create_grammar_table(self, parent):
        # Header
        header_frame = tk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(header_frame, text="Origine ↓ / Destination →", 
                font=('Arial', 10, 'bold'), width=20, borderwidth=1, 
                relief=tk.SOLID).grid(row=0, column=0, sticky='nsew')
        
        knowledge_types = list(KNOWLEDGE_TYPES.keys())
        
        # Column headers
        for col, ktype in enumerate(knowledge_types, 1):
            color = KNOWLEDGE_TYPES[ktype]['color']
            tk.Label(header_frame, text=ktype, font=('Arial', 9, 'bold'),
                    bg=color, fg='white', width=12, borderwidth=1,
                    relief=tk.SOLID).grid(row=0, column=col, sticky='nsew')
        
        # Table content
        for row, source in enumerate(knowledge_types, 1):
            # Row header
            color = KNOWLEDGE_TYPES[source]['color']
            tk.Label(header_frame, text=source, font=('Arial', 9, 'bold'),
                    bg=color, fg='white', width=20, borderwidth=1,
                    relief=tk.SOLID).grid(row=row, column=0, sticky='nsew')
            
            # Relations
            for col, dest in enumerate(knowledge_types, 1):
                relations = MOT_GRAMMAR.get(source, {}).get(dest, [])
                rel_text = ', '.join(relations) if relations else '—'
                
                bg_color = '#e0f2fe' if relations else '#fee2e2'
                tk.Label(header_frame, text=rel_text, font=('Arial', 9),
                        bg=bg_color, borderwidth=1, relief=tk.SOLID,
                        width=12).grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
        
        # Legend
        legend_frame = tk.LabelFrame(parent, text="Légende des Relations", 
                                     font=('Arial', 11, 'bold'), padx=10, pady=10)
        legend_frame.pack(fill=tk.X, pady=10)
        
        for rel_type, config in RELATION_TYPES.items():
            rel_frame = tk.Frame(legend_frame)
            rel_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(rel_frame, text=f"{rel_type}:", font=('Arial', 10, 'bold'),
                    width=5).pack(side=tk.LEFT)
            tk.Label(rel_frame, text=f"{config['label']} - {config['description']}",
                    font=('Arial', 9), justify=tk.LEFT).pack(side=tk.LEFT, padx=5)


class MOTEditorApp:
    """Main MOT Editor Application - Enhanced Version"""
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur MOT - Modélisation par Objets Typés (Version Améliorée)")
        
        # Make window responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1600, int(screen_width * 0.9))
        window_height = min(900, int(screen_height * 0.9))
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.state('zoomed')  # Maximize on Windows
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Data structures
        self.nodes = []
        self.relations = []
        self.node_counter = 0
        
        # UI state
        self.selected_tool = 'Concept'
        self.selected_relation_type = 'C'
        self.mode = 'node'
        self.selected_node = None
        self.dragging_node = None
        self.relation_start = None
        self.drag_data = {'x': 0, 'y': 0}
        self.hovered_relation = None
        self.zoom_level = 1.0
        
        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with grid
        main_container = tk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky='nsew')
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Canvas area
        self.setup_canvas(main_container)

    def setup_sidebar(self, parent):
        """Setup the sidebar with controls"""
        sidebar = tk.Frame(parent, width=340, bg='#f8f9fa', relief=tk.RAISED, borderwidth=1)
        sidebar.grid(row=0, column=0, sticky='ns')
        sidebar.grid_propagate(False)
        
        # Title
        title = tk.Label(sidebar, text="Éditeur MOT", font=('Arial', 18, 'bold'), 
                        bg='#f8f9fa', fg='#2563eb')
        title.pack(pady=15)
        
        # Mode selection
        mode_frame = tk.LabelFrame(sidebar, text="Mode", font=('Arial', 11, 'bold'),
                                   bg='#f8f9fa', padx=10, pady=10)
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_frame = tk.Frame(mode_frame, bg='#f8f9fa')
        btn_frame.pack(fill=tk.X)
        
        self.mode_node_btn = tk.Button(btn_frame, text="🔷 Nœuds", command=lambda: self.set_mode('node'),
                                       bg='#3b82f6', fg='white', font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, padx=15, pady=8, cursor='hand2')
        self.mode_node_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.mode_relation_btn = tk.Button(btn_frame, text="🔗 Relations", 
                                           command=lambda: self.set_mode('relation'),
                                           bg='#e5e7eb', fg='black', font=('Arial', 10),
                                           relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        self.mode_relation_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Scrollable frame for tools
        canvas_scroll = tk.Canvas(sidebar, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Knowledge types section
        self.knowledge_frame = tk.LabelFrame(scrollable_frame, text="Types de Connaissances",
                                            font=('Arial', 11, 'bold'), bg='#f8f9fa', padx=10, pady=10)
        self.knowledge_frame.pack(fill=tk.X, pady=5)
        self.setup_knowledge_buttons()
        
        # Relation types section
        self.relation_frame = tk.LabelFrame(scrollable_frame, text="Types de Relations",
                                           font=('Arial', 11, 'bold'), bg='#f8f9fa', padx=10, pady=10)
        self.relation_frame.pack(fill=tk.X, pady=5)
        self.setup_relation_buttons()
        
        # Grammar info button
        grammar_btn = tk.Button(scrollable_frame, text="📖 Voir la Grammaire MOT",
                               command=self.show_grammar_info,
                               bg='#8b5cf6', fg='white', font=('Arial', 10, 'bold'),
                               pady=8, cursor='hand2')
        grammar_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Info panel
        self.info_frame = tk.LabelFrame(scrollable_frame, text="Informations",
                                       font=('Arial', 11, 'bold'), bg='#f8f9fa', padx=10, pady=10)
        self.info_frame.pack(fill=tk.X, pady=5)
        self.info_label = tk.Label(self.info_frame, text="Aucun nœud sélectionné",
                                   bg='#f8f9fa', fg='#666', justify=tk.LEFT, wraplength=280)
        self.info_label.pack()
        
        # Edit controls
        self.edit_frame = tk.Frame(self.info_frame, bg='#f8f9fa')
        
        tk.Label(self.edit_frame, text="Étiquette:", bg='#f8f9fa', font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.label_entry = tk.Entry(self.edit_frame, font=('Arial', 10))
        self.label_entry.pack(fill=tk.X, pady=2)
        self.label_entry.bind('<KeyRelease>', self.update_node_label)
        
        tk.Label(self.edit_frame, text="Stéréotype:", bg='#f8f9fa', font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5, 0))
        self.stereotype_entry = tk.Entry(self.edit_frame, font=('Arial', 10))
        self.stereotype_entry.pack(fill=tk.X, pady=2)
        self.stereotype_entry.bind('<KeyRelease>', self.update_node_stereotype)
        
        self.delete_btn = tk.Button(self.edit_frame, text="🗑 Supprimer le Nœud", 
                                    command=self.delete_selected_node,
                                    bg='#ef4444', fg='white', font=('Arial', 10, 'bold'), 
                                    pady=5, cursor='hand2')
        self.delete_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Relations list
        self.relations_list_frame = tk.LabelFrame(scrollable_frame, text="Relations du Modèle",
                                                 font=('Arial', 11, 'bold'), bg='#f8f9fa', 
                                                 padx=10, pady=10)
        self.relations_list_frame.pack(fill=tk.X, pady=5)
        
        self.relations_listbox = tk.Listbox(self.relations_list_frame, height=6, font=('Arial', 9))
        self.relations_listbox.pack(fill=tk.X, pady=5)
        self.relations_listbox.bind('<<ListboxSelect>>', self.on_relation_select)
        
        self.delete_relation_btn = tk.Button(self.relations_list_frame, 
                                            text="🗑 Supprimer la Relation",
                                            command=self.delete_selected_relation,
                                            bg='#f59e0b', fg='white', font=('Arial', 9, 'bold'),
                                            pady=5, cursor='hand2', state=tk.DISABLED)
        self.delete_relation_btn.pack(fill=tk.X)
        
        # Export/Import buttons
        export_frame = tk.LabelFrame(scrollable_frame, text="Fichiers", font=('Arial', 11, 'bold'),
                                    bg='#f8f9fa', padx=10, pady=10)
        export_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(export_frame, text="💾 Sauvegarder (JSON)", command=self.export_json,
                 bg='#3b82f6', fg='white', font=('Arial', 10, 'bold'), 
                 pady=8, cursor='hand2').pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="📂 Charger (JSON)", command=self.load_json,
                 bg='#10b981', fg='white', font=('Arial', 10, 'bold'), 
                 pady=8, cursor='hand2').pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="📄 Exporter (Texte)", command=self.export_text,
                 bg='#8b5cf6', fg='white', font=('Arial', 10, 'bold'), 
                 pady=8, cursor='hand2').pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="🗑 Nouveau Modèle", command=self.clear_model,
                 bg='#ef4444', fg='white', font=('Arial', 10, 'bold'), 
                 pady=8, cursor='hand2').pack(fill=tk.X, pady=2)
        
        # Stats
        self.stats_frame = tk.LabelFrame(scrollable_frame, text="Statistiques",
                                        font=('Arial', 11, 'bold'), bg='#f8f9fa', padx=10, pady=10)
        self.stats_frame.pack(fill=tk.X, pady=5)
        self.stats_label = tk.Label(self.stats_frame, text="Nœuds: 0\nRelations: 0",
                                    bg='#f8f9fa', fg='#333', justify=tk.LEFT, font=('Arial', 10))
        self.stats_label.pack()
        
        self.update_mode_buttons()

    def setup_knowledge_buttons(self):
        """Create buttons for knowledge types"""
        for ktype, config in KNOWLEDGE_TYPES.items():
            btn = tk.Button(self.knowledge_frame, text=f"  {ktype}", 
                          command=lambda t=ktype: self.select_knowledge_type(t),
                          bg=config['color'], fg='white', font=('Arial', 10, 'bold'),
                          relief=tk.RAISED, anchor=tk.W, padx=10, pady=8, cursor='hand2')
            btn.pack(fill=tk.X, pady=2)
            self.create_tooltip(btn, config['description'])

    def setup_relation_buttons(self):
        """Create buttons for relation types"""
        for rel_type, config in RELATION_TYPES.items():
            btn = tk.Button(self.relation_frame, 
                          text=f"{rel_type} - {config['label']}", 
                          command=lambda t=rel_type: self.select_relation_type(t),
                          bg='#e5e7eb', fg='#333', font=('Arial', 9),
                          relief=tk.FLAT, anchor=tk.W, padx=10, pady=6, cursor='hand2')
            btn.pack(fill=tk.X, pady=2)
            self.create_tooltip(btn, config['description'])

    def setup_canvas(self, parent):
        """Setup the drawing canvas with scrollbars"""
        canvas_container = tk.Frame(parent, bg='white')
        canvas_container.grid(row=0, column=1, sticky='nsew')
        canvas_container.grid_rowconfigure(1, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Top toolbar with zoom controls
        toolbar = tk.Frame(canvas_container, bg='#e5e7eb', height=50)
        toolbar.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        # Zoom controls
        zoom_frame = tk.Frame(toolbar, bg='#e5e7eb')
        zoom_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(zoom_frame, text="🔍 Zoom:", bg='#e5e7eb', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(zoom_frame, text="−", command=self.zoom_out,
                 bg='#3b82f6', fg='white', font=('Arial', 12, 'bold'),
                 width=3, cursor='hand2').pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = tk.Label(zoom_frame, text="100%", bg='white',
                                   font=('Arial', 10, 'bold'), width=6,
                                   relief=tk.SUNKEN, padx=5)
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        tk.Button(zoom_frame, text="+", command=self.zoom_in,
                 bg='#3b82f6', fg='white', font=('Arial', 12, 'bold'),
                 width=3, cursor='hand2').pack(side=tk.LEFT, padx=2)
        
        tk.Button(zoom_frame, text="🔄 Réinitialiser", command=self.reset_zoom,
                 bg='#10b981', fg='white', font=('Arial', 9, 'bold'),
                 padx=10, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(zoom_frame, text="📐 Tout Voir", command=self.fit_to_view,
                 bg='#8b5cf6', fg='white', font=('Arial', 9, 'bold'),
                 padx=10, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Message label
        self.message_label = tk.Label(toolbar, text="", font=('Arial', 10, 'bold'),
                                     bg='#10b981', fg='white', padx=15, pady=5)
        self.message_label.pack(side=tk.RIGHT, padx=10)
        self.message_label.pack_forget()
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(canvas_container, bg='#f3f4f6', cursor='cross',
                               scrollregion=(0, 0, 3000, 3000))
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, 
                                   command=self.canvas.xview)
        h_scrollbar.grid(row=2, column=0, sticky='ew')
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL,
                                   command=self.canvas.yview)
        v_scrollbar.grid(row=1, column=1, sticky='ns')
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, 
                            yscrollcommand=v_scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.canvas.bind('<Motion>', self.on_canvas_motion)
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Control-MouseWheel>', self.on_ctrl_mousewheel)

    def on_mousewheel(self, event):
        """Handle mouse wheel for scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_ctrl_mousewheel(self, event):
        """Handle Ctrl+MouseWheel for zooming"""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        """Zoom in the canvas"""
        if self.zoom_level < 3.0:
            self.zoom_level *= 1.2
            self.apply_zoom()
            self.show_message(f"Zoom: {int(self.zoom_level * 100)}%", 'info')

    def zoom_out(self):
        """Zoom out the canvas"""
        if self.zoom_level > 0.3:
            self.zoom_level /= 1.2
            self.apply_zoom()
            self.show_message(f"Zoom: {int(self.zoom_level * 100)}%", 'info')

    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.zoom_level = 1.0
        self.apply_zoom()
        self.show_message("Zoom réinitialisé à 100%", 'success')

    def apply_zoom(self):
        """Apply the current zoom level"""
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        self.redraw_canvas()

    def fit_to_view(self):
        """Fit all nodes to view"""
        if not self.nodes:
            self.show_message("Aucun nœud à afficher", 'info')
            return
        
        # Find bounding box of all nodes
        min_x = min(node.x for node in self.nodes) - 100
        max_x = max(node.x for node in self.nodes) + 100
        min_y = min(node.y for node in self.nodes) - 100
        max_y = max(node.y for node in self.nodes) + 100
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate required zoom
        model_width = max_x - min_x
        model_height = max_y - min_y
        
        if model_width > 0 and model_height > 0:
            zoom_x = canvas_width / model_width
            zoom_y = canvas_height / model_height
            self.zoom_level = min(zoom_x, zoom_y, 2.0) * 0.9  # 90% to add margin
            
            # Center the view
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            self.apply_zoom()
            
            # Scroll to center
            self.canvas.xview_moveto((center_x - canvas_width/2/self.zoom_level) / 3000)
            self.canvas.yview_moveto((center_y - canvas_height/2/self.zoom_level) / 3000)
            
            self.show_message("Vue ajustée au modèle", 'success')

    def on_canvas_motion(self, event):
        """Handle mouse motion for hover effects"""
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # Check if hovering over a relation delete button
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item in items:
            for relation in self.relations:
                if relation.delete_btn_id == item:
                    self.canvas.config(cursor='hand2')
                    return
        
        # Check if hovering over a node
        for node in self.nodes:
            distance = math.sqrt((node.x - x)**2 + (node.y - y)**2)
            if distance < 60:
                self.canvas.config(cursor='hand2' if self.mode == 'relation' else 'fleur')
                return
        
        self.canvas.config(cursor='cross' if self.mode == 'node' else 'hand2')

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief=tk.SOLID,
                           borderwidth=1, font=('Arial', 9), wraplength=300, justify=tk.LEFT, padx=5, pady=5)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def set_mode(self, mode):
        """Set the current mode"""
        self.mode = mode
        self.relation_start = None
        self.selected_node = None
        self.update_mode_buttons()
        self.update_info_panel()
        self.canvas.config(cursor='cross' if mode == 'node' else 'hand2')

    def update_mode_buttons(self):
        """Update mode button styles"""
        if self.mode == 'node':
            self.mode_node_btn.config(bg='#3b82f6', fg='white', relief=tk.RAISED, 
                                     font=('Arial', 10, 'bold'))
            self.mode_relation_btn.config(bg='#e5e7eb', fg='black', relief=tk.FLAT, 
                                         font=('Arial', 10))
            self.knowledge_frame.pack(fill=tk.X, pady=5)
            self.relation_frame.pack_forget()
        else:
            self.mode_node_btn.config(bg='#e5e7eb', fg='black', relief=tk.FLAT, 
                                     font=('Arial', 10))
            self.mode_relation_btn.config(bg='#10b981', fg='white', relief=tk.RAISED, 
                                         font=('Arial', 10, 'bold'))
            self.knowledge_frame.pack_forget()
            self.relation_frame.pack(fill=tk.X, pady=5)

    def select_knowledge_type(self, ktype):
        """Select a knowledge type"""
        self.selected_tool = ktype
        self.show_message(f"{ktype} sélectionné", 'success')

    def select_relation_type(self, rel_type):
        """Select a relation type"""
        self.selected_relation_type = rel_type
        self.show_message(f"Relation {rel_type} sélectionnée", 'success')

    def on_canvas_click(self, event):
        """Handle canvas click"""
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # Check for delete button click
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item in items:
            for relation in self.relations:
                if relation.delete_btn_id == item:
                    self.delete_relation(relation)
                    return
        
        clicked_node = self.get_node_at_position(x, y)
        
        if clicked_node:
            if self.mode == 'relation':
                self.handle_relation_click(clicked_node)
            else:
                self.select_node(clicked_node)
                self.drag_data['x'] = x
                self.drag_data['y'] = y
                self.dragging_node = clicked_node
        else:
            if self.mode == 'node':
                self.add_node(x, y)
            else:
                self.selected_node = None
                self.update_info_panel()

    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.dragging_node and self.mode == 'node':
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            
            self.dragging_node.x = x
            self.dragging_node.y = y
            
            self.drag_data['x'] = x
            self.drag_data['y'] = y
            
            self.redraw_canvas()

    def on_canvas_release(self, event):
        """Handle mouse release"""
        self.dragging_node = None

    def get_node_at_position(self, x, y):
        """Find node at position"""
        for node in self.nodes:
            distance = math.sqrt((node.x - x)**2 + (node.y - y)**2)
            if distance < 60:
                return node
        return None

    def add_node(self, x, y):
        """Add a new node"""
        self.node_counter += 1
        type_count = len([n for n in self.nodes if n.type == self.selected_tool])
        label = f"{self.selected_tool} {type_count + 1}"
        
        node = Node(self.node_counter, self.selected_tool, label, x, y)
        self.nodes.append(node)
        
        self.redraw_canvas()
        self.show_message(f"{self.selected_tool} ajouté", 'success')
        self.update_stats()

    def handle_relation_click(self, node):
        """Handle clicking nodes in relation mode"""
        if not self.relation_start:
            self.relation_start = node
            self.show_message("Sélectionnez le nœud de destination", 'info')
            self.redraw_canvas()
        else:
            if self.relation_start.id != node.id:
                self.add_relation(self.relation_start, node)
            self.relation_start = None
            self.redraw_canvas()

    def add_relation(self, from_node, to_node):
        """Add a relation with grammar validation"""
        if not GrammarValidator.validate_relation(from_node.type, to_node.type, 
                                                   self.selected_relation_type):
            allowed = GrammarValidator.get_allowed_relations(from_node.type, to_node.type)
            if allowed:
                msg = (f"Relation invalide!\n\n"
                      f"{self.selected_relation_type} entre {from_node.type} "
                      f"et {to_node.type} n'est pas permise.\n\n"
                      f"Relations autorisées: {', '.join(allowed)}")
            else:
                msg = (f"Relation invalide!\n\n"
                      f"Aucune relation n'est permise entre {from_node.type} "
                      f"et {to_node.type} selon la grammaire MOT.")
            
            messagebox.showerror("Erreur de Grammaire", msg)
            self.show_message("Relation refusée - Grammaire non respectée", 'error')
            return
        
        relation = Relation(from_node.id, to_node.id, self.selected_relation_type)
        self.relations.append(relation)
        
        self.redraw_canvas()
        self.update_relations_list()
        self.show_message(f"Relation {self.selected_relation_type} créée", 'success')
        self.update_stats()

    def select_node(self, node):
        """Select a node"""
        self.selected_node = node
        self.update_info_panel()
        self.redraw_canvas()

    def delete_selected_node(self):
        """Delete the selected node"""
        if not self.selected_node:
            return
        
        if messagebox.askyesno("Confirmer", 
                              f"Supprimer le nœud '{self.selected_node.label}' ?"):
            self.nodes = [n for n in self.nodes if n.id != self.selected_node.id]
            self.relations = [r for r in self.relations 
                            if r.from_node != self.selected_node.id 
                            and r.to_node != self.selected_node.id]
            
            self.selected_node = None
            self.redraw_canvas()
            self.update_info_panel()
            self.update_relations_list()
            self.show_message("Nœud supprimé", 'success')
            self.update_stats()

    def delete_relation(self, relation):
        """Delete a specific relation"""
        if messagebox.askyesno("Confirmer", "Supprimer cette relation ?"):
            self.relations = [r for r in self.relations if r.id != relation.id]
            self.redraw_canvas()
            self.update_relations_list()
            self.show_message("Relation supprimée", 'success')
            self.update_stats()

    def delete_selected_relation(self):
        """Delete relation selected in listbox"""
        selection = self.relations_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if idx < len(self.relations):
            self.delete_relation(self.relations[idx])

    def on_relation_select(self, event):
        """Handle relation selection in listbox"""
        selection = self.relations_listbox.curselection()
        self.delete_relation_btn.config(state=tk.NORMAL if selection else tk.DISABLED)

    def update_node_label(self, event):
        """Update node label"""
        if self.selected_node:
            self.selected_node.label = self.label_entry.get()
            self.redraw_canvas()

    def update_node_stereotype(self, event):
        """Update node stereotype"""
        if self.selected_node:
            self.selected_node.stereotype = self.stereotype_entry.get()
            self.redraw_canvas()

    def update_info_panel(self):
        """Update information panel"""
        if self.selected_node:
            config = KNOWLEDGE_TYPES[self.selected_node.type]
            info_text = f"Type: {self.selected_node.type}\n\n{config['description']}"
            self.info_label.config(text=info_text)
            
            self.label_entry.delete(0, tk.END)
            self.label_entry.insert(0, self.selected_node.label)
            
            self.stereotype_entry.delete(0, tk.END)
            self.stereotype_entry.insert(0, self.selected_node.stereotype)
            
            self.edit_frame.pack(fill=tk.X, pady=10)
        else:
            self.info_label.config(text="Aucun nœud sélectionné\n\nCliquez sur un nœud pour le sélectionner")
            self.edit_frame.pack_forget()

    def update_relations_list(self):
        """Update relations listbox"""
        self.relations_listbox.delete(0, tk.END)
        for rel in self.relations:
            from_node = next((n for n in self.nodes if n.id == rel.from_node), None)
            to_node = next((n for n in self.nodes if n.id == rel.to_node), None)
            if from_node and to_node:
                self.relations_listbox.insert(tk.END, 
                    f"{from_node.label} --[{rel.type}]--> {to_node.label}")

    def draw_node(self, node):
        """Draw a node on canvas"""
        config = KNOWLEDGE_TYPES[node.type]
        color = config['color']
        shape = config['shape']
        
        is_selected = self.selected_node and self.selected_node.id == node.id
        is_relation_start = self.relation_start and self.relation_start.id == node.id
        
        outline_color = '#ffff00' if is_relation_start else ('white' if is_selected else 'black')
        outline_width = 4 if (is_selected or is_relation_start) else 2
        
        x, y = node.x, node.y
        
        if shape == 'ellipse':
            node.canvas_id = self.canvas.create_oval(
                x - 60, y - 40, x + 60, y + 40,
                fill=color, outline=outline_color, width=outline_width
            )
        elif shape == 'hexagon':
            points = [x - 60, y, x - 30, y - 35, x + 30, y - 35,
                     x + 60, y, x + 30, y + 35, x - 30, y + 35]
            node.canvas_id = self.canvas.create_polygon(
                points, fill=color, outline=outline_color, width=outline_width
            )
        else:  # rect
            node.canvas_id = self.canvas.create_rectangle(
                x - 60, y - 30, x + 60, y + 30,
                fill=color, outline=outline_color, width=outline_width
            )
        
        # Draw stereotype if exists (above label, inside shape)
        if node.stereotype:
            node.stereotype_id = self.canvas.create_text(
                x, y - 15, text=f"«{node.stereotype}»",
                fill='white', font=('Arial', 8, 'italic')
            )
            # Draw label below stereotype
            node.text_id = self.canvas.create_text(
                x, y + 5, text=node.label, fill='white', 
                font=('Arial', 10, 'bold'), width=110
            )
        else:
            # Draw label centered
            node.text_id = self.canvas.create_text(
                x, y, text=node.label, fill='white', 
                font=('Arial', 10, 'bold'), width=110
            )

    def draw_relation(self, relation):
        """Draw a relation on canvas"""
        from_node = next((n for n in self.nodes if n.id == relation.from_node), None)
        to_node = next((n for n in self.nodes if n.id == relation.to_node), None)
        
        if not from_node or not to_node:
            return
        
        # Apply zoom
        x1, y1 = from_node.x * self.zoom_level, from_node.y * self.zoom_level
        x2, y2 = to_node.x * self.zoom_level, to_node.y * self.zoom_level
        
        # Calculate arrow points to stop at node edge
        angle = math.atan2(y2 - y1, x2 - x1)
        edge_offset = 65 * self.zoom_level
        x2_adj = x2 - edge_offset * math.cos(angle)
        y2_adj = y2 - edge_offset * math.sin(angle)
        
        line_width = max(1, int(2 * self.zoom_level))
        arrow_size = max(8, int(12 * self.zoom_level))
        
        relation.line_id = self.canvas.create_line(
            x1, y1, x2_adj, y2_adj,
            arrow=tk.LAST, width=line_width, fill='#333', 
            arrowshape=(arrow_size, arrow_size + 3, arrow_size // 2)
        )
        
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        label_size = 18 * self.zoom_level
        
        relation.label_bg_id = self.canvas.create_oval(
            mid_x - label_size, mid_y - label_size, mid_x + label_size, mid_y + label_size,
            fill='white', outline='#666', width=2
        )
        
        label_font_size = max(8, int(9 * self.zoom_level))
        
        relation.label_text_id = self.canvas.create_text(
            mid_x, mid_y, text=relation.type, fill='#333',
            font=('Arial', label_font_size, 'bold')
        )
        
        # Delete button
        delete_font_size = max(8, int(10 * self.zoom_level))
        delete_offset = 25 * self.zoom_level
        
        relation.delete_btn_id = self.canvas.create_text(
            mid_x + delete_offset, mid_y - delete_offset, text='❌', fill='#ef4444',
            font=('Arial', delete_font_size)
        )

    def redraw_canvas(self):
        """Redraw all elements"""
        self.canvas.delete('all')
        
        for relation in self.relations:
            self.draw_relation(relation)
        
        for node in self.nodes:
            self.draw_node(node)

    def update_stats(self):
        """Update statistics"""
        self.stats_label.config(
            text=f"Nœuds: {len(self.nodes)}\nRelations: {len(self.relations)}"
        )

    def show_message(self, text, msg_type='success'):
        """Show temporary message"""
        colors = {'success': '#10b981', 'error': '#ef4444', 'info': '#f59e0b'}
        
        self.message_label.config(text=text, bg=colors.get(msg_type, '#10b981'))
        self.message_label.pack(side=tk.RIGHT, padx=10)
        self.root.after(2500, lambda: self.message_label.pack_forget())

    def show_grammar_info(self):
        """Show grammar information window"""
        GrammarInfoWindow(self.root)

    def clear_model(self):
        """Clear the model"""
        if messagebox.askyesno("Confirmer", "Effacer tout le modèle ?"):
            self.nodes.clear()
            self.relations.clear()
            self.selected_node = None
            self.node_counter = 0
            self.redraw_canvas()
            self.update_info_panel()
            self.update_relations_list()
            self.update_stats()
            self.show_message("Modèle effacé", 'success')

    def export_text(self):
        """Export as text file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("MODÈLE MOT - Modélisation par Objets Typés\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("CONNAISSANCES:\n")
                f.write("-" * 60 + "\n")
                for node in self.nodes:
                    stereotype = f" <<{node.stereotype}>>" if node.stereotype else ""
                    f.write(f"• {node.label} ({node.type}){stereotype}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("RELATIONS:\n")
                f.write("-" * 60 + "\n")
                for relation in self.relations:
                    from_node = next((n for n in self.nodes if n.id == relation.from_node), None)
                    to_node = next((n for n in self.nodes if n.id == relation.to_node), None)
                    if from_node and to_node:
                        rel_name = RELATION_TYPES[relation.type]['label']
                        f.write(f"• {from_node.label} --[{relation.type}: {rel_name}]--> {to_node.label}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Statistiques: {len(self.nodes)} nœuds, {len(self.relations)} relations\n")
                f.write("=" * 60 + "\n")
            
            self.show_message("Export réussi", 'success')
            messagebox.showinfo("Succès", f"Modèle exporté vers:\n{filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")

    def export_json(self):
        """Export as JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            data = {
                'nodes': [node.to_dict() for node in self.nodes],
                'relations': [rel.to_dict() for rel in self.relations],
                'metadata': {
                    'node_counter': self.node_counter,
                    'version': '2.0'
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.show_message("Sauvegarde réussie", 'success')
            messagebox.showinfo("Succès", f"Modèle sauvegardé vers:\n{filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def load_json(self):
        """Load from JSON"""
        filename = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.nodes.clear()
            self.relations.clear()
            self.selected_node = None
            
            max_id = 0
            for node_data in data.get('nodes', []):
                node = Node(
                    node_data['id'],
                    node_data['type'],
                    node_data['label'],
                    node_data['x'],
                    node_data['y'],
                    node_data.get('stereotype', '')
                )
                self.nodes.append(node)
                max_id = max(max_id, node.id)
            
            self.node_counter = max_id
            
            for rel_data in data.get('relations', []):
                relation = Relation(
                    rel_data['from'],
                    rel_data['to'],
                    rel_data['type'],
                    rel_data.get('id')
                )
                self.relations.append(relation)
            
            self.redraw_canvas()
            self.update_stats()
            self.update_info_panel()
            self.update_relations_list()
            self.show_message("Chargement réussi", 'success')
            messagebox.showinfo("Succès", f"Modèle chargé depuis:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MOTEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()