# Abstracted cv2 functions that take custom types Vector2 and ColorBGR as arguments
# and applies the same font to all text

import cv2
import vector2
import color

def draw_rectangle(frame, pos, size, color, line_type):
    cv2.rectangle(frame, pos.to_tuple(), (pos.x + size.x, pos.y + size.y), color.to_tuple(), line_type)

def draw_text(frame, text, pos, text_color, line_type):
    cv2.putText(frame, text, (pos.x + 10, pos.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color.to_tuple(), line_type)