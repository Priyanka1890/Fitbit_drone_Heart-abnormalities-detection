
import pandas as pd
import os



class LoginData:
    def __init__(self, data_path:str):
        self.df = pd.read_csv(data_path)
    def check_login(self, usr, pwd, role):
        return self.df[(self.df.username==usr) & (self.df.password == pwd) & (self.df.role == role)]
