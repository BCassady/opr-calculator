from distutils.command.build import build
from pickletools import read_long1
from re import L
import tkinter as tk
from tkinter import ttk
import numpy as np 
 
LARGEFONT =("Verdana", 35)

global teams
teams = []
matches = []
oprs = []



  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text ="Home Page", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.place(x=640, y=20, anchor="center") 
  
        button1 = ttk.Button(self, text ="Add/Edit Teams",
        command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = (50, 25))
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Add/Edit Matches",
        command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 25)

        def build_table():
            game_scroll = tk.Scrollbar(self)
            table = ttk.Treeview(self,yscrollcommand=game_scroll.set)
            table.place(x=640, y=300, anchor="center")
            game_scroll.config(command=table.yview)

            table['columns'] = ('rank', 'team_number', 'opr')

            table.column("#0", width=0,  stretch=tk.NO)
            table.column("rank",anchor="center", width=80)
            table.column("team_number",anchor="center",width=80)
            table.column("opr",anchor="center",width=80)

            table.heading("#0",text="",anchor="center")
            table.heading("rank",text="Rank",anchor="center")
            table.heading("team_number",text="Number",anchor="center")
            table.heading("opr",text="OPR",anchor="center")

            for i in range(len(oprs)):
                table.insert(parent='',index='end',iid=i,text='',
                    values=(str(i+1),oprs[i][0],oprs[i][1]))

        def calculate():
            try:

                team_num = len(teams)
                match_num = len(matches)
                index_team = {}
                team_index = {}

                i = 0
                for row in range(team_num):
                    team = teams[row]
                    team_index[int(team)] = i
                    index_team[i] = int(team)
                    i += 1

                mat = [[0]*team_num for _ in range(team_num)]
                s = [0 for _ in range(team_num)]
                
                for row in range(match_num):
                    
                    team0 = team_index[int(matches[row][0])]
                    team1 = team_index[int(matches[row][1])]
                    team2 = team_index[int(matches[row][2])]
                    team3 = team_index[int(matches[row][3])]

                    mat[team0][team0] += 1
                    mat[team1][team1] += 1
                    mat[team2][team2] += 1
                    mat[team3][team3] += 1

                    mat[team0][team1] += 1
                    mat[team1][team0] += 1
                    mat[team2][team3] += 1
                    mat[team3][team2] += 1

                    s[team0] += int(matches[row][4])
                    s[team1] += int(matches[row][4])
                    s[team2] += int(matches[row][5])
                    s[team3] += int(matches[row][5])

                p = np.linalg.solve(mat, s)
                
                global oprs

                while(len(oprs)>0):
                    oprs.pop()

                for i in range(team_num):
                    curr_team = index_team[i]
                    oprs.append((curr_team, round(p[i], 2)))

                oprs.sort(key = lambda x: x[1])

                oprs = oprs[::-1]
                
                build_table()
            except Exception as e:
                print("Check for missing teams: " + str(e))

        build_table()

        calc = ttk.Button(self, text ="Calculate OPRs",
        command = calculate)
        calc.place(x=640, y=420, anchor="center")

        out_name = tk.Entry(self, font=('calibre',10,'normal'))
        in_name = tk.Entry(self, font=('calibre',10,'normal')) 

        def save():
            f = open(out_name.get() + "-teams" + ".txt", "a")
            for team in teams:
                f.write(team + "\n")
            f.close()

            f = open(out_name.get() + "-matches" + ".txt", "a")
            for match in matches: 
                line = ""
                for item in match:
                    line += item + ", "
                line = line[:-2]
                f.write(line+ "\n")
            f.close

        def load():
            teams.clear()
            matches.clear()

            f = open(in_name.get() + "-teams" + ".txt", "r")
            for line in f.readlines():
                teams.append(line)
            f.close()
            f = open(in_name.get() + "-matches" + ".txt", "r")
            for line in f.readlines():
                line = line.split(', ')
                matches.append(line)
            f.close()
            calculate()

        save_file = ttk.Button(self, text ="Save As", command = save) 
        load_file = ttk.Button(self, text ="Load From", command = load) 

        out_name.place(x=940, y=390, anchor="center")
        in_name.place(x=360, y=390, anchor="center")
        save_file.place(x=940, y=420, anchor="center")
        load_file.place(x=360, y=420, anchor="center")

            
        
  
  
