import tkinter as tk
import tkinter.ttk as ttk

def genScreen():
    screen = tk.Tk()
    screen.geometry("410x400")
    label = tk.Label(screen)
    label.grid()
    screen.wm_title("Hello, world")
    return screen, label

screen = tk.Tk()
screen.geometry("410x100")
label = tk.Label(screen)
label.grid()
screen.wm_title("Hello, world")


data = []

def exitScreen():
    try:
        for i in range(0, slider.get()):
            data.append([])
        print(data)
    except:
        pass
    screen.destroy()

#def exit2(i):
 #   data[i].append()


slider =  tk.Scale(label, from_=1, to=5, orient = tk.HORIZONTAL, fg ='#000000', bg ='#6699CC', length = 400, command = None, label = "Number of nodes")
slider.grid(row = 0, column = 0)


b = ttk.Button(screen, text="OK", command= exitScreen)
b.grid(row = 2, column = 0)

screen.mainloop()

for i in range(0, 6):

    screen, label = genScreen()
    sliders = []
    for j in range(0, len(data)):

        slider = tk.Scale(label, from_=5, to=50, orient = tk.HORIZONTAL, fg ='#000000', bg ='#6699CC', length = 400, command = None, label = ("Node", j+1))
        slider.grid(row = j, column = 0)

    b = ttk.Button(screen, text="OK", command= screen.destroy)
    b.grid(row = 2, column = 0)


    screen.mainloop()