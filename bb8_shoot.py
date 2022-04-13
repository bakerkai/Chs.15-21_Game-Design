#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade
# import time

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800 # Screen width
SH = 600 # Screen Height
SP = 4 # speed
t_speed = 2
t_score = 5
b_score = 2
b_speed = 10
bullet_scale = 1

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bb8.png", BB8_scale,)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.center_x += self.change_x
        if self.left <= 0:
            self.left = 0
        if self.right >= SW:
            self.right = SW


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_y -= t_speed
        if self.top < 0:
            self.center_x = random.randrange(self.w, SW - self.w)
            self.center_y = random.randrange(SH + self.h, SH*2)

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")

    def update(self):
        self.center_y += b_speed
        if self.bottom > SH:
            pass

#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)

    def reset(self):
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # set the score
        self.score = 0
        self.Gameover = False

        # set the time
        # self.time = time.sleep(15)

        # set the player
        self.BB8 =  Player()
        self.BB8.center_x = SW/2
        self.BB8.bottom = 20
        self.player_list.append(self.BB8)

        # create the troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w,SW-trooper.w)
            trooper.center_y = random.randrange(SH // 2, SH * 2)
            self.trooper_list.append(trooper)
    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        # Draw the score on screen
        output = f"score: {self.score}"
        arcade.draw_text(output,SW - 80,SH - 20,arcade.color.NEON_CARROT, 14)
        # Draw gameoverscreen
        if self.Gameover:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over: Press R to Play Again", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14, align= "center", anchor_x= "center")

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()
        self.bullet_list.update()
        BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        # trooper_hit_list = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if len(BB8_hit) > 0 and not self.Gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.Gameover = True
        if len(self.trooper_list) == 0:
            self.Gameover = True
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
            arcade.check_for_collision_with_list(bullet, self.trooper_list)
            if len(hit_list) > 0:
                arcade.play_sound(self.bullet.explosion)
                bullet.kill()
            for trooper in hit_list:
                trooper.kill()
                self.score += t_score
        if len(BB8_hit)>0 and not self.Gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.Gameover = True
        if self.score == trooper_count:
            self.reset()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.BB8.change_x = -SP
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = SP
        elif key == arcade.key.R and self.Gameover:
            self.reset()
        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.top
            self.bullet.angle = 90
            self.bullet_list.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_x = 0



    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     self.BB8.center_x = x
    #     self.BB8.center_y = y


#-----Main Function--------
def main():
    window = MyGame(SW,SH,"BB8 Attack")
    window.reset()
    arcade.run()


#------Run Main Function-----
if __name__ == "__main__":
    main()
