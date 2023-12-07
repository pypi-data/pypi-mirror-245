import importlib.resources as resources
from importlib.resources import read_binary, read_text
import sys
import pandas as pd 

def get_cal_list() -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    # contents=read_text("predefs", "cal_names_list.txt")
    # print(contents)
    # df = pd.DataFrame([contents.split('\n')])
    # df=df.transpose()
    # print(df)
    # sys.exit()

    with resources.path("predefs", "cal_names_list.txt") as df:
        return pd.read_fwf(df,names=['CALS'])
    
def get_jpl_results() -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    with resources.path("predefs", "nasa_jpl_results.txt") as df:
    # contents=read_binary("predefs", "nasa_jpl_results.txt")
    # with contents as df:
        return pd.read_csv(df,delimiter=",", skiprows=1, names=['DATE','MJD','RA','DEC','ANG-DIAM'])
    
def get_calsky_results(year) -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    with resources.path("predefs", f"Jupiter_calsky_{year}.dat") as df:
    # contents=read_binary("predefs", f"Jupiter_calsky_{year}.dat")
    # with contents as df:
        return pd.read_csv(df,delimiter=",", skiprows=1, names=['month','day','ra','dec','radius'])
    