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

### The `<bwallx />` tag spawns a wall of bullets along the Y axis and points a certain direction

```xml
<bwallx px=X offset=Y_OFFSET angle=θ spacing=Y_SPACE velocity=VEL imagepath=PATH_TO_IMAGE waittime=SECONDS/>
```

X is the X position of the bullet wall

Y_OFFSET is the Y offset of the bullet wall

Y_SPACE is the Y spacing of the bullet wall

θ is the angle of the bullet wall

PATH_TO_IMAGE is the path to the image the the bullet wall uses

SECONDS is the seconds that the bullet wall waits for before moving

### `<bwally />` is the same as the previous tag except that the axis they go along is X instead of Y

### The `<repeat />` tag is like a for loop for the parser so the tags inside it get repeated, nesting `<repeat />` is NOT supported, delay tags are not affected by this tag

```xml
<repeat amount=AMOUNT prop=PROP increment=AMT>
    <bwallx px="100" offset="80" angle="0" spacing="200" velocity="8" imagepath="bone.png" waittime="4"/>
</repeat>
```

AMOUNT is the amount of times the inside tag is repeated

PROP is the property to increment or decrement by AMT, AMT increases by AMT AMOUNT times
