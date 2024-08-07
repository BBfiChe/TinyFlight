import pygame
import math

pygame.init()
screen = pygame.display.set_mode((128, 128))
pygame.display.set_caption('TinyFlight')

green = (0, 255, 0)
skyblue = (135, 206, 235)
black = (0, 0, 0)

hdg = 316
spd = 563
pitch = 0
roll = 0
gs = 0
aoa = 0
pitchrate = 10
rollrate = 50
alt = 5000
altspd = 0
throttle = 0
font = pygame.font.Font(r"C:\Users\Administrator\Downloads\TC3x5numbers-Regular.ttf", 5)
test = pygame.image.load(r"C:\Users\Administrator\Downloads\testflight.bmp")
imagerect = test.get_rect()
radarmode = 1
mode = 0
modes = ['TXI', 'FLY', 'WPN']
abtoggle = 0

# Constants for the HUD
SQUARE_START_X, SQUARE_START_Y = 37, 37
SQUARE_SIZE = 54
CENTER_X = SQUARE_START_X + SQUARE_SIZE // 2
CENTER_Y = SQUARE_START_Y + SQUARE_SIZE // 2
LINE_SPACING = 5
TEXT_OFFSET = 6
MAX_LINES = 5
INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

# Example F-22 Raptor, clean config
abmaxthrust = 312000
maxthrust = 232000
minweight = 193191
weight = 0

def rotate_point(px, py, ox, oy, angle):
    cos_theta, sin_theta = math.cos(angle), math.sin(angle)
    px, py = px - ox, py - oy
    return px * cos_theta - py * sin_theta + ox, px * sin_theta + py * cos_theta + oy

def draw_rotated_text(surface, text, pos, angle, color, font_size=12):
    font = pygame.font.SysFont(None, font_size)
    text_surface = pygame.transform.rotate(font.render(text, True, color), angle)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect.topleft)

def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=4, space_length=4, gap_length=10):
    x1, y1, x2, y2 = *start_pos, *end_pos
    total_length = math.hypot(x2 - x1, y2 - y1)
    half_gap = gap_length / 2
    dash_total_length = dash_length + space_length
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    gap_offset_x = half_gap * (x2 - x1) / total_length
    gap_offset_y = half_gap * (y2 - y1) / total_length
    start_gap_x, start_gap_y = mid_x - gap_offset_x, mid_y - gap_offset_y
    end_gap_x, end_gap_y = mid_x + gap_offset_x, mid_y + gap_offset_y

    def draw_segment(start, end):
        segment_length = math.hypot(end[0] - start[0], end[1] - start[1])
        num_dashes = int(segment_length / dash_total_length)
        for i in range(num_dashes + 1):
            dash_start = (
                start[0] + (end[0] - start[0]) * i * dash_total_length / segment_length,
                start[1] + (end[1] - start[1]) * i * dash_total_length / segment_length
            )
            dash_end = (
                start[0] + (end[0] - start[0]) * (i * dash_total_length + dash_length) / segment_length,
                start[1] + (end[1] - start[1]) * (i * dash_total_length + dash_length) / segment_length
            )
            if math.hypot(dash_end[0] - start[0], dash_end[1] - start[1]) > segment_length:
                dash_end = end
            pygame.draw.line(surface, color, dash_start, dash_end, width)

    draw_segment((x1, y1), (start_gap_x, start_gap_y))
    draw_segment((end_gap_x, end_gap_y), (x2, y2))

def compute_out_code(x, y, min_x, min_y, max_x, max_y):
    code = INSIDE
    if x < min_x:
        code |= LEFT
    elif x > max_x:
        code |= RIGHT
    if y < min_y:
        code |= BOTTOM
    elif y > max_y:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, min_x, min_y, max_x, max_y):
    outcode1 = compute_out_code(x1, y1, min_x, min_y, max_x, max_y)
    outcode2 = compute_out_code(x2, y2, min_x, min_y, max_x, max_y)
    accept = False

    while True:
        if outcode1 == 0 and outcode2 == 0:
            accept = True
            break
        elif (outcode1 & outcode2) != 0:
            break
        else:
            x, y = 0.0, 0.0
            outcode_out = outcode1 if outcode1 != 0 else outcode2
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (max_y - y1) / (y2 - y1)
                y = max_y
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (min_y - y1) / (y2 - y1)
                y = min_y
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (max_x - x1) / (x2 - x1)
                x = max_x
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (min_x - x1) / (x2 - x1)
                x = min_x

            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_out_code(x1, y1, min_x, min_y, max_x, max_y)
            else:
                x2, y2 = x, y
                outcode2 = compute_out_code(x2, y2, min_x, min_y, max_x, max_y)

    return (x1, y1), (x2, y2) if accept else None