# second window frame page1
class Page1(tk.Frame):

    def make_table_2(self):

        game_scroll = tk.Scrollbar(self)
        table = ttk.Treeview(self,yscrollcommand=game_scroll.set)
        table.place(x=640, y=500, anchor="center")
        game_scroll.config(command=table.yview)

        table['columns'] = ('team_number')

        table.column("#0", width=0,  stretch=tk.NO)
        table.column("team_number",anchor="center", width=80)

        table.heading("#0",text="",anchor="center")
        table.heading("team_number",text="Team Number",anchor="center")

        for i, team in enumerate(teams):
            table.insert(parent='',index='end',iid=i,text='',
                values=(team))

    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

        label = ttk.Label(self, text ="Teams", font = LARGEFONT)
        label.place(x=640, y=20, anchor="center") 
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Go home",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = (50, 25))
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Add/Edit Matches",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 25)

        team_add_entry = tk.Entry(self, font=('calibre',10,'normal'))

        team_remove_entry = tk.Entry(self, font=('calibre',10,'normal'))

        def make_table():

            game_scroll = tk.Scrollbar(self)
            table = ttk.Treeview(self,yscrollcommand=game_scroll.set)
            table.place(x=640, y=500, anchor="center")
            game_scroll.config(command=table.yview)

            table['columns'] = ('team_number')

            table.column("#0", width=0,  stretch=tk.NO)
            table.column("team_number",anchor="center", width=80)

            table.heading("#0",text="",anchor="center")
            table.heading("team_number",text="Team Number",anchor="center")

            for i, team in enumerate(teams):
                table.insert(parent='',index='end',iid=i,text='',
                    values=(team))

        def addTeam():
            if team_add_entry.get() not in teams:
                teams.append(team_add_entry.get())
                teams.sort(key = int)
                make_table()

        def removeTeam():
            if team_remove_entry.get() in teams:
                teams.remove(team_remove_entry.get())
                self.make_table() 

        sub_add_btn=tk.Button(self, text = 'Add Team', command = addTeam)
        sub_rmv_btn=tk.Button(self, text = 'Remove Team', command = removeTeam)

        team_add_entry.grid(row=2, column=2, padx=210)
        sub_add_btn.grid(row=3, column=2)
        team_remove_entry.grid(row=2, column=5)
        sub_rmv_btn.grid(row=3, column=5)
        make_table()

    def on_show_frame(self, event):
        self.make_table_2()

  
