import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class Gui(): 
    
    def __init__(self, jssp=None ,step=0 ):
        self.jssp = jssp
        self.render_mode=""
        
        self.icons_path=os.path.join(os.path.dirname(__file__), "icons\\")
        self.root_render_path =os.path.join(os.getcwd(), "renders\\")
        
        self.available_direct=[f.path for f in os.scandir(self.root_render_path) if f.is_dir()] 
        
        self.current_render_path=self.root_render_path
        if self.available_direct :
            self.current_render_path=self.available_direct[0]
          
        self.root = tk.Tk()
        self.root.title("Render solution")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.window = ttk.Frame(self.notebook)
        self.notebook.add(self.window, text="Petrinet")

        self.central_frame = ttk.Frame(self.window)
        self.central_frame.grid(row=1, column=1, padx=10, pady=10)
        
        self.empty_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.empty_frame, text="Plan")
        
        self.window.photo = None  # Initialize as None
                
        self.interval = 70 # Set the interval in milliseconds
        self.current_image_index = 0  # Track the current image index
        self.slideshow_running = False 
        


    def create_gui(self):

        # Create the top frame
        top_frame = ttk.Frame(self.window)
        top_frame.grid(row=0, column=1, padx=10, pady=10)
        
        # Create the central frame 
        central_frame = ttk.Frame(self.window)
        central_frame.grid(row=2, column=1, padx=10, pady=10)
 
        # Create the frame to the left
        left_frame = ttk.Frame(self.window)
        left_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ns")
 
        # Create the frame to the right
        right_frame = ttk.Frame(self.window)
        right_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ns")
 
        # Create another frame below the three defined frames
        bottom_frame = ttk.Frame(self.window)
        bottom_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
 
        # Configure grid row and column weights to make central frame expand
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
 
        
        def apply_speed():
            # Get the speed from the Spinbox
            new_speed = int(self.speed_spinbox.get())
            self.interval = new_speed
            print(f"New slideshow speed set to {new_speed} ms")
            
        def next_button_click():
             if self.current_image_index <len(os.listdir(self.current_render_path))-1:
                 self.current_image_index +=1 
                 self.update_image(self.current_image_index)
      
        def previous_button_click():
             if self.current_image_index >=1 :
                 self.current_image_index -= 1
                 self.update_image(self.current_image_index)
                   
        def reset_button_click():
            self.update_image(0)
            self.current_image_index = 0
               
        def relode_button_click():
            print("Relode button clicked!")
            for widget in central_frame.winfo_children():
                widget.destroy()
                        
        def backward_button_click():
            print("backward button clicked!")
        def forward_button_click():
            print("forward button clicked!")
        
        def pause_button_click():
            #print("pause button clicked!")
            self.slideshow_running = False 
            

        def play_button_click():      
            if not self.slideshow_running:
               self.slideshow_running = True
               self.play_slideshow()


        # Create a frame to hold the buttons
        buttons_frame = tk.Frame(bottom_frame)
        buttons_frame.pack(padx=10, pady=10 ,anchor="w")

        # Load the custom button images
        backward_image = ImageTk.PhotoImage(file=self.icons_path+"backward.png")
        forward_image = ImageTk.PhotoImage(file=self.icons_path+"forward.png")
        pause_image = ImageTk.PhotoImage(file=self.icons_path+"pause.png")
        play_image = ImageTk.PhotoImage(file=self.icons_path+"play.png")
        next_image = ImageTk.PhotoImage(file=self.icons_path+"next.png")
        previous_image = ImageTk.PhotoImage(file=self.icons_path+"previous.png")
        relode_image = ImageTk.PhotoImage(file=self.icons_path+"repeat.png")   
        reset_image = ImageTk.PhotoImage(file=self.icons_path+"reset.png")

        # Create the buttons with the custom images
        backward_button = ttk.Button(buttons_frame, image=backward_image, command=backward_button_click)
        forward_button = ttk.Button(buttons_frame, image=forward_image, command=forward_button_click)
        pause_button = ttk.Button(buttons_frame, image=pause_image, command=pause_button_click)
        play_button = ttk.Button(buttons_frame, image=play_image, command=play_button_click)     
        next_button = ttk.Button(buttons_frame, image=next_image, command=next_button_click) 
        previous_button = ttk.Button(buttons_frame, image=previous_image, command=previous_button_click)  
        relode_button = ttk.Button(buttons_frame, image=relode_image, command=relode_button_click)   
        reset_button = ttk.Button(buttons_frame, image=reset_image, command=reset_button_click)      
        
        # Keep a reference to the image
        backward_button.image = backward_image 
        forward_button.image = forward_image 
        pause_button.image = pause_image        
        play_button.image = play_image   
        next_button.image = next_image
        previous_button.image = previous_image
        relode_button.image = relode_image
        reset_button.image = reset_image
        
        # pack buttons in the GUI 
        backward_button.pack(side="left", padx=5, pady=5)
        forward_button.pack(side="left", padx=5, pady=5)
        pause_button.pack(side="left", padx=5, pady=5)
        play_button.pack(side="left", padx=5, pady=5)
        previous_button.pack(side="left", padx=5, pady=5)
        next_button.pack(side="left", padx=5, pady=5)
        relode_button.pack(side="right", padx=5, pady=5)    
        reset_button.pack(side="right", padx=50, pady=5)
        
        
       # Create a label for the slideshow speed
        speed_label = ttk.Label(top_frame, text="Slideshow Speed (ms):")
        speed_label.grid(row=2, column=0, padx=(5, 0), pady=5, sticky="e")
        
        # Create a Spinbox for the user to select the speed
        self.speed_spinbox = ttk.Spinbox(top_frame, from_=10, to=200, increment=10, width=5)
        self.speed_spinbox.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="w")
        
        # Create a button to apply the new speed
        apply_speed_button = ttk.Button(top_frame, text="Apply Speed", command=apply_speed)
        apply_speed_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        
        
        def on_directory_change(event):
            self.slideshow_running = False 
            self.current_render_path = directory_combobox.get()+"\\"
            self.current_image_index = 0 
            #self.display_solution()
              
        # Create a label for the dropdown list
        directory_label = ttk.Label(top_frame, text="Available Directories:")
        directory_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Create a Combobox widget to display available directories
        directory_combobox = ttk.Combobox(top_frame, values=self.available_direct ,width=120)
        directory_combobox.grid(row=0, column=1, padx=5, pady=5)
        directory_combobox.bind("<<ComboboxSelected>>", lambda event, self=self: on_directory_change(event))
               
            
    def display_solution(self):
         
         image = Image.open(self.current_render_path+f"{self.jssp.instanceID}.jpg")
         photo = ImageTk.PhotoImage(image)
         label = ttk.Label(self.empty_frame, image=photo)
         label.image = photo  
         label.grid(row=0, column=0)
            

    def play_slideshow(self):
    
        if self.slideshow_running:
            self.update_image(self.current_image_index)
            self.current_image_index += 1

            if self.current_image_index >= len(os.listdir(self.current_render_path)):
                self.current_image_index = 0

            self.root.after(self.interval, self.play_slideshow)
            
   
    def update_image(self,step):
        
                    # Define the fixed size for the image    
        fixed_width = 800
        fixed_height = 600
        
        image_path=self.current_render_path+str(step+1)+".jpg"
        image = Image.open(image_path)
            
        # Update the image displayed in the GUI
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        # Calculate the new width and height based on the fixed dimensions and aspect ratio
        if fixed_width / aspect_ratio <= fixed_height:
            new_width = fixed_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = fixed_height
            new_width = int(new_height * aspect_ratio)
                     
        resized_image = image.resize((new_width, new_height)) 
        # Calculate the position to paste the resized image in the white image
        x = (fixed_width - new_width) // 2
        y = (fixed_height - new_height) // 2
        
        # Create the white image and paste the resized image in the center
        white_image = Image.new('RGB', (fixed_width, fixed_height), 'white')
        white_image.paste(resized_image, (x, y))
        
        # Create the PhotoImage from the white image
        photo = ImageTk.PhotoImage(white_image)
        # Remove any existing label before creating a new one
        for widget in self.central_frame.winfo_children():
            widget.destroy()
    
        label = tk.Label(self.central_frame, image=photo)
        label.image = photo
        label.pack()
        
        
    def launch_gui(self):
        self.create_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)  # Bind the close event
        self.root.mainloop()

    def on_window_close(self):
        self.root.quit()  # Quit the main event loop
        self.root.destroy()  # Destroy the root window


if __name__ == "__main__":
    
    pass
   
   
    



    

    

    