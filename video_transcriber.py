#!/usr/bin/env python3
"""
Video Transcription Tool using Gemini 2.5 Pro
Features: API key management, video transcription/translation, SRT output, progress tracking
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
import time
import threading
from pathlib import Path
from datetime import timedelta
import google.generativeai as genai


class APIKeyManager:
    """Manage multiple Gemini API keys"""
    
    def __init__(self, config_file="api_keys.json"):
        self.config_file = config_file
        self.keys = self.load_keys()
    
    def load_keys(self):
        """Load API keys from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading API keys: {e}")
                return {}
        return {}
    
    def save_keys(self):
        """Save API keys to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
        except Exception as e:
            print(f"Error saving API keys: {e}")
    
    def add_key(self, name, key):
        """Add or update an API key"""
        self.keys[name] = key
        self.save_keys()
    
    def remove_key(self, name):
        """Remove an API key"""
        if name in self.keys:
            del self.keys[name]
            self.save_keys()
    
    def get_key(self, name):
        """Get an API key by name"""
        return self.keys.get(name)
    
    def get_all_names(self):
        """Get all API key names"""
        return list(self.keys.keys())


class VideoTranscriber:
    """Handle video transcription using Gemini API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
    
    def transcribe_video(self, video_path, prompt, temperature=0.7, progress_callback=None):
        """
        Transcribe video using Gemini 2.5 Pro
        Returns the transcription text
        """
        try:
            if progress_callback:
                progress_callback(10, "Uploading video to Gemini...")
            
            # Upload video file
            video_file = genai.upload_file(path=video_path)
            
            if progress_callback:
                progress_callback(30, "Processing video...")
            
            # Wait for video to be processed
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed")
            
            if progress_callback:
                progress_callback(50, "Generating transcription...")
            
            # Use Gemini 2.5 Pro for video understanding
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config={
                    "temperature": temperature,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                }
            )
            
            # Generate transcription
            response = model.generate_content([video_file, prompt])
            
            if progress_callback:
                progress_callback(90, "Finalizing...")
            
            # Clean up uploaded file
            genai.delete_file(video_file.name)
            
            if progress_callback:
                progress_callback(100, "Complete!")
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
    
    def parse_srt_from_text(self, text):
        """
        Parse SRT format from the transcription text
        If the text is already in SRT format, return it as-is
        Otherwise, create a simple SRT with the full text
        """
        # Check if text already looks like SRT format
        lines = text.strip().split('\n')
        if len(lines) > 2 and lines[0].strip().isdigit() and '-->' in lines[1]:
            return text
        
        # If not in SRT format, create a simple single-entry SRT
        srt_content = "1\n"
        srt_content += "00:00:00,000 --> 00:00:10,000\n"
        srt_content += text.replace('\n', ' ') + "\n"
        return srt_content


