#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800 # Screen width
SH = 600 # Screen Height
SP = 4 # speed

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bb8.png", BB8_scale,)
    def update(self):
        pass

class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
    def update(self):
        pass

#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def reset(self):
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        # set the score
        self.score = 0

        # set the player
        self.BB8 =  Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH/2
        self.player_list.append(self.BB8)

        # create the troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w,SW-trooper.w)
            trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)
    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()

        # Draw the score on screen
        output = f"score: {self.score}"
        arcade.draw_text(output,10,20,arcade.color.BLACK,14)

    def on_update(self, dt):
        pass
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.BB8.center_x = x
        self.BB8.center_y = y


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    window.reset()
    arcade.run()


#------Run Main Function-----
if __name__ == "__main__":
    main()
