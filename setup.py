from cx_Freeze import setup, Executable

setup(

    name="rupturium",version="0.4",description="its rupture disk manufacturing helper",executables=[Executable("mgui.py")],

)   