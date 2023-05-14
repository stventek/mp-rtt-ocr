from real_time_translate import RealTimeTranslate
import main_tk

mainTK = main_tk.MainTK()

if __name__ == "__main__":
    window_app = RealTimeTranslate(mainTK)
    mainTK.app.mainloop()