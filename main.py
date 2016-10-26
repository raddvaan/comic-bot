from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd
import os
import string
import random
import Levenshtein
import Pmw
import subprocess
import pdb
import time
# import ComicBot as CB
x = 0
versionstring = "V.0.0.3"
root = Tk()
Pmw.initialise(root)
root.wm_iconbitmap('icons\\multiappicon.ico')
root.title("ComicBot" + " - " + versionstring)
DEBUGMODE = 0
DEBUGPATH = 'E:\\Comics\\Ultimate Marvel\\Ultimate Sort'

# subprocess.Popen(r'explorer /select, ' + DEBUGPATH )
# os.system('explorer ' + '"' + DEBUGPATH + '"')


class AppWindow:
    loadicon = PhotoImage(file='icons\\openold26.png')
    loadnewicon = PhotoImage(file='icons\\opennew26.png')
    runicon = PhotoImage(file="icons\\run26.png")
    clearicon = PhotoImage(file="icons\\clear26.png")
    sortdirold = ""
    sortdirnew = ""
    eventdict = {}
    cureventlist = []
    curevent = ""
    isevent = False
    revval = {
        "revo1": False,
        "revo2": False,
        "revn1": False,
        "revn2": False,
        "reve1": False}

    comictypes = [".cbr", ".cbz"]

    renamevar = BooleanVar()
    sortvar = BooleanVar()
    incyearvar = BooleanVar()
    delorigvar = BooleanVar()

    # initj#
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=1000, height=600)
        self.mainwin = Frame(self.master)
        self.mainwin.pack(fill=BOTH, expand=YES)
        self.stitleids = {}
        self.stitleidnum = 0

        self.settypediag = None

        self.topmenu = Menu(self.master)
        self.master.config(menu=self.topmenu)
        self.filemenu = Menu(self.topmenu)
        self.optionmenu = Menu(self.topmenu)
        self.topmenu.add_cascade(label="File", menu=self.filemenu)
        self.topmenu.add_cascade(label="Options", menu=self.optionmenu)
        self.optionmenu.add_command(
            label="Set Filetypes",
            command=self.clear_ftype_choose)
        self.filemenu.add_command(label="Exit", command=self.master.quit)

        self.statusbar = Label(
            self.master,
            text="",
            bd=1,
            relief=SUNKEN,
            anchor=W)

        self.statusbar.pack(
            side=BOTTOM,
            fill=X)

        self.toolframe = Frame(self.mainwin, bd=2)
        self.fileframe = Frame(self.mainwin, bd=1, relief=SUNKEN)

        self.optionframe = Frame(
            self.fileframe,
            width=95,
            bd=2,
            relief=RAISED)
        self.filepanes = PanedWindow(
            self.fileframe,
            orient=HORIZONTAL,
            sashwidth=5,
            bd=1,
            bg="light grey")

        self.option1 = Frame(
            self.optionframe,
            width=100,
            bg='grey',
            relief=SUNKEN)
        self.option2 = Frame(
            self.optionframe,
            width=100,
            bg='grey')
        self.option3 = Frame(
            self.optionframe,
            width=100,
            bg='grey')
        self.option4 = Frame(
            self.optionframe,
            width=100,
            bg='grey')

        self.o1cbf = Frame(self.option1)
        self.o2cbf = Frame(self.option2)
        self.o3cbf = Frame(self.option3)
        self.o4cbf = Frame(self.option4)
        self.o1cb = Checkbutton(
            self.o1cbf,
            bd=1,
            variable=self.renamevar)
        self.o2cb = Checkbutton(
            self.o2cbf,
            bd=1,
            variable=self.sortvar)
        self.o3cb = Checkbutton(
            self.o3cbf,
            bd=1,
            variable=self.incyearvar)
        self.o4cb = Checkbutton(
            self.o4cbf,
            bd=1,
            variable=self.delorigvar)
        self.o1cbl = Label(
            self.o1cbf,
            text="Rename")
        self.o2cbl = Label(
            self.o2cbf,
            text="Sort")
        self.o3cbl = Label(
            self.o3cbf,
            text="Incl. Year")
        self.o4cbl = Label(
            self.o4cbf,
            text="Delete Orig")

        self.option1.pack(fill=X)
        self.option2.pack(fill=X)
        self.option3.pack(fill=X)
        self.option4.pack(fill=X)
        self.o1cbf.pack(fill=BOTH)
        self.o2cbf.pack(fill=BOTH)
        self.o3cbf.pack(fill=BOTH)
        self.o4cbf.pack(fill=BOTH)
        self.o1cb.pack(side=RIGHT)
        self.o2cb.pack(side=RIGHT)
        self.o3cb.pack(side=RIGHT)
        self.o4cb.pack(side=RIGHT)
        self.o1cbl.pack(side=LEFT)
        self.o2cbl.pack(side=LEFT)
        self.o3cbl.pack(side=LEFT)
        self.o4cbl.pack(side=LEFT)
        self.o1cb.select()
        self.o2cb.select()
        self.o4cb.select()

        self.oldwin = Frame(
            self.filepanes,
            bg='grey',
            bd=1,
            width=470)
        self.newwin = Frame(
            self.filepanes,
            bg='grey',
            bd=1)

        self.filepanes.add(self.oldwin)
        self.filepanes.add(self.newwin)
        self.master.bind("<Control-e>", self.kb_shortcuts)

        self.ysbo = ttk.Scrollbar(self.oldwin, orient='vertical')
        self.ysbo.pack(side=RIGHT, fill=Y, expand=NO)
        self.ysbn = ttk.Scrollbar(self.newwin, orient='vertical')
        self.ysbn.pack(side=RIGHT, fill=Y, expand=NO)

        self.oldtree = ttk.Treeview(self.oldwin)
        self.oldtree["columns"] = ("one")
        self.oldtree.column("one", width=50, stretch=FALSE)
        self.oldtree.configure(
            selectmode=EXTENDED,
            yscrollcommand=self.ysbo.set)
        self.ysbo.config(command=self.oldtree.yview)

        self.oldtree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.oldtree.heading(
            "#0",
            text="Comics",
            command=lambda: self.tv_sort("old", "#0", "revo1"))
        self.oldtree.heading(
            "#1",
            text="Files",
            command=lambda: self.tv_sort("old", "Files", "revo2"))
        root.update()

        self.newtree = ttk.Treeview(self.newwin)
        self.newtree["columns"] = ("one")
        self.newtree.column("one", width=50, stretch=FALSE)
        self.newtree.configure(
            selectmode=EXTENDED,
            yscrollcommand=self.ysbn.set)
        self.ysbn.config(command=self.newtree.yview)
        self.newtree.heading("one", text="Files")
        self.newtree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.newtree.heading(
            "#0",
            text="Comics",
            command=lambda: self.tv_sort("new", "#0", "revn1"))
        self.newtree.heading(
            "#1",
            text="Files",
            command=lambda: self.tv_sort("new", "Files", "revn2"))

        self.optionframe.pack(side=LEFT, fill=Y)
        self.filepanes.pack(
            fill=BOTH,
            expand=YES,
            padx=20,
            pady=20,
            side=RIGHT)
        self.toolframe.pack(fill=X)
        self.fileframe.pack(fill=BOTH, expand=YES)

        self.openbasebut = Button(
            self.toolframe,
            image=self.loadicon,
            command=self.open_file_old)
        self.master.bind("<Control-o>", self.kb_shortcuts)
        self.openbasebut.pack(side=LEFT)
        self.opennewbut = Button(
            self.toolframe,
            image=self.loadnewicon,
            command=self.open_file_new)
        self.master.bind("<Control-n>", self.kb_shortcuts)
        self.opennewbut.pack(side=LEFT)
        self.runbut = Button(
            self.toolframe,
            image=self.runicon,
            command=self.run_but)
        self.runbut.pack(side=LEFT)
        self.clearbut = Button(
            self.toolframe,
            image=self.clearicon,
            command=self.clear_all)
        self.clearbut.pack(side=LEFT)

        self.filepanes.sash_place(0, 1000, 0)
        # self.filepanes.paneconfigure(self.newwin, sticky=E)

        root.update()

        self.oldtree.bind('<Double-1>', self.highlight_selection)
        self.newtree.bind('<Double-1>', self.highlight_newtree)
        self.oldtree.bind('<Button-3>', self.old_right_click)
        self.newtree.bind('<Button-3>', self.new_right_click)

        self.conmenu = Menu(self.master)
        self.conmenu.add_command(
            label="Edit Issue",
            command=lambda: self.custom_edit_title("new"))
        self.conmenu.add_command(
            label="Print Tags",
            command=self.print_issue_tags)
        self.conmenold = Menu(self.master)
        self.conmenold.add_command(
            label="Edit Issue",
            command=lambda: self.custom_edit_title("old"))
        self.conmenold.add_command(
            label="Show file in Explorer",
            command=self.open_select_file)

        self.scanbar = ttk.Progressbar(self.statusbar, length=200)
        self.scanbar.pack(side=RIGHT, padx=2, pady=2)
        # tooltips
        self.helpb = Pmw.Balloon(state='balloon', relmouse='both')
        self.helpb.bind(self.runbut, "Tester")
        self.helpb.bind(self.clearbut, "Clear")
        return

    def kb_shortcuts(self, event):

        print(event.keycode)
        event = str(event.keycode)

        self.shortcutdict = {
            "79": self.open_file_old,
            "78": self.open_file_new,
            "69": self.custom_edit_title}

        try:

            self.shortcutdict[event]()

        except:
            return
        return

    def open_file_old(self):

        # pdb.set_trace()
        sumfiles = []
        if DEBUGMODE == 1:
            self.sortdirold = DEBUGPATH
        else:
            self.sortdirold = tkfd.askdirectory()
        self.statusbar.config(text="Scanning...")
        for roots, dirs, files in os.walk(self.sortdirold):
            sumfiles.extend(files)

        tfiles = len(sumfiles)
        apptime = round(tfiles * 0.013)
        self.statusbar.config(
            text="Scanning ~" + str(tfiles) +
            " files. Approx. time " +
            str(apptime) +
            "s")
        # self.sortdirold = self.olddir
        self.clear_tree("old")
        self.clear_tree("new")

        self.scanbar.configure(maximum=tfiles)
        starttime = time.time()
        self.pop_tree("", self.sortdirold)
        # print(self.stitleids)
        self.scanbar.stop()
        endtime = time.time()
        self.statusbar.config(
            text="Done. Processed " +
            str(tfiles) +
            " files in " +
            str(round(endtime - starttime, 2)) +
            "s")

        timetaken = round(endtime - starttime, 2)
        print(timetaken)
        return

    def add_item(self, itemtags):

        return

    def open_file_new(self):
        self.sortdirnew = tkfd.askdirectory()

        return

    def pop_tree(self, parent, path):
        #pdb.set_trace()
        pathlist = os.listdir(path)
        for item in pathlist:
            abspath = os.path.normpath(os.path.join(path, item))
            dircheck = os.path.isdir(abspath)
            if dircheck:
                filecount = len(os.listdir(abspath))
                treein = self.oldtree.insert(
                    parent,
                    "end",
                    text=item,
                    values=[filecount],
                    tags=('dir'))

            else:
                filestatus, filetype = self.type_check(item)
                if filestatus == 'clear':
                    scrubres = self.name_scrub(item, filetype)
                    # dname = scrubres[0]
                    fname = scrubres[0]
                    title = scrubres[1]
                    subtitle = scrubres[2]
                    issue = scrubres[3]
                    event = scrubres[4]
                    volume = scrubres[5]
                    year = scrubres[6]
                    publisher = scrubres[7]
                    filetype = scrubres[8]
                    treein = self.oldtree.insert(
                        parent,
                        "end",
                        text=item,
                        tags="issue")
                    # print(self.newtree.get_children())
                    # print(self.tree_search(title))

                    searchstatus, stitleid = self.tree_search(title)
                    if searchstatus == 'true':
                        curfc = self.newtree.item(stitleid, "values")[0]
                        # print(curfc)
                        curfc = int(curfc) + 1
                        self.newtree.item(stitleid, values=[curfc])
                        treenewi = self.newtree.insert(
                            stitleid,
                            'end',
                            text=fname,
                            iid=treein,
                            tags=(
                                "issue", str(issue),
                                "series", str(title),
                                "volume", volume,
                                "event", event,
                                "year", year,
                                "publisher", publisher,
                                "subtitle", subtitle,
                                "filetype", filetype))
                        self.scanbar.step()
                    elif searchstatus == 'false':
                        seriesid = self.stitle_id_gen(title)
                        treenews = self.newtree.insert(
                            '', 'end',
                            text=title,
                            iid=seriesid,
                            tags=('dir', title),
                            values=[0])

                        treenewi = self.newtree.insert(
                            treenews, 'end',
                            text=fname, iid=treein,
                            tags=(
                                "issue", str(issue),
                                "series", str(title),
                                "volume", volume,
                                "event", event,
                                "year", year,
                                "publisher", publisher,
                                "subtitle", subtitle,
                                "filetype", filetype))

                        self.newtree.item(seriesid, values=[1])

                        self.scanbar.step()

            root.update()
            if dircheck:
                self.pop_tree(treein, abspath)

        return

    def move_item(self, iid):
        series = self.newtree.item(iid, "tags")[3]
        pstatus, newpid = self.tree_search(series)

        if pstatus == "false":
            newpid = self.stitle_id_gen(series)
            self.newtree.insert('', 'end',
                                text=series, iid=newpid,
                                tags=('dir', series))
            self.newtree.move(iid, newpid, 0)
        else:
            self.newtree.move(iid, newpid, 0)
        return

    def tree_search(self, stitle):
        if self.newtree.get_children() == ():
            return 'false', 'blank'
        else:
            status = 'false'
            itemid = ''
            for itemid in self.newtree.get_children():
                if stitle == self.newtree.item(itemid)["text"]:

                    status = 'true'
                    itemid = itemid

                    return status, itemid

                else:
                    status = 'false'
                    itemid = ''

            return status, itemid
        return 'false', 'blank'

    def stitle_id_gen(self, stitle):
        self.stitleidnum += 1
        stitleidhex = hex(self.stitleidnum)
        self.stitleids[stitle] = "ST" + str(stitleidhex)

        return self.stitleids[stitle]

    def clear_all(self):

        self.sortdirnew = ""
        self.sortdirold = ""
        self.oldtree.delete(*self.oldtree.get_children(''))
        self.newtree.delete(*self.newtree.get_children(''))
        return

    def clear_tree(self, treeid):

        for item in self.oldtree.get_children():
            self.oldtree.delete(item)
        for item in self.newtree.get_children():
            self.newtree.delete(item)
            return

    def old_right_click(self, event):
        # element = self.oldtree.identify_row(event.y)
        # self.oldtree.focus(element)
        # self.oldtree.selection_set(element)
        self.conmenold.post(event.x_root, event.y_root)

        return

    def new_right_click(self, event):
        # element = self.newtree.identify_row(event.y)
        # self.newtree.selection_set(element)
        self.conmenu.post(event.x_root, event.y_root)

        return

    def highlight_selection(self, flag):
        fid = self.oldtree.focus()
        print(self.oldtree.item(fid))
        if self.oldtree.tag_has('dir', fid) == 1:
            return
        else:

            self.newtree.selection_set(fid)

            self.newtree.see(fid)

        return

    def open_select_file(self):

        iid = self.oldtree.focus()
        parent = self.oldtree.parent(iid)
        parentList = {}
        compcheck = 0
        counter = 1
        fullpath = self.sortdirold
        # testpath ='E:\\Comics\\Ultimate Marvel\\
        # Ultimate Sort\\1)Marvel Ultimate Universe (2000-2009) - Part 1'
        while compcheck == 0:

            if parent == "":
                # print(counter)
                if counter == 1:
                    print("YES")
                    print(self.oldtree.item(iid, 'text'))
                    parentList[1] = self.oldtree.item(iid, 'text')
                compcheck += 1
            else:

                ptitle = self.oldtree.item(parent, 'text')
                parentList[counter] = ptitle
                parent = self.oldtree.parent(parent)
                counter += 1

        pLength = len(parentList)
        # print('PLENGTH ' + str(pLength))
        # buildcounter = 1
        for item in parentList:
            # print('PLENGTH ' + str(pLength))
            fullpath = fullpath + '/' + parentList[pLength]
            pLength = pLength - 1

        if len(parentList) >= 1:
            fullpath = fullpath + "/" + self.oldtree.item(iid, "text")
        print("FINAL" + fullpath)
        fullpath = os.path.normpath(fullpath)

        subprocess.Popen(r'explorer /select, ' + fullpath)
        return

    def highlight_newtree(self, flag):
        fid = self.newtree.focus()
        if self.newtree.tag_has('dir', fid):
            return
        else:

            self.oldtree.selection_set(fid)
            self.oldtree.see(fid)
        return

    def test_but(self):

        return

    def tv_sort(self, tree, column, reverse):
        treedict = {
            "old": "self.oldtree",
            "new": "self.newtree",
            "edit": "self.sissuestv"}

        children = {}
        stree = eval(treedict[tree])
        rev = self.revval[reverse]

        # print(self.revval[reverse])

        for item in stree.get_children():
            # print(x)
            if column == "#0":
                children[item] = stree.item(item, 'text')
            elif column == "Files":
                children[item] = int(stree.item(item, 'values')[0])

        # print(children.keys())
        childrensort = sorted(
            children.items(),
            key=lambda x: x[1],
            reverse=rev)

        # print(childrensort)
        for item in childrensort:
            stree.move(item[0], "", "end")

        self.revval[reverse] = not self.revval[reverse]
        return

    def run_but(self):

        print(self.sortdirold)
        print(self.sortdirnew)
        return

    def clear_ftype_choose(self):
        if not self.settypediag:

            self.settypediag = Toplevel(
                width=500,
                height=200,
                padx=20,
                pady=20)
            self.settypediag.minsize(width=500, height=200)
            self.settypediag.protocol(
                "WM_DELETE_WINDOW",
                self.set_typediag_none)
            self.settypediag.title("Set acceptable filetypes")

            self.entrylabelf = LabelFrame(
                self.settypediag,
                text="Acceptable filetypes")
            self.entrylabelf.pack(fill=BOTH, expand=YES)
            self.typebox = Frame(self.entrylabelf)
            self.typebox.grid(row=0, column=1, columnspan=5)
            self.typelist = Listbox(self.typebox)
            self.typelist.pack()
            self.newetype = Entry(self.entrylabelf)
            self.newetype.grid(column=1, row=1)
            self.addtypeb = Button(self.entrylabelf, text="+")
            self.addtypeb.grid(column=2, row=1)
            for item in self.comictypes:
                self.typelist.insert(END, item)
            self.typelist.bind("<Double-1>", self.delete_type)
            self.newetype.bind("<Return>", self.add_to_type_list)
            self.addtypeb.bind("<Button-1>", self.add_to_type_list)

        print(self.comictypes)
        return

    def add_to_type_list(self, event):
        newitem = self.newetype.get()
        if newitem in self.typelist.get(0, END):
            self.newetype.delete(0, END)
        else:
            if re.search("\A\.[a-zA-Z]{1,3}$", newitem) is not None:

                self.typelist.insert(END, newitem)
                self.newetype.delete(0, END)
            else:
                self.newetype.delete(0, END)

    def delete_type(self, event):
        fid = self.typelist.curselection()
        self.typelist.delete(fid)

        return

    def set_typediag_none(self):
        self.comictypes = self.typelist.get(0, END)
        self.settypediag.destroy()
        self.settypediag = None
        return

    def print_issue_tags(self):
        stree = self.newtree
        iid = stree.focus()
        print(stree.item(iid, "tags"))
        return

    def custom_edit_title(self, tree):

        self.treedict = {"old": self.oldtree, "new": self.newtree}
        stree = self.treedict[tree]
        selected = list(stree.selection())

        self.seriescheck = BooleanVar()
        self.issuecheck = BooleanVar()
        self.volumecheck = BooleanVar()
        self.eventcheck = BooleanVar()
        self.yearcheck = BooleanVar()
        self.pubcheck = BooleanVar()
        self.subcheck = BooleanVar()
        self.seriescheck.set(1)
        self.issuecheck.set(1)
        self.volumecheck.set(1)
        self.eventcheck.set(1)
        self.yearcheck.set(1)
        self.pubcheck.set(1)
        self.subcheck.set(1)

        self.seriesvar = StringVar()
        self.issuevar = StringVar()
        self.volumevar = StringVar()
        self.eventvar = StringVar()
        self.yearvar = StringVar()
        self.pubvar = StringVar()
        self.subvar = StringVar()

        self.vardict = {
            "self.seriesvar": self.seriescheck,
            "self.issuevar": self.issuecheck,
            "self.volumevar": self.volumecheck,
            "self.eventvar": self.eventcheck,
            "self.yearvar": self.yearcheck,
            "self.pubvar": self.pubcheck,
            "self.subvar": self.subcheck}

        self.edit_box = Toplevel(padx=10, pady=10)
        self.edit_box.lift(aboveThis=None)
        self.editframe = Frame(self.edit_box)
        self.editframe.pack()
        self.navframe = Frame(self.editframe)
        self.navframe.pack(side=TOP)
        self.ilabelf = LabelFrame(self.editframe, width=85, bg="darkgrey")
        self.ilabelf.pack(fill=BOTH, expand=YES)

        self.origtitle = ""
        self.origlabel = Label(self.navframe, text=self.origtitle, width=100)
        self.nextb = Button(self.navframe, text=">")
        self.prevb = Button(self.navframe, text="<")
        self.lbframe = Frame(self.ilabelf, width=20)
        self.lbframe.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.ilbsb = ttk.Scrollbar(self.lbframe, orient='vertical')
        self.sissuestv = ttk.Treeview(
            self.lbframe,
            yscrollcommand=self.ilbsb.set)
        self.sissuestv.heading(
            "#0", text="New Name",
            command=lambda: self.tv_sort("edit", "#0", "reve1"))

        self.ilbsb.config(command=self.sissuestv.yview)
        self.infof = Frame(self.ilabelf, bd=10)

        self.dirlist = []
        self.issuedict = {}

        self.sissuestv.pack(side=LEFT, fill=BOTH, expand=YES)
        self.ilbsb.pack(side=RIGHT, fill=Y, )

        self.prevb.pack(side=LEFT)
        self.origlabel.pack(side=LEFT)
        self.nextb.pack(side=RIGHT)
        self.infof.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.seriesL = Label(self.infof, text="Series")
        self.seriesL.grid(row=1, column=1)

        self.seriesCb = Checkbutton(
            self.infof, bd=1, variable=self.seriescheck)
        self.seriesCb.grid(row=1)

        self.seriesE = Entry(self.infof, width=40, textvariable=self.seriesvar)
        self.seriesE.grid(row=1, column=2)

        self.issueL = Label(self.infof, text="Issue")
        self.issueL.grid(row=2, column=1)

        self.issueCb = Checkbutton(self.infof, bd=1, variable=self.issuecheck)
        self.issueCb.grid(row=2)

        self.issueE = Entry(self.infof, width=40, textvariable=self.issuevar)
        self.issueE.grid(row=2, column=2)

        self.volumeL = Label(self.infof, text="Volume")
        self.volumeL.grid(row=3, column=1)

        self.volumeCb = Checkbutton(
            self.infof, bd=1, variable=self.volumecheck)
        self.volumeCb.grid(row=3)

        self.volumeE = Entry(self.infof, width=40, textvariable=self.volumevar)
        self.volumeE.grid(row=3, column=2)

        # self.eventL = Label(self.infof, text="Event")
        # self.issueL.grid(row=2)

        # self.eventE = Entry(self.infof, width=40)
        # self.issueE.grid(row=4, column=2)

        self.yearL = Label(self.infof, text="Year")
        self.yearL.grid(row=4, column=1)

        self.yearCb = Checkbutton(self.infof, bd=1, variable=self.yearcheck)
        self.yearCb.grid(row=4)

        self.yearE = Entry(self.infof, width=40, textvariable=self.yearvar)
        self.yearE.grid(row=4, column=2)

        self.publisherL = Label(self.infof, text="Publisher")
        self.publisherL.grid(row=5, column=1)

        self.publisherCb = Checkbutton(
            self.infof, bd=1, variable=self.pubcheck)
        self.publisherCb.grid(row=5)

        self.publisherE = Entry(self.infof, width=40, textvariable=self.pubvar)
        self.publisherE.grid(row=5, column=2)

        self.subtitleL = Label(self.infof, text="Subtitle")
        self.subtitleL.grid(row=6, column=1)

        self.subtitleCb = Checkbutton(
            self.infof, bd=1,
            variable=self.subcheck,
            command=self.print_values)

        self.subtitleCb.grid(row=6)

        self.subtitleE = Entry(self.infof, width=40, textvariable=self.subvar)
        self.subtitleE.grid(row=6, column=2)
        self.volumevar.trace("w", self.update_checks)
        self.seriesvar.trace("w", self.update_checks)
        self.issuevar.trace("w", self.update_checks)
        self.pubvar.trace("w", self.update_checks)
        self.subvar.trace("w", self.update_checks)
        self.yearvar.trace("w", self.update_checks)
        self.eventvar.trace("w", self.update_checks)

        self.eventf = LabelFrame(self.infof, text="Event")

        self.updateB = Button(
            self.infof, text="Update", command=self.update_preview)
        self.updateB.grid(row=8, column=2, sticky=E)

        self.saveB = Button(self.edit_box, text="Save")
        self.saveB.pack(side=RIGHT)
        self.populate_edit_screen(selected, tree)

        return

    def populate_edit_screen(self, selected, tree):
        self.dirlist = []
        self.issuedict = {}
        self.sissuestv.delete(*self.sissuestv.get_children())

        stree = self.treedict[tree]
        self.gather_dirs(selected, "self.dirlist", tree)
        iid = selected[0]

        pid = stree.parent(iid)
        # print(self.dirlist)

        if self.dirlist != []:

            self.gather_issues(self.dirlist, "self.issuedict", 1)
        else:
            self.gather_issues(selected, "self.issuedict", 0)

        issuekeys = list(self.issuedict.keys())
        firstiss = issuekeys[0]
        self.nextb.config(
            command=lambda: self.browse_buttons(firstiss, "next", tree))
        self.prevb.config(
            command=lambda: self.browse_buttons(firstiss, "prev", tree))
        tagtuple = self.get_tags(firstiss)
        curissue = tagtuple[0]
        curseries = tagtuple[1]
        curvol = tagtuple[2]
        curevent = tagtuple[3]
        curyear = tagtuple[4]
        curpub = tagtuple[5]
        cursub = tagtuple[6]

        tagdict = {
            "issue": curissue,
            "series": curseries,
            "volume": curvol,
            "event": curevent,
            "year": curyear,
            "publisher": curpub,
            "subtitle": cursub}
        alternate = False
        coldict = {False: "#f2f3f4", True: "white"}

        for key, value in self.issuedict.items():
            itemtags = self.get_tags(key)
            i_issue = itemtags[0]
            i_series = itemtags[1]
            i_vol = itemtags[2]
            i_event = itemtags[3]
            i_year = itemtags[4]
            i_pub = itemtags[5]
            i_sub = itemtags[6]

            if i_issue != curissue:
                self.issuecheck.set(0)

                curissue = ""
            if i_series != curseries:
                curseries = ""
                self.seriescheck.set(0)
            if i_vol != curvol:
                curvol = ""
                self.seriescheck.set(0)
            if i_event != curevent:
                curevent = ""
            if i_year != curyear:
                curyear = ""
                self.yearcheck.set(0)
            if i_pub != curpub:
                curpub = ""
                self.pubcheck.set(0)
            if i_sub != cursub:
                cursub = ""
                self.subcheck.set(0)
            additem = self.sissuestv.insert(
                "", 'end', text=value, iid=key,
                tags=self.newtree.item(key, "tags"))

            self.sissuestv.itemconfig(0, bg=coldict[alternate])
            alternate = not alternate
        self.multissues = 0

        if len(issuekeys) > 1:
            self.multissues = 1
            self.origtitle = "Multiple Files"
        else:
            self.origtitle = stree.item(issuekeys[0], 'text')

        self.origlabel.configure(text=self.origtitle)

        if self.issuecheck.get() == 0:
            self.issueCb.config(state=DISABLED)

        for key, value in self.vardict.items():
            key = eval(key).get()
            # print("KEY + " + key)
            if key == "":
                value.set(0)
        self.saveB.config(
            command=lambda: self.save_edits(iid, pid, self.issuedict))

        self.seriesE.delete(0, END)
        self.issueE.delete(0, END)
        self.volumeE.delete(0, END)
        # self.eventE.delete(0, END)
        self.yearE.delete(0, END)
        self.publisherE.delete(0, END)
        self.subtitleE.delete(0, END)

        self.seriesE.insert(0, str(curseries))
        self.issueE.insert(0, str(curissue))
        self.volumeE.insert(0, str(curvol))
        # self.eventE.insert(0, str(curevent))
        self.yearE.insert(0, str(curyear))
        self.publisherE.insert(0, str(curpub))
        self.subtitleE.insert(0, str(cursub))

        return tagtuple

    def update_checks(self, *args):
        for key, value in self.vardict.items():
            onval = 1
            if key == "self.issuevar":
                if self.multissues == 1:
                    onval = 0
            key = eval(key).get()
            if key != "":

                value.set(onval)
            else:
                value.set(0)

    def browse_buttons(self, iid, direct, tree):

        advdict = {"next": self.oldtree.next, "prev": self.oldtree.prev}
        newitem = advdict[direct](iid)
        print("NEWITEM " + newitem)
        if newitem == "":
            return
        self.populate_edit_screen([newitem], tree)
        # print(advdict[direct](iid))B
        # print(self.oldtree.index(iid))
        return

    def update_preview(self):
        stree = self.sissuestv

        for item in stree.get_children(""):
            streeTags = stree.item(item, "tags")

            seriesCheckD = {0: streeTags[3], 1: self.seriesvar.get()}
            issueCheckD = {0: streeTags[1], 1: self.issuevar.get()}
            volumeCheckD = {0: streeTags[5], 1: self.volumevar.get()}
            yearCheckD = {0: streeTags[9], 1: self.yearvar.get()}
            pubCheckD = {0: streeTags[11], 1: self.pubvar.get()}
            subCheckD = {0: streeTags[13], 1: self.subvar.get()}
            newTags = (
                "issue", issueCheckD[self.issuecheck.get()],
                "series", seriesCheckD[self.seriescheck.get()],
                "volume", volumeCheckD[self.volumecheck.get()],
                "event", "",
                "year", yearCheckD[self.yearcheck.get()],
                "publisher", pubCheckD[self.pubcheck.get()],
                "subtitle", subCheckD[self.subcheck.get()],
                "filetype", streeTags[15])

            newname = self.name_builder(
                newTags[3], newTags[13],
                newTags[5], newTags[1],
                newTags[9], newTags[15])

            stree.item(item, text=newname, tags=newTags)

    def print_values(self):
        print(self.seriescheck.get())
        print(self.issuecheck.get())
        return

    def gather_dirs(self, selected, varilist, tree):
        stree = self.treedict[tree]
        dirlist = eval(varilist)

        for item in selected:

            if stree.item(item, 'tags')[0] == 'dir':
                dirlist.insert(0, item)
                for item in stree.get_children(item):

                    self.gather_dirs([item], varilist, tree)
        return

    def gather_issues(self, dirs, varidict, hasdirs):
        idict = eval(varidict)
        for item in dirs:
            if hasdirs == 1:

                children = self.oldtree.get_children(item)
            else:
                children = dirs
            for child in children:
                if self.oldtree.item(child, "tags")[0] != 'dir':

                    childtags = self.newtree.item(child, 'tags')

                    idict[child] = self.newtree.item(child, 'text')

        return

    def save_edits(self, iid, pid, issuedict):
        stree = self.sissuestv
        newtree = self.newtree
        for item in stree.get_children(""):
            pid = newtree.parent(item)
            newtree.item(
                item, tags=stree.item(item, "tags"),
                text=stree.item(item, "text"))
            self.move_item(item)
            self.clear_empty(pid)

        return

    def clear_empty(self, pid):
        ntree = self.newtree
        if ntree.tag_has("dir", pid):
            if ntree.get_children(pid) == ():
                ntree.delete(pid)
        return

    def get_tags(self, iid):
        tags = self.newtree.item(iid, "tags")
        tagtuple = (
            tags[1], tags[3],
            tags[5], tags[7],
            tags[9], tags[11],
            tags[13])

        if tags[0] == "dir":
            return "dir", tags[1]
        else:
            return tagtuple





