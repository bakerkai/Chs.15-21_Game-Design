#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade
import math
# import time

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 10
SW = 800 # Screen width
SH = 600 # Screen Height
SP = 4 # speed
t_speed = 2
levels = 3
'''
level 0 = instructions
level 1 = level 1
level 2 = level 2
level 4 = gameover screen
'''
t_score = 5
b_score = 2
b_speed = 10
bullet_scale = 1
EXPLOSION_TEXTURE_COUNT = 50
MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png", 1,)
        self.current_texture = 0
        self.textures = texture_list
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale,)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0
        self.change_angle = 0


    def update(self):
        self.angle += self.change_angle
        angle_rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)
        if self.left <= 0:
            self.left = 0
        elif self.right >= SW:
            self.right = SW

        if self.top >= SH:
            self.top = SH
        elif self.bottom <= 0:
            self.bottom = 0

class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1,2,2) # !!!!!
        self.dy = random.randrange(-1,2,2)

    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx

        if self.bottom <0 or self.top >SH:
            self.dy  *= -1
        if self.left < 0 or self.right > SW:
            self.dx *= -1

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x -= self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)

        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()

class Enemy_Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        if self.angle == 0:
            self.center_x += b_speed
        elif self.angle == 90:
            self.center_y += b_speed
        elif self.angle == 180:
            self.center_x -= b_speed
        elif self.angle == 270:
            self.center_y -= b_speed

        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()

#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.current_state = 0
        self.gameover = True

        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        if self.current_state in range(1, levels + 1):
            self.background = arcade.load_texture(f"Images/sky{self.current_state}.png")

        #Create sprite lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        # set the score
        # self.score = 0
        # self.Gameover = False

        # set the time
        # self.time = time.sleep(15)

        # set the player
        self.BB8 =  Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH/2
        self.player_list.append(self.BB8)

        # create the troopers
        for i in range(trooper_count):
            trooper = Trooper()
            if i%2 == 0:
                trooper.center_x = random.randrange(trooper.w, int(SW - SW / 3))
            else:
                trooper.center_x = random.randrange(int(SW * 2/3), SW - trooper.w)
            trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)


    def on_draw(self):
        arcade.start_render()
        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and SPACE to fire. Choose your level.", SW //2, SH // 2, arcade.color.PISTACHIO, align="center", anchor_x= "center")

        elif not self.Gameover:
            arcade.draw_texture_rectangle(SW // 2, SH //2, SW, SH, self.background)
            self.trooper_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
            self.ebullets.draw()
            self.explosions.draw()
            # Draw the score on screen
            output = f"score: {self.score}"
            level = f"level: {self.current_state}"
            arcade.draw_rectangle_filled(SW - 40, SH - 20, 80, 40, arcade.color.BLACK)
            arcade.draw_text(output,SW - 80,SH - 40, ((0,255,0)), 14)
            arcade.draw_text(level,SW - 80,SH - 20,((0,255,0)), 14)

        else:
        # Draw gameoverscreen
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over: Press I for instructions or a level number.", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14, align= "center", anchor_x= "center")


    def on_update(self, dt):
        if self.current_state in range(1, levels + 1):
            self.Gameover = False
        else:
            self.Gameover = True

        if not self.Gameover:
            self.player_list.update()
            self.trooper_list.update()
            self.bullet_list.update()
            self.ebullets.update()
            self.explosions.update()
            BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            # trooper_hit_list = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            if len(self.trooper_list) == 0:
                self.current_state += 1
                self.reset()


            if len(BB8_hit) > 0 and not self.Gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_state = levels + 1

            # randomly shooting bullets
            for trooper in self.trooper_list:
                if random.randrange(1000) == 0:
                    ebullet = Enemy_Bullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    ebullet.top = trooper.bottom
                    self.ebullets.append(ebullet)

            # check if bb8 hit
            BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
            if len(BB8_bombed) > 0 and not self.Gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_state = levels + 1
            if len(self.trooper_list) == 0:
                self.Gameover = True

            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.bullet.explosion) # possibly move to label 65 function
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosions.append(explosion)

                for trooper in hit_list: # label 65
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
            self.BB8.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.BB8.change_angle = -ANGLE_SPEED
        elif key == arcade.key.UP:
            self.BB8.speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.BB8.change_angle = -MOVEMENT_SPEED
        elif key == arcade.key.R and self.Gameover:
            self.reset()
        elif key == arcade.key.SPACE and not self.Gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = b_speed
            self.bullet_list.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)
        if key == arcade.key.I and self.Gameover:
            self.current_state = 0
        elif key == arcade.key.KEY_1 and self.Gameover:
            self.current_state = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_2 and self.Gameover:
            self.current_state = 2
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_3 and self.Gameover:
            self.current_state = 3
            self.score = 0
            self.reset()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_angle = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.BB8.speed = 0



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
