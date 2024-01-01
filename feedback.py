import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
from ttkbootstrap.tooltip import ToolTip

class Feedback(ttk.Frame):
    def __init__(self, main, PATH):
        super().__init__(main)

        # Links        
        self.feedback_form = 'https://docs.google.com/forms/d/e/1FAIpQLSegZLNXZ2PcSCRW8f3nx1twnoym3_bMNMQ92dRNkzBPfiHB0g/viewform?usp=sf_link'
        self.feature_form = 'https://docs.google.com/forms/d/e/1FAIpQLScjMIzlfjLIKHi1bNpvF4rk7k3u-lP5oogBlFlHdCKqoSLkLA/viewform?usp=sf_link'
        self.issue_form = 'https://docs.google.com/forms/d/e/1FAIpQLScghg-gvAe0lMLHqNGakLTK33hha4ip0faCTwzyp4IrP1ji6w/viewform?usp=sf_link'
        self.issue_github = 'https://github.com/Uthayamurthy/TURPO/issues'

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.path = PATH
        
        # Header
        hdr_frame = ttk.Frame(self, padding=10)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)
        hlbl = ttk.Label(master=hdr_frame, text='Feedback', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        body_frame = ttk.Frame(self, padding=10)
        body_frame.grid(row=1, column=0, sticky=NSEW)

        desc = 'Make TURPO even better: Tell us what you think!'

        desc_lbl = ttk.Label(master=body_frame, text=desc, font=('Helvetica', 16, 'bold'))
        desc_lbl.grid(row=0, column=0, padx=10, pady=10)

        feedback_lbl = ttk.Label(master=body_frame, text='Share your Feedback', font=('Helvetica', 15, 'bold'))
        feedback_lbl.grid(row=1, column=0, padx=10, pady=15)

        feedback_btn = ttk.Button(master=body_frame, text='Feedback Form', bootstyle='primary', command=self.open_feedback)
        feedback_btn.grid(row=1, column=1, padx=10, pady=15)

        ToolTip(feedback_btn, 'You will be redirected to a Google Form.')

        feature_lbl = ttk.Label(master=body_frame, text='Suggest a New Feature', font=('Helvetica', 15, 'bold'))
        feature_lbl.grid(row=2, column=0, padx=10, pady=15)

        feature_btn = ttk.Button(master=body_frame, text='Suggestion Form', bootstyle='primary', command=self.open_suggestion)
        feature_btn.grid(row=2, column=1, padx=10, pady=15)

        ToolTip(feature_btn, 'You will be redirected to a Google Form. Kindly check the project roadmap before you post a suggestion here.')
        
        issue_lbl = ttk.Label(master=body_frame, text='Report an Issue', font=('Helvetica', 15, 'bold'))
        issue_lbl.grid(row=3, column=0, padx=10, pady=15)

        issue_btn_1 = ttk.Button(master=body_frame, text='Issue Form', bootstyle='primary', command=self.open_issue_1)
        issue_btn_1.grid(row=3, column=1, padx=10, pady=15)

        ToolTip(issue_btn_1, 'You will be redirected to a Google Form. If Issue is verified, it will be opened as a issue in Github behalf of you.')

        issue_btn_2 = ttk.Button(master=body_frame, text='Github', bootstyle='primary', command=self.open_issue_2)
        issue_btn_2.grid(row=3, column=2, padx=10, pady=15)

        ToolTip(issue_btn_2, 'Open a issue in Github Directly.')



    def open_feedback(self):
        webbrowser.open_new_tab(self.feedback_form)

    def open_suggestion(self):
        webbrowser.open_new_tab(self.feature_form)
    
    def open_issue_1(self):
        webbrowser.open_new_tab(self.issue_form)
    
    def open_issue_2(self):
        webbrowser.open_new_tab(self.issue_github)