##########################################################    
##########################################################
######   ########################################   ######
######   ########    ALGORITHMS FOR SORT   ######   ######
######   ########################################   ######
######   ########################################   ######
####       ####################################       ####
#####     ########   BELOW THIS BLOCK   ########     #####
######   ########################################   ######
####### ########################################## #######
##########################################################






    # def comic_finder(self, comicTitle, comicYear): #searches known databeses
    #     if comicYear == "0000":
    #         year = year_prompt(comicTitle)
    #     else:
    #         year = comicYear
    #     cdburl = "http://www.comicbookdb.com/search.php?form_search=" + str(comicTitle) + " " + year + "&form_searchtype=Title"
    #     cdburl2 = "http://www.comicbookdb.com/title.php?ID=348"
    #     source_code = requests.get(cdburl)
    #     plain_text = source_code.text
    #     soup = BeautifulSoup(plain_text, "html.parser")
    #     for link in soup.find_all('a', href=re.compile('title.php?')):
    #         print(link.string)

    def name_scrub(self, dname, filetype):
        print("DNAME=" + dname)
        self.incyear = self.incyearvar.get()

        strippedname = re.sub(filetype, "", dname)
        strippedname = re.sub("[\%\_\^]", " ", strippedname)
        strippedname = strippedname.replace("#", "")
        strippedname

        strippedname, isevent, eiss, etitle = self.event_handler(strippedname)

        issyr, strippedname = self.year_cracker(strippedname)

        volume, strippedname = self.volume_finder(strippedname)
        print("STRIPPEDNAME " + strippedname)
        badchars = True
        # pdb.set_trace()

        issue, strippedname = self.issue_cracker(strippedname)
        while badchars is True:
            charsearch = re.search("\A\s|-$|\s$", strippedname)
            if charsearch is not None:
                print(charsearch)
                strippedname = re.sub("\A\s|-$|\s$", "", strippedname)
            else:
                badchars = False

            print(charsearch)

        print("OKAY")
        print(strippedname)
        # title, subtitle = self.subtitle_scraper(
        #    strippedname, strippedname, issue, strippedname)

        title = self.title_cracker(strippedname)
        print(title)

        title, subtitle = self.subtitle_scraper(
            strippedname, strippedname, issue, title)
        print(subtitle)

        if subtitle == "false":
            subtitle = ""
        else:
            title = title.replace(subtitle, "")

        fname = self.name_builder(
            title, subtitle, volume, issue, issyr, filetype)
        print(fname)
        return fname, title, subtitle, issue, etitle, volume, issyr, "", filetype 

    def name_builder(self, series, subtitle, volume, issue, issyr, filetype):

        if issyr == "":
            year = ""
        else:
            if self.incyear:
                year = " (" + issyr + ")"
            else:
                year = ""

        if subtitle != "":
            subtitle = " - " + subtitle
        if volume != "":
            voliss = volume + " " + issue
        else:
            voliss = volume + issue
        fname = series + subtitle + " - " + voliss + year + filetype

        return fname

    def event_handler(self, dname):
        # pdb.set_trace()

        eviss = re.search(
            "\A\d{1, 3}(\.\d{1,2})?[\s]-?", dname)

        if eviss is not None:
            eviss = eviss.group(0)
            namenoevent = re.sub(eviss, "", dname)

            self.isevent = True
            self.notitle = True

            self.cureventlist.append(dname)
            if self.curevent == "":
                evtitle = tksd.askstring("Event Detected", "Event Title?")
                self.curevent = evtitle
            else:
                evtitle = self.curevent

            # while self.notitle == True:
            #     x = 1

            # namenoevent = dname[re.search("\A\d{1,3}[\s-]", dname).span()[1]:len(dname)]

            # eviss = re.sub("\D", "", eviss)
            return namenoevent, self.isevent, eviss, evtitle
        else:
            if self.cureventlist != []:
                self.eventdict[self.curevent] = self.cureventlist
                self.cureventlist = []
            self.isevent = False

            return dname, False, "", ""

        namenoevent = dname
        evtitle = "ASS"

        return namenoevent, self.isevent, eviss, evtitle

    def ask_event_title(self, dname):
        askwin = Toplevel()

        return "title"

    def scan_folder(self, location):

        for root, dirs, files in os.walk(location):
            sub = root

            for file in os.listdir(sub):
                try:

                    # pdb.set_trace()
                    filestatus, filetype = type_check(file)

                    print(filetype)
                    if filestatus == "clear":

                        scrubname = name_scrub(file, filetype)
                    #    print('sname')
                    #    print(scrubname)
                        if scrubname == "false":
                            newname, namescrap = name_scrub(file, filetype)

                        else:
                            # print("else")
                            foldertitle, newname = name_scrub(file, filetype)

                        if location == marvelSort:
                            newloc = newmarvel
                        elif location == dcSort:
                            newloc = newdc
                        elif location == ultSort:
                            newloc = newult

                        move_file(file, newname, foldertitle, sub, newloc)
                except:
                    print("EXCEPT")

        return

    def move_file(
            self, oldfilename,
            newfilename, title,
            oldlocation, newlocation):

        print(oldfilename, newfilename, title, oldlocation, newlocation)
        return

    def issue_cracker(self, dname):

        try:

            issue = str(re.search(
                "[#\)\s][0-9]{1,3}?(\.\d)?([\(\s-]|$)|"
                "TPB|\s?Annual([#\)\s][0-9]{1,3})*",
                dname).group(0))
            issin = dname.index(issue)
            namenoiss = dname[0:issin]
            badchars = True

            while badchars is True:
                charsearch = re.search("\A\s|-|\s$|\(|\)|#", issue)
                if charsearch is not None:
                    print(charsearch)
                    issue = re.sub("\A\s|-|\s$|\(|\)|#", "", issue)
                else:
                    badchars = False

        except:
            issue = "(One Shot)"
            namenoiss = dname

        while len(issue) < 3:
            issue = "0" + issue

        return issue, namenoiss

    def title_cracker(self, dname):
        # print(dname)
        title = dname
        return title

    def year_cracker(self, dname):
        try:
            # print(dname)
            issyr = re.search(
                '[\(\s]195\d[\s\)]|[\(\s]19[6-9]\d[\s\)]'
                '|[\(\s]20[0-3]\d[\s\)]|[\(\s]2040[\s\)]',
                dname).group(0)
            namenoyear = dname.replace(issyr, "")
            # print(namenoyear)
            issyr = issyr.replace("(", "").replace(")", "").replace(" ", "")
            # print(issyr)

        except:
            issyr = ""
            namenoyear = dname

        return issyr, namenoyear

    def type_check(self, file):
        filetype = re.search("\.[a-zA-Z]{2,4}$", file)
        # print(filetype)
        if filetype.group(0) in self.comictypes:
            status = "clear"

        else:
            status = "skip"
        return status, filetype.group(0)

    def volume_finder(self, dname):

        try:
            volobj = re.search("\s?v(ol)?\s?\d{1,2}", dname, re.IGNORECASE)
            volume = volobj.group(0)
            

            volumeno = re.search("\d{1,2}", volume).group(0)
            # print(volumeno)
            if len(volumeno) == 2:
                volume = "V" + volumeno
            else:
                volume = "V0" + volumeno
            namenovol = re.sub(volobj.group(0), "", dname)
            print("NOVOL" + namenovol)
            volume = re.sub(" ","",volume)
            

            return volume, namenovol
        except:
            volume = ""
            namenovol = dname

            # print(volume)
            return volume, namenovol

    def subtitle_scraper(self, strippedname, dname, issue, title):
        try:

            dashfind = re.search(" - ", dname).span()[0]
            issuein = re.search(issue, dname).span()[0] - 1
            subtitle = dname[dashfind:issuein]
            # print(subtitle)
            ctitle = re.sub(subtitle, "", title)

        except:
            ctitle = title
            subtitle = "false"
        # print("TITLE " + ctitle)
        # print("SUB " + subtitle)
        return ctitle, subtitle

    def DEBUGFILES(self):
        self.pop_tree("", DEBUGPATH)
        return

appwin = AppWindow(root)

if DEBUGMODE == 1:
    appwin.open_file_old()

root.mainloop()
print("EXIT")
