import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageOps

class ModernImageFilter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Image Filter")
        self.root.geometry("1300x700")
        self.root.configure(bg="#1e3a5f")  # Blue background
        
        # Variables
        self.original_image = None
        self.filtered_image = None
        self.image_path = None
        self.filter_var = tk.StringVar(value="original")
        
        # Create modern UI with blue theme
        self.create_modern_ui()
        
    def create_modern_ui(self):
        # TOP: Clean header with blue theme
        header_frame = tk.Frame(self.root, bg="#2c5282")  # Darker blue
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # App name
        tk.Label(header_frame, text="Modern Filters", 
                font=("Arial", 24, "bold"), bg="#2c5282", fg="#ffffff").pack(side=tk.LEFT, padx=20, pady=15)
        
        # Action buttons
        action_frame = tk.Frame(header_frame, bg="#2c5282")
        action_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(action_frame, text="📁 Load", command=self.load_image,
                 bg="#3182ce", fg="white", font=("Arial", 10), 
                 relief=tk.RAISED, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="💾 Save", command=self.save_image,
                 bg="#38a169", fg="white", font=("Arial", 10),
                 relief=tk.RAISED, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="↻ Reset", command=self.reset_all,
                 bg="#e53e3e", fg="white", font=("Arial", 10),
                 relief=tk.RAISED, width=10).pack(side=tk.LEFT, padx=5)
        
        # Filter selection area
        filter_frame = tk.Frame(self.root, bg="#2d3748")  # Dark blue-gray
        filter_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Filter buttons with blue theme
        filters = [
            ("Original / Natural", "original"),
            ("Warm", "warm"),
            ("Cool", "cool"),
            ("Bright", "bright"),
            ("Contrast", "contrast"),
            ("Vivid", "vivid"),
            ("Matte", "matte"),
            ("Black & White", "bw"),
            ("Blur", "blur")
        ]
        
        # Create filter buttons in a grid
        for i, (text, value) in enumerate(filters):
            btn = tk.Radiobutton(filter_frame, text=text, variable=self.filter_var,
                                value=value, bg="#4a5568", fg="#e2e8f0",
                                selectcolor="#3182ce", font=("Arial", 10),
                                indicatoron=0, width=14, height=2,
                                command=self.apply_filter)
            row = i // 5  # 5 buttons per row
            col = i % 5
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid columns
        for i in range(5):
            filter_frame.grid_columnconfigure(i, weight=1)
        
        # Image display area
        image_frame = tk.Frame(self.root, bg="#1e3a5f")
        image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Original image panel
        orig_frame = tk.LabelFrame(image_frame, text="Original Image",
                                  font=("Arial", 12, "bold"),
                                  bg="#2d3748", fg="#e2e8f0", relief=tk.GROOVE)
        orig_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.original_panel = tk.Label(orig_frame, bg="#1a202c", 
                                      text="No image loaded",
                                      font=("Arial", 12), fg="#a0aec0")
        self.original_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Filtered image panel
        filt_frame = tk.LabelFrame(image_frame, text="Filtered Image",
                                  font=("Arial", 12, "bold"),
                                  bg="#2d3748", fg="#e2e8f0", relief=tk.GROOVE)
        filt_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.filtered_panel = tk.Label(filt_frame, bg="#1a202c",
                                      text="Select a filter",
                                      font=("Arial", 12), fg="#a0aec0")
        self.filtered_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar at bottom
        status_frame = tk.Frame(self.root, bg="#2c5282", height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    bg="#2c5282", fg="#cbd5e0",
                                    font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def load_image(self):
        """Load an image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                self.image_path = file_path
                img = cv2.imread(file_path)
                if img is None:
                    messagebox.showerror("Error", "Failed to load image!")
                    return
                
                self.original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.filtered_image = self.original_image.copy()
                self.filter_var.set("original")
                self.display_images()
                
                filename = file_path.split('/')[-1]
                self.status_label.config(text=f"Loaded: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_images(self):
        """Display both images"""
        if self.original_image is not None:
            # Calculate size based on window
            frame_width = self.root.winfo_width() // 2 - 60
            frame_height = self.root.winfo_height() - 220
            
            max_size = min(frame_width, frame_height, 550)
            
            # Original image
            orig_resized = self.resize_image(self.original_image, max_size)
            if orig_resized is not None:
                orig_img = Image.fromarray(orig_resized)
                orig_tk = ImageTk.PhotoImage(orig_img)
                self.original_panel.config(image=orig_tk, text="")
                self.original_panel.image = orig_tk
            
            # Filtered image
            filt_resized = self.resize_image(self.filtered_image, max_size)
            if filt_resized is not None:
                filt_img = Image.fromarray(filt_resized)
                filt_tk = ImageTk.PhotoImage(filt_img)
                self.filtered_panel.config(image=filt_tk, text="")
                self.filtered_panel.image = filt_tk
    
    def resize_image(self, image, max_size):
        """Resize image while keeping aspect ratio"""
        if image is None:
            return None
            
        height, width = image.shape[:2]
        if max(width, height) > max_size:
            ratio = max_size / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return cv2.resize(image, (new_width, new_height))
        return image
    
    def apply_filter(self):
        """Apply modern filters"""
        if self.original_image is None:
            return
        
        self.filtered_image = self.original_image.copy()
        filter_type = self.filter_var.get()
        
        try:
            if filter_type == "original":
                # Original - no change
                pass
                
            elif filter_type == "warm":
                # Warm filter - increase red/orange tones
                img_array = self.filtered_image.astype(np.float32)
                
                # Increase red channel
                img_array[:, :, 0] *= 1.15  # Red
                img_array[:, :, 1] *= 1.05  # Green (slightly)
                img_array[:, :, 2] *= 0.95  # Blue (reduce)
                
                # Add warm tint
                img_array[:, :, 0] += 10  # Add red tint
                img_array[:, :, 1] += 5   # Add yellow tint
                
                self.filtered_image = np.clip(img_array, 0, 255).astype(np.uint8)
                
            elif filter_type == "cool":
                # Cool filter - increase blue tones
                img_array = self.filtered_image.astype(np.float32)
                
                # Increase blue channel
                img_array[:, :, 0] *= 0.95  # Red (reduce)
                img_array[:, :, 1] *= 1.05  # Green (slightly)
                img_array[:, :, 2] *= 1.15  # Blue
                
                # Add cool tint
                img_array[:, :, 2] += 10  # Add blue tint
                
                self.filtered_image = np.clip(img_array, 0, 255).astype(np.uint8)
                
            elif filter_type == "bright":
                # Bright filter - increase brightness
                img_array = self.filtered_image.astype(np.float32)
                
                # Increase brightness
                img_array += 30
                
                # Increase contrast slightly
                mean = np.mean(img_array)
                img_array = (img_array - mean) * 1.1 + mean
                
                self.filtered_image = np.clip(img_array, 0, 255).astype(np.uint8)
                
            elif filter_type == "contrast":
                # Contrast filter - increase contrast
                img_array = self.filtered_image.astype(np.float32)
                
                # Calculate mean
                mean = np.mean(img_array)
                
                # Increase contrast
                img_array = (img_array - mean) * 1.3 + mean
                
                self.filtered_image = np.clip(img_array, 0, 255).astype(np.uint8)
                
            elif filter_type == "vivid":
                # Vivid filter - increase saturation and contrast
                img_array = self.filtered_image.astype(np.float32)
                
                # Convert to HSV for saturation adjustment
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                hsv = hsv.astype(np.float32)
                
                # Increase saturation
                hsv[:, :, 1] *= 1.5
                hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
                
                # Increase value (brightness) slightly
                hsv[:, :, 2] *= 1.1
                hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
                
                # Convert back to RGB
                self.filtered_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
                
                # Increase contrast
                mean = np.mean(self.filtered_image)
                self.filtered_image = (self.filtered_image.astype(np.float32) - mean) * 1.2 + mean
                self.filtered_image = np.clip(self.filtered_image, 0, 255).astype(np.uint8)
                
            elif filter_type == "matte":
                # Matte filter - soft, desaturated look
                img_array = self.filtered_image.astype(np.float32)
                
                # Convert to HSV
                hsv = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
                hsv = hsv.astype(np.float32)
                
                # Reduce saturation
                hsv[:, :, 1] *= 0.6
                
                # Reduce contrast
                mean = np.mean(hsv[:, :, 2])
                hsv[:, :, 2] = (hsv[:, :, 2] - mean) * 0.8 + mean
                
                # Convert back to RGB
                self.filtered_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
                
                # Add slight warm tint
                self.filtered_image = self.filtered_image.astype(np.float32)
                self.filtered_image[:, :, 0] += 5  # Red
                self.filtered_image[:, :, 1] += 3  # Green
                self.filtered_image = np.clip(self.filtered_image, 0, 255).astype(np.uint8)
                
            elif filter_type == "bw":
                # Black & White filter
                # Convert to grayscale
                gray = cv2.cvtColor(self.filtered_image, cv2.COLOR_RGB2GRAY)
                
                # Enhance contrast
                gray = cv2.equalizeHist(gray)
                
                # Convert back to 3 channels
                self.filtered_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
                
            elif filter_type == "blur":
                # Blur filter - soft Gaussian blur
                self.filtered_image = cv2.GaussianBlur(self.filtered_image, (7, 7), 2)
            
            self.display_images()
            self.status_label.config(text=f"Applied: {filter_type}")
            
        except Exception as e:
            print(f"Filter error: {e}")
    
    def reset_all(self):
        """Reset to original image"""
        if self.original_image is not None:
            self.filtered_image = self.original_image.copy()
            self.filter_var.set("original")
            self.display_images()
            self.status_label.config(text="Reset to original")
    
    def save_image(self):
        """Save filtered image"""
        if self.filtered_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), 
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    save_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(file_path, save_image)
                    messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
                    self.status_label.config(text=f"Saved: {file_path.split('/')[-1]}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def run(self):
        """Run application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = ModernImageFilter()
    app.run()
