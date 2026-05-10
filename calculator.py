from tkinter import *
# Building a calculator:
root=Tk()
root.title("Calculator")
operator=""
f_Num=0
entry =Entry(root,width=40, borderwidth=5)
entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)



def button_click(number):
    current= entry.get() # gets what in the box currently
    entry.delete(0, END) # Deletes the thing in box
    entry.insert(0, str(current)+ str(number))
    
def button_clears():
    entry.delete(0, END)    
    
def button_action(op):
    global f_Num, operator
    if entry.get() == "":  # ← guard against empty box
        return
    first_number=entry.get()
   
    f_Num=int(first_number)
    entry.delete(0,END)
    operator=str(op)   
    
    
def button_equals():
    second_number=int(entry.get())
    entry.delete(0,END)
    
    if (operator == "+"):
        entry.insert(0, f_Num + second_number)
    
    elif (operator=="-"):
        entry.insert(0, f_Num - second_number)
    elif (operator=="x"):
        entry.insert(0, f_Num * second_number)
    elif (operator=="/"):
        entry.insert(0, f_Num /second_number)
    else:
        return
    
    
button_1=Button(root, text="1", padx=40,pady=20,command=lambda: button_click(1))
button_2=Button(root, text="2", padx=40,pady=20,command=lambda: button_click(2))
button_3=Button(root, text="3", padx=40,pady=20,command=lambda: button_click(3))
button_4=Button(root, text="4", padx=40,pady=20,command=lambda: button_click(4))
button_5=Button(root, text="5", padx=40,pady=20,command=lambda: button_click(5))
button_6=Button(root, text="6", padx=40,pady=20,command=lambda: button_click(6))
button_7=Button(root, text="7", padx=40,pady=20,command=lambda: button_click(7))
button_8=Button(root, text="8", padx=40,pady=20,command=lambda: button_click(8))
button_9=Button(root, text="9", padx=40,pady=20,command=lambda: button_click(9))
button_0=Button(root, text="0", padx=40,pady=20,command=lambda: button_click(0))

button_addition=Button(root, text="+",padx=40,pady=20,command=lambda: button_action("+"),bg="light blue")
button_sub=Button(root, text="-",padx=40,pady=20,command=lambda: button_action("-"),bg="light blue")
button_multiply=Button(root, text="x",padx=40,pady=20,command=lambda: button_action("x"),bg="light blue")
button_divide=Button(root, text="/",padx=40,pady=20,command=lambda: button_action("/"),bg="light blue")
button_equal=Button(root, text="=",padx=40,pady=20,command=button_equals,bg="light blue")

button_clear=Button(root, text="C",padx=40,pady=20,command=button_clears,bg="light blue")
    
# Positioning the buttons
button_1.grid(row=3,column=0)    
button_2.grid(row=3,column=1)    
button_3.grid(row=3,column=2)
button_divide.grid(row=3,column=3)
  
 
button_4.grid(row=2,column=0)    
button_5.grid(row=2,column=1)    
button_6.grid(row=2,column=2)    
button_multiply.grid(row=2,column=3)    

button_7.grid(row=1,column=0)    
button_8.grid(row=1,column=1)    
button_9.grid(row=1,column=2)    
button_clear.grid(row=1,column=3)    

button_0.grid(row=4,column=0)   
button_addition.grid(row=4,column=1)   
button_sub.grid(row=4,column=2)   
button_equal.grid(row=4,column=3)   
    
    

# key binds
root.bind("1", lambda event: button_click(1))
root.bind("2", lambda event: button_click(2))
root.bind("3", lambda event: button_click(3))
root.bind("4", lambda event: button_click(4))
root.bind("5", lambda event: button_click(5))
root.bind("6", lambda event: button_click(6))
root.bind("7", lambda event: button_click(7))
root.bind("8", lambda event: button_click(8))
root.bind("9", lambda event: button_click(9))
root.bind("0", lambda event: button_click(0))

root.bind("+", lambda event: button_action("+"))
root.bind("-", lambda event: button_action("-"))
root.bind("x", lambda event: button_action("x"))
root.bind("*", lambda event: button_action("x"))  # * key as alternative for multiply
root.bind("/", lambda event: button_action("/"))
root.bind("<Return>", lambda event: button_equals())  # Enter key for =
root.bind("c", lambda event: button_clears())

root.mainloop()