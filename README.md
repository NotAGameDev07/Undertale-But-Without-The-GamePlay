# How to write a level file for <i>insert_title_here</i>

### The `<delay />` tag sets a delay for the proceeding XML tags

```xml
<delay duration=X/>
```

X is the duration in seconds

### The `<bullet />` tag is to spawn a bullet

```xml
<bullet px=X py=Y angle=θ velocity=VEL imagepath=PATH_TO_IMAGE waittime=SECONDS/>
```

X is the X position of the bullet
Y is the Y position of the bullet
θ is the angle of the bullet
PATH_TO_IMAGE is the path to the image the the bullet uses
SECONDS is the seconds that the bullet waits for before moving

###### NOTE: The bullet appears after the combined delay durations of all of the delay tags preceding it

### The `<bwall />` tag spawns a wall of bullets along an axis and points a certain direction
