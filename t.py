import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# Create a frame
frame = tk.Frame(root, relief="ridge", borderwidth=2)
frame.pack(padx=10, pady=10)

# Create a label as the header
header_label = tk.Label(frame, text="My LabelFrame", font=("Arial", 12, "bold"), bg='red')
header_label.pack(pady=5)

# Add widgets to the frame
label1 = tk.Label(frame, text="Widget 1")
label1.pack()
label2 = tk.Label(frame, text="Widget 2")
label2.pack()

root.mainloop()
