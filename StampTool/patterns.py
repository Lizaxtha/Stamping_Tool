import random
import math

class PatternGenerator:

    @staticmethod
    def generate_positions(pattern_name, x, y, stamp_spacing, random_offset, canvas_width=None, canvas_height=None):

        if pattern_name == "Brush":
            return PatternGenerator._brush_pattern(x,y)
        elif pattern_name == "Random":
            return PatternGenerator._random_pattern(x,y,random_offset)
        elif pattern_name == "Circle":
            return PatternGenerator._circle_pattern(x,y,stamp_spacing)
        elif pattern_name == "Spiral":
            return PatternGenerator._spiral_pattern(x,y,stamp_spacing)
        elif pattern_name == "Grid":
            return PatternGenerator._grid_pattern(x,y,stamp_spacing)
        elif pattern_name == "Border":
            return PatternGenerator._border_pattern(canvas_width,canvas_height,stamp_spacing)
        elif pattern_name == "Star":
            return PatternGenerator._star_pattern(x,y,stamp_spacing)
        else:
            return [(x,y)]

    @staticmethod
    def _brush_pattern(x,y):
        return [(x,y)]
    
    @staticmethod
    def _random_pattern(x,y,offset):
        return[(
            x+random.randint(-offset, offset),
            y+random.randint(-offset, offset),

        )]

    @staticmethod
    def _circle_pattern(cx,cy,radius):
        positions = []
        num_stamps = 12

        for i in range(num_stamps):
            angle = (2*math.pi*i)/num_stamps
            stamp_x = cx + radius *3*math.cos(angle)
            stamp_y = cy + radius *3*math.sin(angle)
            positions.append((stamp_x, stamp_y))

        return positions
