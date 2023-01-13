import pygame

pygame.init() # Initialize Pygame
window_size = (700, 700) # Set the window size
screen = pygame.display.set_mode(window_size) # Create the window
pygame.display.set_caption("The Ant Game") # Set the title of the window
bg_color = (255, 255, 255) # Set the background color

# # Set the font and font size
font_1 = pygame.font.Font(None, 70)
font_2 = pygame.font.Font(None, 35)

# Set the text and text color
text_color = (48,19,1)
text_1 = "THE ANT GAME"
text_2 = "LEVEL"
text_3 = "TIME"
text_4 = "SCORE"
text_5 = "SUGAR 1"
text_6 = "SUGAR 2"

# Render the text
text_surface_1 = font_1.render(text_1, True, text_color)
text_surface_2 = font_2.render(text_2, True, text_color)
text_surface_3 = font_2.render(text_3, True, text_color)
text_surface_4 = font_2.render(text_4, True, text_color)
text_surface_5 = font_2.render(text_5, True, text_color)
text_surface_6 = font_2.render(text_6, True, text_color)

# Set the position of the text box
text_pos_1 = (90, 80)
text_pos_2 = (560, 50)
text_pos_3 = (560, 180)
text_pos_4 = (560, 310)
text_pos_5 = (560, 440)
text_pos_6 = (560, 570)

# Set the size of the bounding box
rect_size_1 = (500, 500)
rect_size_2 = (110, 75)

# Set the position of the bounding box
rect_pos_1 = (30, 170 )
rect_pos_2 = (560, 75)
rect_pos_3 = (560, 205)
rect_pos_4 = (560, 335)
rect_pos_5 = (560, 465)
rect_pos_6 = (560, 595)

# Set the color and thickness of the bounding box
rect_color = (92, 64, 51) # Dark Brown
rect_thickness = 2


# Set the level to display
level = 1
level_font = pygame.font.Font(None, 50)
level_text = level_font.render(str(level), True, text_color)
level_pose = (605, 95)

# Set the score to display
score = 12
score_font = pygame.font.Font(None, 40)
score_text = level_font.render(str(score) + "/20", True, text_color)
score_pose = (570, 360)

# Load sugar icon image 
sugar_image = pygame.image.load("sugar_3.png")
sugar_image = pygame.transform.scale(sugar_image, (55,55)) 
sugar_rect = sugar_image.get_rect()
sugar_rect.center = (615, 500)
sugar_rect_2 = sugar_image.get_rect()
sugar_rect_2.center= (615, 630)

# Timer
timer_font = pygame.font.Font(None, 40)
duration = 60 # Set the duration of the timer in seconds
clock = pygame.time.Clock() # Create a clock object to track the elapsed time

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the background
    screen.fill(bg_color)
    
    # Draw the text box
    screen.blit(text_surface_1, text_pos_1)
    screen.blit(text_surface_2, text_pos_2)
    screen.blit(text_surface_3, text_pos_3)
    screen.blit(text_surface_4, text_pos_4)
    screen.blit(text_surface_5, text_pos_5)
    screen.blit(text_surface_6, text_pos_6)

    # Draw the bounding box
    pygame.draw.rect(screen, rect_color, (rect_pos_1, rect_size_1), rect_thickness)
    pygame.draw.rect(screen, rect_color, (rect_pos_2, rect_size_2), rect_thickness)
    pygame.draw.rect(screen, rect_color, (rect_pos_3, rect_size_2), rect_thickness)
    pygame.draw.rect(screen, rect_color, (rect_pos_4, rect_size_2), rect_thickness)
    pygame.draw.rect(screen, rect_color, (rect_pos_5, rect_size_2), rect_thickness)
    pygame.draw.rect(screen, rect_color, (rect_pos_6, rect_size_2), rect_thickness)

    # Blit the text surface to the window
    screen.blit(level_text,level_pose)
    screen.blit(score_text,score_pose)
    
    # Blit the sugar icon to the window 
    screen.blit(sugar_image, sugar_rect)
    screen.blit(sugar_image, sugar_rect_2)
        
    # Update the display
    pygame.display.flip()

pygame.quit() # Quit Pygame


