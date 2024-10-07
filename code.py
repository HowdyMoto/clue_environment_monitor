import time
from adafruit_clue import clue
from displayio import Group, OnDiskBitmap, TileGrid
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Constants for temperature and humidity thresholds
LOW_TEMPERATURE = 24
HIGH_TEMPERATURE = 30
LOW_HUMIDITY = 20
HIGH_HUMIDITY = 60
SHOW_FAHRENHEIT = True

# Load the font
FONT = bitmap_font.load_font("/fonts/Nunito-75.bdf")
FONT = bitmap_font.load_font("/fonts/PublicSans-Bold-32.bdf")
FONT = bitmap_font.load_font("/fonts/PublicSans-Bold-48.bdf")


# File paths for icons
TEMPERATURE_PNG = "/icons/temperature.bmp"
HUMIDITY_PNG = "/icons/humidity.bmp"

# Create a display group
display_group = Group()

# Load the temperature and humidity icons as bitmaps
temperature_icon_bmp = OnDiskBitmap(TEMPERATURE_PNG)
humidity_icon_bmp = OnDiskBitmap(HUMIDITY_PNG)

temperature_icon = TileGrid(temperature_icon_bmp, pixel_shader=temperature_icon_bmp.pixel_shader, x=8, y=40)
temperature_label = label.Label(FONT, text="... -- C", color=clue.WHITE, x=78, y=66)

humidity_icon = TileGrid(humidity_icon_bmp, pixel_shader=humidity_icon_bmp.pixel_shader, x=8, y=140)
humidity_label = label.Label(FONT, text="... -- %", color=clue.WHITE, x=76, y=164)

# Add icons and labels to the display group
display_group.append(temperature_icon)
display_group.append(temperature_label)
display_group.append(humidity_icon)
display_group.append(humidity_label)

# Show the display group on the CLUE screen
clue.display.root_group = display_group
print(clue.display.brightness)
clue.display.brightness = 0.5

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

# Main loop to update temperature and humidity
while True:
    temperature = clue.temperature  # Get temperature from clue's sensor
    humidity = clue.humidity        # Get humidity from clue's sensor
    temperature_type_string = "F"

    # Report temperature
    if (SHOW_FAHRENHEIT):
        temperature = celsius_to_fahrenheit(temperature)
        temperature_label.text = f"{temperature:.0f} F"
    else:
        temperature = temperature
        temperature_label.text = f"{temperature:.0f} C"

    # Report humidity, report if it's too high
    humidity_label.text = f"{humidity:.0f} %"
    if (humidity >= HIGH_HUMIDITY ):
        humidity_label.color = clue.RED
    else:
        humidity_label.color = clue.WHITE

    # Hold the left button for a moment to toggle temperature mode
    if clue.button_a:
        print("Toggle temperature mode")
        SHOW_FAHRENHEIT = not SHOW_FAHRENHEIT
    
    time.sleep(1)  # Update every second