class VideoTranscriberGUI:
    """GUI for video transcription application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Video Transcriber")
        self.root.geometry("900x800")
        
        self.api_manager = APIKeyManager()
        self.selected_video = None
        self.output_mode = tk.StringVar(value="original")
        self.custom_folder = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI layout"""
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # API Key Section
        ttk.Label(main_frame, text="API Key Management", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        ttk.Label(main_frame, text="Select API Key:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.api_key_combo = ttk.Combobox(main_frame, state="readonly", width=30)
        self.api_key_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.refresh_api_keys()
        
        ttk.Button(main_frame, text="Manage Keys", command=self.open_key_manager).grid(
            row=row, column=2, pady=5, padx=5
        )
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Video Selection
        ttk.Label(main_frame, text="Video File", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        ttk.Label(main_frame, text="Selected Video:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.video_label = ttk.Label(main_frame, text="No video selected", foreground="gray")
        self.video_label.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.select_video).grid(
            row=row, column=2, pady=5, padx=5
        )
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Output Settings
        ttk.Label(main_frame, text="Output Settings", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        ttk.Radiobutton(
            main_frame, text="Save in original video folder", 
            variable=self.output_mode, value="original"
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        
        ttk.Radiobutton(
            main_frame, text="Save in custom folder:", 
            variable=self.output_mode, value="custom"
        ).grid(row=row, column=0, sticky=tk.W, pady=2)
        
        self.custom_folder_label = ttk.Label(main_frame, text="Not set", foreground="gray")
        self.custom_folder_label.grid(row=row, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.select_output_folder).grid(
            row=row, column=2, pady=2, padx=5
        )
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Transcription Settings
        ttk.Label(main_frame, text="Transcription Settings", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        # Temperature
        ttk.Label(main_frame, text="Temperature:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.temp_var = tk.DoubleVar(value=0.7)
        temp_frame = ttk.Frame(main_frame)
        temp_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.temp_scale = ttk.Scale(temp_frame, from_=0, to=2, variable=self.temp_var, orient=tk.HORIZONTAL)
        self.temp_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.temp_label = ttk.Label(temp_frame, text="0.70")
        self.temp_label.pack(side=tk.LEFT, padx=5)
        self.temp_var.trace_add("write", self.update_temp_label)
        row += 1
        
        # Prompt
        ttk.Label(main_frame, text="Prompt:", anchor=tk.W).grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5
        )
        row += 1
        
        prompt_frame = ttk.Frame(main_frame)
        prompt_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        prompt_frame.columnconfigure(0, weight=1)
        prompt_frame.rowconfigure(0, weight=1)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=8, wrap=tk.WORD)
        self.prompt_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.prompt_text.insert("1.0", 
            "Please transcribe this video with timestamps in SRT format. "
            "Include accurate timing for each subtitle segment. "
            "Format each entry as:\n"
            "1\n"
            "00:00:00,000 --> 00:00:05,000\n"
            "Transcribed text here\n\n"
            "Continue this pattern for the entire video."
        )
        
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Progress Section
        ttk.Label(main_frame, text="Progress", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100, length=300
        )
        self.progress_bar.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        self.transcribe_btn = ttk.Button(
            button_frame, text="Start Transcription", command=self.start_transcription
        )
        self.transcribe_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def update_temp_label(self, *args):
        """Update temperature label when slider moves"""
        self.temp_label.config(text=f"{self.temp_var.get():.2f}")
    
    def refresh_api_keys(self):
        """Refresh the API key dropdown"""
        keys = self.api_manager.get_all_names()
        self.api_key_combo['values'] = keys
        if keys:
            self.api_key_combo.current(0)
    
    def open_key_manager(self):
        """Open API key management window"""
        KeyManagerWindow(self.root, self.api_manager, self.refresh_api_keys)
    
    def select_video(self):
        """Open file dialog to select video"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.selected_video = filename
            self.video_label.config(text=os.path.basename(filename), foreground="black")
    
    def select_output_folder(self):
        """Select custom output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.custom_folder = folder
            self.custom_folder_label.config(
                text=os.path.basename(folder) or folder, foreground="black"
            )
    
    def update_progress(self, value, status):
        """Update progress bar and status label"""
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def start_transcription(self):
        """Start the transcription process"""
        # Validation
        if not self.api_key_combo.get():
            messagebox.showerror("Error", "Please select an API key")
            return
        
        if not self.selected_video:
            messagebox.showerror("Error", "Please select a video file")
            return
        
        if self.output_mode.get() == "custom" and not self.custom_folder:
            messagebox.showerror("Error", "Please select a custom output folder")
            return
        
        # Disable button during processing
        self.transcribe_btn.config(state="disabled")
        
        # Run transcription in separate thread
        thread = threading.Thread(target=self.run_transcription)
        thread.daemon = True
        thread.start()
    
    def run_transcription(self):
        """Run the transcription process in a separate thread"""
        try:
            # Get settings
            api_key_name = self.api_key_combo.get()
            api_key = self.api_manager.get_key(api_key_name)
            temperature = self.temp_var.get()
            prompt = self.prompt_text.get("1.0", tk.END).strip()
            
            # Initialize transcriber
            self.update_progress(0, "Initializing...")
            transcriber = VideoTranscriber(api_key)
            
            # Transcribe video
            self.update_progress(5, "Starting transcription...")
            result = transcriber.transcribe_video(
                self.selected_video,
                prompt,
                temperature,
                self.update_progress
            )
            
            # Parse SRT format
            srt_content = transcriber.parse_srt_from_text(result)
            
            # Determine output path
            video_path = Path(self.selected_video)
            if self.output_mode.get() == "original":
                output_dir = video_path.parent
            else:
                output_dir = Path(self.custom_folder)
            
            output_file = output_dir / f"{video_path.stem}.srt"
            
            # Save SRT file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            self.update_progress(100, f"Complete! Saved to: {output_file}")
            messagebox.showinfo("Success", f"Transcription saved to:\n{output_file}")
        
        except Exception as e:
            self.update_progress(0, "Error occurred")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.transcribe_btn.config(state="normal")


class KeyManagerWindow:
    """Window for managing API keys"""
    
    def __init__(self, parent, api_manager, refresh_callback):
        self.api_manager = api_manager
        self.refresh_callback = refresh_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("API Key Manager")
        self.window.geometry("600x400")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the key manager UI"""
        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # List of keys
        ttk.Label(frame, text="Saved API Keys:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.key_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.key_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.key_listbox.yview)
        
        self.refresh_list()
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Add New Key", command=self.add_key).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_key).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def refresh_list(self):
        """Refresh the list of API keys"""
        self.key_listbox.delete(0, tk.END)
        for name in self.api_manager.get_all_names():
            self.key_listbox.insert(tk.END, name)
    
    def add_key(self):
        """Add a new API key"""
        dialog = AddKeyDialog(self.window, self.api_manager)
        self.window.wait_window(dialog.window)
        self.refresh_list()
        self.refresh_callback()
    
    def remove_key(self):
        """Remove selected API key"""
        selection = self.key_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a key to remove")
            return
        
        key_name = self.key_listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Remove API key '{key_name}'?"):
            self.api_manager.remove_key(key_name)
            self.refresh_list()
            self.refresh_callback()


class AddKeyDialog:
    """Dialog for adding a new API key"""
    
    def __init__(self, parent, api_manager):
        self.api_manager = api_manager
        
        self.window = tk.Toplevel(parent)
        self.window.title("Add API Key")
        self.window.geometry("400x150")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Key name
        ttk.Label(frame, text="Key Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # API key
        ttk.Label(frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.key_entry = ttk.Entry(frame, width=40, show="*")
        self.key_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        """Save the API key"""
        name = self.name_entry.get().strip()
        key = self.key_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a key name")
            return
        
        if not key:
            messagebox.showerror("Error", "Please enter an API key")
            return
        
        self.api_manager.add_key(name, key)
        self.window.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = VideoTranscriberGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