def generate_hud_lines(pitch_angle):
    hud_lines = []
    pitch_angle = int(pitch_angle)  # Ensure pitch_angle is an integer
    start_pitch = (pitch_angle // LINE_SPACING - (MAX_LINES // 2)) * LINE_SPACING
    end_pitch = start_pitch + ((MAX_LINES - 1) * LINE_SPACING)
    for pitch in range(start_pitch, end_pitch + 1, LINE_SPACING):
        line_y = CENTER_Y - (pitch - pitch_angle) * (SQUARE_SIZE / (2 * (90 // LINE_SPACING)))
        display_pitch = abs(pitch % 180 - 180 if pitch % 180 > 90 else pitch % 180)
        hud_lines.append((f"{display_pitch}", [(CENTER_X - SQUARE_SIZE // 2, line_y), (CENTER_X + SQUARE_SIZE // 2, line_y)], display_pitch == 0))
    return hud_lines

def draw_hud_lines(surface, roll_angle, pitch_angle):
    roll_rad = math.radians(roll_angle)
    hud_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
    hud_surface.set_colorkey(black)
    hud_surface.fill(black)

    hud_lines = generate_hud_lines(pitch_angle)
    for pitch_text, line, is_zero_pitch in hud_lines:
        (start_x, start_y), (end_x, end_y) = line
        new_start_x, new_start_y = rotate_point(start_x, start_y, CENTER_X, CENTER_Y, roll_rad)
        new_end_x, new_end_y = rotate_point(end_x, end_y, CENTER_X, CENTER_Y, roll_rad)
        clipped_line = cohen_sutherland_clip(new_start_x, new_start_y, new_end_x, new_end_y, SQUARE_START_X, SQUARE_START_Y, SQUARE_START_X + SQUARE_SIZE, SQUARE_START_Y + SQUARE_SIZE)

        if clipped_line:
            clipped_start, clipped_end = clipped_line
            if is_zero_pitch:
                draw_dashed_line(hud_surface, green, (clipped_start[0] - SQUARE_START_X, clipped_start[1] - SQUARE_START_Y), (clipped_end[0] - SQUARE_START_X, clipped_end[1] - SQUARE_START_Y), 1, dash_length=SQUARE_SIZE, space_length=0, gap_length=15)
            else:
                draw_dashed_line(hud_surface, green, (clipped_start[0] - SQUARE_START_X, clipped_start[1] - SQUARE_START_Y), (clipped_end[0] - SQUARE_START_X, clipped_end[1] - SQUARE_START_Y))

            text_angle = -roll_angle
            offset_x, offset_y = TEXT_OFFSET * math.cos(roll_rad), TEXT_OFFSET * math.sin(roll_rad)
            draw_rotated_text(surface, pitch_text, (clipped_start[0] - offset_x, clipped_start[1] - offset_y), text_angle, green)
            draw_rotated_text(surface, pitch_text, (clipped_end[0] + offset_x, clipped_end[1] + offset_y), text_angle, green)

    surface.blit(hud_surface, (SQUARE_START_X, SQUARE_START_Y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                mode = (mode + 1) % 3

    if throttle <= 80:
        spd = throttle * 7
    else:
        spd = 700
    if abtoggle == 0:
        twr = maxthrust*(throttle/100) / (minweight + weight)
    elif abtoggle == 1:
        twr = abmaxthrust / (minweight + weight)

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        roll -= rollrate*twr / 60
    if keys[pygame.K_RIGHT]:
        roll += rollrate*twr / 60
    if keys[pygame.K_UP]:
        pitch += pitchrate*twr / 60
    if keys[pygame.K_DOWN]:
        pitch -= pitchrate*twr / 60
    if keys[pygame.K_z]:
        pass
    if keys[pygame.K_x]:
        pass
    if keys[pygame.K_a]:
        throttle -= 1
    if keys[pygame.K_d]:
        throttle += 1

    if alt < 0:
        alt = 0
    if hdg < 0:
        hdg = 359
    elif hdg > 359:
        hdg = 0
    if throttle < 0:
        throttle = 0
    elif throttle > 100:
        throttle = 100
    if roll < 0:
        roll = 359
    elif roll > 359:
        roll = 0
    if pitch < 0:
        pitch = 359
    elif pitch > 359:
        pitch = 0

    screen.fill(black)
    screen.blit(test, imagerect)
    screen.blit(font.render(str(hdg), False, green), (79 - len(str(hdg)) * 4, 20))
    screen.blit(font.render('ASL' if radarmode == 0 else 'RDR', False, green), (114, 47))
    screen.blit(font.render(str(alt), False, green), (107, 57))
    screen.blit(font.render(str(spd), False, green), (28 - len(str(spd)) * 4, 54))
    screen.blit(font.render(str(altspd), False, green), (127 - len(str(altspd) * 4), 122))
    screen.blit(font.render(modes[mode], False, green), (11, 120))
    screen.blit(font.render(str(round((spd / 666.7), 2)), False, green), (11, 68))
    screen.blit(font.render(str(round(gs, 2)), False, green), (11, 75))
    screen.blit(font.render(str(round(aoa, 2)), False, green), (11, 82))
    if abtoggle == 0:
        pygame.draw.line(screen, green, [4, 126], [4, 126 - (throttle / 20) * 4])
        pygame.draw.line(screen, green, [5, 126], [5, 126 - (throttle / 20) * 4])
    else:
        pygame.draw.line(screen, green, [4, 126], [4, 106])
        pygame.draw.line(screen, green, [5, 126], [5, 106])

    if 0 <= throttle <= 80:
        abtoggle = 0
    else:
        abtoggle = 1

    # Draw the HUD lines for pitch display
    draw_hud_lines(screen, roll, pitch)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
