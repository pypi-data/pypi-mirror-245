import os, pygame

from ..src.UserInterface import UserInterface

RUN_FOR = -1 # seconds

PATH = os.path.join(os.path.dirname(__file__), "image.png")

class Shift:
    def __init__(self, type_, car, crew, start, end):
        self.type = type_
        self.car = car
        self.crew = crew
        self.start = start
        self.end = end

class Program():
    def __init__(self):
        self.win_w, self.win_h = 300, 270
        self.center = (int(self.win_w/2),int(self.win_h/2))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))

    def main(self):

        with open(os.path.join(os.path.dirname(__file__), "test_dp.xml"), "r") as f:
            structure = f.read()

        shift = Shift("JOK", "A-39", ["First1 Last1", "First2 Last2", "First3 Last3", "First4 Last4"], "15.11.2023, 10:00", "15.11.2023, 18:30")
        
        self.ui = UserInterface()
        self.ui.set_structure(structure)
        self.ui.set_variables({
            "type_": shift.type,
            "car": shift.car,
            "crew": [(index, name) for index, name in enumerate(shift.crew)],
            "start": shift.start,
            "end": shift.end
        })
        self.ui.set_pos((0, 0))
        
        self.screen.fill((0,0,0))
        self.ui.draw(self.screen)
        pygame.display.flip()
        pygame.image.save(self.screen, PATH)
        print(f"Saved to file '{PATH}'")
        
        

Program().main()