# third window frame page2
class Page2(tk.Frame):

    def make_table_2(self):

        game_scroll = tk.Scrollbar(self)
        table = ttk.Treeview(self,yscrollcommand=game_scroll.set)
        table.place(x=640, y=500, anchor="center")
        game_scroll.config(command=table.yview)

        table['columns'] = ('match_number', 'red_1', 'red_2', 'blue_1', 'blue_2', 'red_score', 'blue_score')

        table.column("#0", width=0,  stretch=tk.NO)
        table.column("match_number",anchor="center", width=80)
        table.column("red_1",anchor="center", width=80)
        table.column("red_2",anchor="center", width=80)
        table.column("blue_1",anchor="center", width=80)
        table.column("blue_2",anchor="center", width=80)
        table.column("red_score",anchor="center", width=80)
        table.column("blue_score",anchor="center", width=80)

        table.heading("#0",text="",anchor="center")
        table.heading("match_number",text="Match",anchor="center")
        table.heading("red_1",text="Red 1",anchor="center")
        table.heading("red_2",text="Red 2",anchor="center")
        table.heading("blue_1",text="Blue 1",anchor="center")
        table.heading("blue_2",text="Blue 2",anchor="center")
        table.heading("red_score",text="Red Score",anchor="center")
        table.heading("blue_score",text="Blue Score",anchor="center")

        for i, match in enumerate(matches):
            table.insert(parent='',index='end',iid=i,text='',
                values=(i+1, match[0], match[1], match[2], match[3], match[4], match[5]))

    def on_show_frame(self, event):
        self.make_table_2()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

        label = ttk.Label(self, text ="Matches", font = LARGEFONT)
        label.place(x=640, y=20, anchor="center")
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Add/Edit Teams",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = (50, 25))
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Go home",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 25)

        match_team0 = tk.Entry(self, font=('calibre',10,'normal'))
        match_team1 = tk.Entry(self, font=('calibre',10,'normal'))
        match_team2 = tk.Entry(self, font=('calibre',10,'normal'))
        match_team3 = tk.Entry(self, font=('calibre',10,'normal'))
        score_red = tk.Entry(self, font=('calibre',10,'normal'))
        score_blue = tk.Entry(self, font=('calibre',10,'normal'))

        edit = tk.Entry(self, font=('calibre',10,'normal')) 

        def make_table():

            game_scroll = tk.Scrollbar(self)
            table = ttk.Treeview(self,yscrollcommand=game_scroll.set)
            table.place(x=640, y=500, anchor="center")
            game_scroll.config(command=table.yview)

            table['columns'] = ('match_number', 'red_1', 'red_2', 'blue_1', 'blue_2', 'red_score', 'blue_score')

            table.column("#0", width=0,  stretch=tk.NO)
            table.column("match_number",anchor="center", width=80)
            table.column("red_1",anchor="center", width=80)
            table.column("red_2",anchor="center", width=80)
            table.column("blue_1",anchor="center", width=80)
            table.column("blue_2",anchor="center", width=80)
            table.column("red_score",anchor="center", width=80)
            table.column("blue_score",anchor="center", width=80)

            table.heading("#0",text="",anchor="center")
            table.heading("match_number",text="Match",anchor="center")
            table.heading("red_1",text="Red 1",anchor="center")
            table.heading("red_2",text="Red 2",anchor="center")
            table.heading("blue_1",text="Blue 1",anchor="center")
            table.heading("blue_2",text="Blue 2",anchor="center")
            table.heading("red_score",text="Red Score",anchor="center")
            table.heading("blue_score",text="Blue Score",anchor="center")

            for i, match in enumerate(matches):
                table.insert(parent='',index='end',iid=i,text='',
                    values=(i+1, match[0], match[1], match[2], match[3], match[4], match[5]))
  

        def addMatch():
            matches.append([match_team0.get(), match_team1.get(), match_team2.get(), match_team3.get(), score_red.get(), score_blue.get()])
            make_table()

        def removeMatch():
            matches.remove(matches[-1])
            make_table()

        def editMatch():
            matches[int(edit.get())-1] = [match_team0.get(), match_team1.get(), match_team2.get(), match_team3.get(), score_red.get(), score_blue.get()]
            make_table() 

        sub_add_btn=tk.Button(self, text = 'Add Match', command = addMatch)
        sub_rmv_btn=tk.Button(self, text = 'Remove Last Match', command = removeMatch)
        sub_edt_btn=tk.Button(self, text = 'Edit Match ID:', command = editMatch)

        match_team0.grid(row=2, column=2, padx=5, sticky="n")
        match_team1.grid(row=2, column=3, padx=5, sticky="n")
        match_team2.grid(row=2, column=4, padx=5, sticky="n")
        match_team3.grid(row=2, column=5, padx=5, sticky="n")
        score_red.grid(row=2, column=6, padx=5, sticky="n")
        score_blue.grid(row=2, column=7, padx=5, sticky="n")

        red1 = tk.Label(self, text="Red 1")
        red2 = tk.Label(self, text="Red 2")
        blue1 = tk.Label(self, text="Blue 1")
        blue2 = tk.Label(self, text="Blue 2")
        red_score = tk.Label(self, text="Red Score")
        blue_score = tk.Label(self, text="Blue Score")

        red1.grid(row=1, column=2, padx=5, sticky="s")
        red2.grid(row=1, column=3, padx=5, sticky="s")
        blue1.grid(row=1, column=4, padx=5, sticky="s")
        blue2.grid(row=1, column=5, padx=5, sticky="s")
        red_score.grid(row=1, column=6, padx=5, sticky="s")
        blue_score.grid(row=1, column=7, padx=5, sticky="s")
        edit.grid(row=3, column=5, pady=4)

        

        sub_add_btn.grid(row=3, column=2, sticky="n")
        sub_rmv_btn.grid(row=3, column=7, sticky="n")
        sub_edt_btn.grid(row=3, column=4, sticky="ne")
        make_table()
  
  
# Driver Code
app = tkinterApp()
app.geometry('1280x720')
app.mainloop()