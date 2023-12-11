from tkinter import *
import ARMflames.Split as sp
import ARMflames.FLAMES as fl


def UI():
    root=Tk()
    root.title("ARMflames")
    root.geometry("+300+100")
    root.geometry("700x500")

    def Predict():
        tk1=Toplevel()
        tk1.geometry("+300+100")
        tk1.geometry("700x70")
        r=fl.times(sp.setnames(ne1.get(),ne2.get()))
        l=Label(tk1,text=r,font=("Arial Bold",30),bg="yellow",fg="red")
        l.pack()
    
    hd=Label(root,text="ARMflames Game",font=("Arial Bold",40))
    n1=Label(root,text="Enter The First Person Name:",font=("Arial Bold",11))
    n2=Label(root,text="Enter The Second Person Name:",font=("Arial Bold",11))


    ne1=Entry(root,width=30,font=("Arial",11),
              fg="blue",
              border=5,
              textvariable="name1")
    ne1.insert(0,"Abdur Rahim")

    ne2=Entry(root,width=30,font=("Arial",11),
              fg="blue",
              textvariable="name2")
    ne2.insert(0,"Abinaya")

    pd=Button(root,text="Predict",width=70,command=Predict,
              activebackground='Yellow',
              activeforeground='red')

    #hd.grid(row=1,columnspan=3)
    hd.place(x=120,y=80)

    n1.place(x=120,y=200)
    n2.place(x=120,y=250)


    ne1.place(x=380,y=200)
    ne2.place(x=380,y=250)

    pd.place(x=120,y=300)

    root.mainloop()
    
if __name__=='__main__':
    UI()


