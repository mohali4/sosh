from . import clearScrean
frames = []

class Form :
    def __init__(self, *rows) -> None:
        frames.append(self)
        self.rows = rows
        screen_render()
    def exit(self):
        frames.remove(self)

def screen_render ():
    while frames != []:
        form:Form = frames[-1]
        screen = ""
        option = 0
        options = []
        for row in form.rows :
            if isinstance(row,str):
                screen += row
            elif isinstance(row,list) or isinstance(row,tuple):
                screen += f"[{option}] {row[0]}"
                options.append(row[1])
                option += 1
            screen += "\n"
        clearScrean()
        print(screen)
        while True :
            try :
                option = input("\nSelect action : ")
                option = int(option)
                action = options[option]
                break
            except:
                print (f"Wrong input ! ")
        clearScrean()
        try:
            action(form)
        except TypeError:
            action()
        input("Enter to countinue... ")




