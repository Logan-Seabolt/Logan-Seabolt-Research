import tkinter

class experiment_Program:

    def leftHandMap(self):
        return {
            "index": "f",
            "middle": "d",
            "ring": "s",
            "pinky": "a",
            "thumb": "space"
        }

    def rightHandMap(self):
        return {
            "index": "j",
            "middle": "k",
            "ring": "l",
            "pinky": ";",
            "thumb": "space"
        }

    def testClick(self):
        print("Henlo")

    def runExperiment(self):
        top = tkinter.Tk()
        greeting = tkinter.Label(
            text="Hello\nWelcome To Logan Seabolt\'s brain mapping experiment",
            fg="blue",
            bg="tan",
            width=100,
            height=50)
        button = tkinter.Button(
            text="Press to continue",
            width=25,
            height=5,
            bg="silver",
            fg="black",
            command=self.testClick
        )
        greeting.pack()
        button.pack()
        top.mainloop()


if __name__ == '__main__':
    exp = experiment_Program()
    exp.runExperiment()


