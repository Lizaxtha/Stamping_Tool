import random
import math
class PatternGenerator:

    @staticmethod
    def generate_positions(
        pattern_name, 
        x, 
        y, 
        stamp_spacing, 
        random_offset, 
        canvas_width=None, 
        canvas_height=None, 
        stamp_count=1,
        circle_radius=300, 
        spiral_turns=5, 
        spiral_spacing=250,
        border_spacing=150, 
        border_margin=60):

        if pattern_name == "Brush":
            return PatternGenerator._brush_pattern(x,y)
        elif pattern_name == "Random":
            return PatternGenerator._random_pattern(x,y,random_offset, stamp_count)
        elif pattern_name == "Circle":
            return PatternGenerator._circle_pattern(x,y,circle_radius,stamp_count)
        elif pattern_name == "Spiral":
            return PatternGenerator._spiral_pattern(x,y,spiral_turns, spiral_spacing)
        elif pattern_name == "Border":
            return PatternGenerator._border_pattern(canvas_width,canvas_height,stamp_spacing, border_spacing, border_margin)
        else:
            return [(x,y)]

    @staticmethod
    def _brush_pattern(x,y):
        return [(x,y)]
    
    @staticmethod
    def _random_pattern(x,y,offset, stamp_count):
        positions = []

        min_distance = offset*0.35

        for _ in range(stamp_count):

            attempts = 0

            while attempts < 100:

                angle = random.uniform(0,2*math.pi)
                distance = random.uniform(0, offset)
        
                random_x = x+math.cos(angle)*distance
                random_y = y+math.sin(angle)*distance

                too_close = False

                for existing_x, existing_y in positions:
                    dx=random_x - existing_x
                    dy = random_y - existing_y

                    if(dx*dx + dy*dy)<(min_distance*min_distance):
                        too_close = True
                        break

                if not too_close:
                    positions.append((random_x,random_y))
                    break

                attempts +=1

        return positions

    @staticmethod
    def _circle_pattern(cx,cy,radius,stamp_count):
        positions = []

        for i in range(stamp_count):
            angle = (2*math.pi*i)/stamp_count
            stamp_x = cx + radius * math.cos(angle)
            stamp_y = cy + radius * math.sin(angle)
            positions.append((stamp_x, stamp_y))

        return positions


    @staticmethod
    def _spiral_pattern(cx,cy,spiral_turns, spiral_spacing):
        positions = []

        points_per_turn = 20
        total_points = spiral_turns*points_per_turn

        for i in range(total_points):
            angle = (2*math.pi*i)/points_per_turn
            radius = spiral_spacing *i/points_per_turn

            stamp_x = cx + radius * math.cos(angle)
            stamp_y = cy + radius * math.sin(angle)

            positions.append((stamp_x,stamp_y))

        return positions

    @staticmethod
    def _border_pattern(canvas_width, canvas_height, stamp_spacing, border_spacing, border_margin):
        positions =[]

        if canvas_width is None or canvas_height is None:
            return positions

        left = border_margin
        top = border_margin
        right = canvas_width - border_margin
        bottom = canvas_height - border_margin

        #top
        x= left 
        while x<= right:
            positions.append((x,top))
            x +=border_spacing

        #right
        y = top + border_spacing
        while y<= bottom:
            positions.append((right,y))
            y += border_spacing

        #bottom
        x =right - border_spacing
        while x>=left:
            positions.append((x,bottom))
            x -=border_spacing

        #left
        y = bottom - border_spacing
        while y>top:
            positions.append((left,y))
            y-= border_spacing

        return positions

