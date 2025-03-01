import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
import random
from random_vital_preset import generate_random_preset, save_random_preset, get_style_ranges, random_name

class RandomPresetGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vital Random Preset Generator")
        self.root.geometry("1000x800")
        
        # Initialize all variables first
        self.output_dir = tk.StringVar(value="random_presets")
        self.preset_name = tk.StringVar(value="")
        self.num_presets = tk.StringVar(value="1")
        self.preset_style = tk.StringVar(value="Random")
        self.vol_min = tk.StringVar(value="1000")
        self.vol_max = tk.StringVar(value="8000")
        self.poly_min = tk.StringVar(value="1")
        self.poly_max = tk.StringVar(value="32")
        self.osc_level_min = tk.StringVar(value="0.5")
        self.osc_level_max = tk.StringVar(value="0.8")
        self.filter_cutoff_min = tk.StringVar(value="20")
        self.filter_cutoff_max = tk.StringVar(value="120")
        self.env_attack_min = tk.StringVar(value="0")
        self.env_attack_max = tk.StringVar(value="1")
        self.env_decay_min = tk.StringVar(value="0.3")
        self.env_decay_max = tk.StringVar(value="1")
        self.env_sustain_min = tk.StringVar(value="0")
        self.env_sustain_max = tk.StringVar(value="1")
        self.env_release_min = tk.StringVar(value="0.3")
        self.env_release_max = tk.StringVar(value="1")
        self.empty_mod_chance = tk.StringVar(value="70")
        self.mod_amount_min = tk.StringVar(value="-1.0")
        self.mod_amount_max = tk.StringVar(value="1.0")
        self.mod_power_min = tk.StringVar(value="-4.0")
        self.mod_power_max = tk.StringVar(value="4.0")
        self.status_var = tk.StringVar()
        
        # Style configuration
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Random.TButton", padding=2)
        
        # Create main container
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_container, text="Vital Random Preset Generator", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Controls
        controls_frame = ttk.LabelFrame(main_container, text="Generator Controls", padding="5")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Output directory
        ttk.Label(controls_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=2)
        output_entry = ttk.Entry(controls_frame, textvariable=self.output_dir)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(controls_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=2, pady=2)
        
        # Preset name
        ttk.Label(controls_frame, text="Preset Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        name_frame = ttk.Frame(controls_frame)
        name_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        ttk.Entry(name_frame, textvariable=self.preset_name).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(name_frame, text="Random", style="Random.TButton", 
                  command=lambda: self.preset_name.set(random_name())).pack(side=tk.RIGHT, padx=2)
        
        # Number of presets
        ttk.Label(controls_frame, text="Number of Presets:").grid(row=2, column=0, sticky=tk.W, pady=2)
        num_presets_spin = ttk.Spinbox(controls_frame, from_=1, to=100, textvariable=self.num_presets, width=5)
        num_presets_spin.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Preset style
        ttk.Label(controls_frame, text="Preset Style:").grid(row=3, column=0, sticky=tk.W, pady=2)
        styles = ["Random", "Keys", "Bass", "Lead", "Pad", "Pluck", "FX", "Drums", "Sequence"]
        style_combo = ttk.Combobox(controls_frame, textvariable=self.preset_style, values=styles)
        style_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        style_combo.bind('<<ComboboxSelected>>', self.update_ranges_from_style)
        
        # Parameter ranges notebook
        ranges_notebook = ttk.Notebook(controls_frame)
        ranges_notebook.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Basic ranges tab
        basic_ranges = ttk.Frame(ranges_notebook, padding="5")
        ranges_notebook.add(basic_ranges, text="Basic")
        
        # Volume range
        ttk.Label(basic_ranges, text="Volume Range:").grid(row=0, column=0, sticky=tk.W)
        vol_frame = ttk.Frame(basic_ranges)
        vol_frame.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Entry(vol_frame, textvariable=self.vol_min, width=8).pack(side=tk.LEFT)
        ttk.Label(vol_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(vol_frame, textvariable=self.vol_max, width=8).pack(side=tk.LEFT)
        ttk.Button(vol_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.vol_min, self.vol_max, 0, 10000)).pack(side=tk.LEFT, padx=2)
        
        # Polyphony range
        ttk.Label(basic_ranges, text="Polyphony Range:").grid(row=1, column=0, sticky=tk.W)
        poly_frame = ttk.Frame(basic_ranges)
        poly_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Entry(poly_frame, textvariable=self.poly_min, width=8).pack(side=tk.LEFT)
        ttk.Label(poly_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(poly_frame, textvariable=self.poly_max, width=8).pack(side=tk.LEFT)
        ttk.Button(poly_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.poly_min, self.poly_max, 1, 32)).pack(side=tk.LEFT, padx=2)
        
        # Oscillator ranges tab
        osc_ranges = ttk.Frame(ranges_notebook, padding="5")
        ranges_notebook.add(osc_ranges, text="Oscillator")
        
        # Oscillator level range
        ttk.Label(osc_ranges, text="Level Range:").grid(row=0, column=0, sticky=tk.W)
        osc_frame = ttk.Frame(osc_ranges)
        osc_frame.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Entry(osc_frame, textvariable=self.osc_level_min, width=8).pack(side=tk.LEFT)
        ttk.Label(osc_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(osc_frame, textvariable=self.osc_level_max, width=8).pack(side=tk.LEFT)
        ttk.Button(osc_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.osc_level_min, self.osc_level_max, 0, 1)).pack(side=tk.LEFT, padx=2)
        
        # Oscillator distortion type range
        ttk.Label(osc_ranges, text="Distortion Type:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(osc_ranges, text="(Fixed range: 0-12)").grid(row=1, column=1, sticky=tk.W)
        
        # Oscillator spectral morph range
        ttk.Label(osc_ranges, text="Spectral Morph:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(osc_ranges, text="(Fixed range: 0-15)").grid(row=2, column=1, sticky=tk.W)
        
        # Filter ranges tab
        filter_ranges = ttk.Frame(ranges_notebook, padding="5")
        ranges_notebook.add(filter_ranges, text="Filter")
        
        # Filter cutoff range
        ttk.Label(filter_ranges, text="Cutoff Range:").grid(row=0, column=0, sticky=tk.W)
        filter_frame = ttk.Frame(filter_ranges)
        filter_frame.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Entry(filter_frame, textvariable=self.filter_cutoff_min, width=8).pack(side=tk.LEFT)
        ttk.Label(filter_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(filter_frame, textvariable=self.filter_cutoff_max, width=8).pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.filter_cutoff_min, self.filter_cutoff_max, 0, 140)).pack(side=tk.LEFT, padx=2)
        
        # Envelope ranges tab
        env_ranges = ttk.Frame(ranges_notebook, padding="5")
        ranges_notebook.add(env_ranges, text="Envelope")
        
        # Create frames for each envelope parameter
        env_params = [
            ("Attack Range:", self.env_attack_min, self.env_attack_max, 0),
            ("Decay Range:", self.env_decay_min, self.env_decay_max, 1),
            ("Sustain Range:", self.env_sustain_min, self.env_sustain_max, 2),
            ("Release Range:", self.env_release_min, self.env_release_max, 3)
        ]
        
        for label_text, min_var, max_var, row in env_params:
            ttk.Label(env_ranges, text=label_text).grid(row=row, column=0, sticky=tk.W)
            frame = ttk.Frame(env_ranges)
            frame.grid(row=row, column=1, columnspan=3, sticky=(tk.W, tk.E))
            ttk.Entry(frame, textvariable=min_var, width=8).pack(side=tk.LEFT)
            ttk.Label(frame, text="-").pack(side=tk.LEFT, padx=2)
            ttk.Entry(frame, textvariable=max_var, width=8).pack(side=tk.LEFT)
            ttk.Button(frame, text="Random", style="Random.TButton",
                      command=lambda min_v=min_var, max_v=max_var: self.randomize_range(min_v, max_v, 0, 1)).pack(side=tk.LEFT, padx=2)
        
        # Modulation options
        mod_frame = ttk.LabelFrame(controls_frame, text="Modulation Options", padding="5")
        mod_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        mod_chance_frame = ttk.Frame(mod_frame)
        mod_chance_frame.pack(fill=tk.X)
        ttk.Label(mod_chance_frame, text="Empty Modulation Chance (%):").pack(side=tk.LEFT)
        ttk.Entry(mod_chance_frame, textvariable=self.empty_mod_chance, width=5).pack(side=tk.LEFT, padx=2)
        ttk.Button(mod_chance_frame, text="Random", style="Random.TButton",
                  command=lambda: self.empty_mod_chance.set(str(random.randint(0, 100)))).pack(side=tk.LEFT, padx=2)
        
        # Modulation amount range
        mod_amount_frame = ttk.Frame(mod_frame)
        mod_amount_frame.pack(fill=tk.X, pady=2)
        ttk.Label(mod_amount_frame, text="Modulation Amount Range:").pack(side=tk.LEFT)
        ttk.Entry(mod_amount_frame, textvariable=self.mod_amount_min, width=8).pack(side=tk.LEFT)
        ttk.Label(mod_amount_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(mod_amount_frame, textvariable=self.mod_amount_max, width=8).pack(side=tk.LEFT)
        ttk.Button(mod_amount_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.mod_amount_min, self.mod_amount_max, -1.0, 1.0)).pack(side=tk.LEFT, padx=2)
        
        # Modulation power range
        mod_power_frame = ttk.Frame(mod_frame)
        mod_power_frame.pack(fill=tk.X, pady=2)
        ttk.Label(mod_power_frame, text="Modulation Power Range:").pack(side=tk.LEFT)
        ttk.Entry(mod_power_frame, textvariable=self.mod_power_min, width=8).pack(side=tk.LEFT)
        ttk.Label(mod_power_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(mod_power_frame, textvariable=self.mod_power_max, width=8).pack(side=tk.LEFT)
        ttk.Button(mod_power_frame, text="Random", style="Random.TButton",
                  command=lambda: self.randomize_range(self.mod_power_min, self.mod_power_max, -4.0, 4.0)).pack(side=tk.LEFT, padx=2)
        
        # Generate button
        generate_btn = ttk.Button(controls_frame, text="Generate Presets", command=self.generate_presets)
        generate_btn.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Right panel - Generated Presets List
        presets_frame = ttk.LabelFrame(main_container, text="Generated Presets", padding="5")
        presets_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Presets listbox with scrollbar
        self.presets_list = tk.Listbox(presets_frame, height=20)
        scrollbar = ttk.Scrollbar(presets_frame, orient="vertical", command=self.presets_list.yview)
        self.presets_list.configure(yscrollcommand=scrollbar.set)
        
        self.presets_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        presets_frame.columnconfigure(0, weight=1)
        presets_frame.rowconfigure(0, weight=1)
        
        # Status bar
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def randomize_range(self, min_var, max_var, min_limit, max_limit):
        """Generate random range values ensuring min is less than max"""
        val1 = random.uniform(min_limit, max_limit)
        val2 = random.uniform(min_limit, max_limit)
        min_var.set(f"{min(val1, val2):.2f}")
        max_var.set(f"{max(val1, val2):.2f}")
    
    def update_ranges_from_style(self, event=None):
        style = self.preset_style.get()
        if style != "Random":
            ranges = get_style_ranges(style)
            
            # Update polyphony range
            self.poly_min.set(str(ranges["polyphony"][0]))
            self.poly_max.set(str(ranges["polyphony"][1]))
            
            # Update oscillator level range
            self.osc_level_min.set(str(ranges["osc_level"][0]))
            self.osc_level_max.set(str(ranges["osc_level"][1]))
            
            # Update filter cutoff range
            self.filter_cutoff_min.set(str(ranges["filter_cutoff"][0]))
            self.filter_cutoff_max.set(str(ranges["filter_cutoff"][1]))
            
            # Update envelope ranges
            self.env_attack_min.set(str(ranges["env_attack"][0]))
            self.env_attack_max.set(str(ranges["env_attack"][1]))
            self.env_decay_min.set(str(ranges["env_decay"][0]))
            self.env_decay_max.set(str(ranges["env_decay"][1]))
            self.env_sustain_min.set(str(ranges["env_sustain"][0]))
            self.env_sustain_max.set(str(ranges["env_sustain"][1]))
            self.env_release_min.set(str(ranges["env_release"][0]))
            self.env_release_max.set(str(ranges["env_release"][1]))
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def generate_presets(self):
        try:
            num_presets = int(self.num_presets.get())
            output_dir = self.output_dir.get()
            preset_name = self.preset_name.get()
            
            # Get parameter ranges
            volume_range = (float(self.vol_min.get()), float(self.vol_max.get()))
            polyphony_range = (int(self.poly_min.get()), int(self.poly_max.get()))
            empty_mod_chance = float(self.empty_mod_chance.get())
            
            # Get modulation ranges
            mod_amount_range = (float(self.mod_amount_min.get()), float(self.mod_amount_max.get()))
            mod_power_range = (float(self.mod_power_min.get()), float(self.mod_power_max.get()))
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Clear previous list
            self.presets_list.delete(0, tk.END)
            
            # Update status
            self.status_var.set(f"Generating {num_presets} presets...")
            self.root.update()
            
            # Generate presets
            for i in range(num_presets):
                # Generate filename
                if preset_name:
                    if num_presets > 1:
                        filename = f"{preset_name}_{i+1}.vital"
                    else:
                        filename = f"{preset_name}.vital"
                else:
                    filename = f"{random_name()}.vital"
                
                filepath = os.path.join(output_dir, filename)
                
                # Generate and save preset
                preset = generate_random_preset(
                    preset_style=self.preset_style.get(),
                    volume_range=volume_range,
                    polyphony_range=polyphony_range,
                    empty_mod_chance=empty_mod_chance,
                    mod_amount_range=mod_amount_range,
                    mod_power_range=mod_power_range
                )
                
                with open(filepath, 'w') as f:
                    json.dump(preset, f, indent=2)
                
                self.presets_list.insert(tk.END, filename)
                self.presets_list.see(tk.END)
                self.root.update()
            
            self.status_var.set(f"Successfully generated {num_presets} presets in {output_dir}")
            messagebox.showinfo("Success", f"Generated {num_presets} presets successfully!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate presets: {str(e)}")

def main():
    root = tk.Tk()
    app = RandomPresetGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 