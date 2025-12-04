from src.Interface.App import Application

'''
If main.py exists, it's because it's responsible for initializing the application.
But above all, this file ensures that each file starts from
the location where it is located when searching for one or more resources.
This avoids confusion when searching for one or more resources,
since everything starts from here.
'''
if __name__ == "__main__":
    app = Application() 
    app.run()   # Starts the Tkinter loop which will take care of the rest

