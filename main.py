from tkinter import *
import apiutil as api
import html

root = Tk()
root.title('MagaDek')
root.resizable(0,0)

root.rowconfigure(2, weight=1)

pagenum = 1

Label(root, text='Search MangaDex').grid(columnspan=2, sticky=W)

def on_search():
    xcounter = 0
    ycounter = 0

    global pagenum
    pagenum = 1

    # Clear previous results

    def all_children(window):
        _list = window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        return _list
    
    button_list = all_children(results)
    for i in button_list:
        i.destroy()

    def result_assign(l, ltaglist, b):
        title.configure(text=l.title)
        status.configure(text=l.status)
        tags.configure(text=', '.join(ltaglist))
        desc.configure(text=html.unescape(l.description['en']))

        button_list = all_children(results)
        for i in button_list:
            i['relief'] = RAISED
        
        b['relief'] = GROOVE

    # Fill with new buttons

    try: api.get_manga(search.get())
    except: Label(results, text=f'"{search.get()}" gave no results :(').grid(padx=2, pady=2)
    else:
        for i in api.get_manga(search.get()):
            if xcounter == 5:
                xcounter = 0
                ycounter += 1
            
            taglist = []
            for j in i.tags:
                taglist.append(j['attributes']['name']['en'])
            
            manga_opt = Button(results, text=i.title, height=8, width=15, wraplength=100, borderwidth=4)
            manga_opt['command'] = lambda i=i, b=manga_opt:result_assign(i, taglist, b)
            manga_opt.grid(row=ycounter, column=xcounter, padx=5, pady=5)

            if xcounter + ycounter * 5 == 19:
                break
            
            xcounter += 1

search = Entry(root, borderwidth=3)
search.grid(row=1, column=0, padx=2, pady=5, ipadx=2, ipady=2, sticky=EW)

Button(root, text='Search', command=on_search, borderwidth=3).grid(row=1, column=1, padx=2, pady=2, sticky=EW)

display = LabelFrame(root, text='Info', relief=SUNKEN, width=450, height=630)
display.grid(row=2, column=1, rowspan=3, padx=2, pady=2, sticky=NSEW)
display.grid_propagate(0)

def tags_extend():
    view = Tk()
    view.title('Tags')
    view.resizable(0,0)
    Label(view, text=tags.cget('text'), relief=SUNKEN, width=40, wraplength=280, anchor=W, justify=LEFT).pack(padx=5, pady=5, ipadx=5, ipady=5)

def desc_extend():
    view = Tk()
    view.title('Description')
    view.resizable(0,0)
    Label(view, text=desc.cget('text'), relief=SUNKEN, width=100, wraplength=700, anchor=W, justify=LEFT).pack(padx=5, pady=5, ipadx=5, ipady=5)

Label(display, text='Title:').grid(row=0, column=0, padx=5, pady=5, sticky=NW)
Label(display, text='Status:').grid(row=1, column=0, padx=5, pady=5, sticky=NW)
Button(display, text='Tags:', relief=GROOVE, command=tags_extend, borderwidth=3).grid(row=2, column=0, padx=5, pady=5, sticky=NW)
Button(display, text='Description:', relief=GROOVE, command=desc_extend, borderwidth=3).grid(row=3, column=0, padx=5, pady=5, sticky=NW)

title = Label(display, anchor=W, justify=LEFT, wraplength=350)
status = Label(display, anchor=W, justify=LEFT, wraplength=350)
tags = Label(display, anchor=W, justify=LEFT, wraplength=350)
desc = Label(display, anchor=W, justify=LEFT, wraplength=350)

title.grid(row=0, column=1, pady=5, sticky=NSEW)
status.grid(row=1, column=1, pady=5, sticky=NSEW)
tags.grid(row=2, column=1, pady=5, sticky=NSEW)
desc.grid(row=3, column=1, pady=5, sticky=NSEW)

# title.configure(text='Insert selected text here')

results = LabelFrame(root, text='Search Results', relief=SUNKEN, width=650)
results.grid(row=2, padx=2, pady=2, sticky=NSEW)
results.grid_propagate(0)

navigate = Frame(root)
navigate.grid(row=3, column=0, sticky=EW)
navigate.columnconfigure(0, weight=1)
navigate.columnconfigure(1, weight=1)
navigate.columnconfigure(2, weight=1)

Button(navigate, text='Previous').grid(row=0, column=0, padx=2, pady=2, sticky=EW)
Button(navigate, text='Next').grid(row=0, column=2, padx=2, pady=2, sticky=EW)

pagenav = Label(navigate, text='Page 1/1')
pagenav.grid(row=0, column=1, padx=2, pady=2, sticky=EW)

root.mainloop()