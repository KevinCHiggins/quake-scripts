import shapes
import math
ARCHAIC = 1 # Actually, Wikipedia mentions "sometimes less than one"
PARTHENON = 1.25
PYCNOSTLE = 1.5
SYSTYLE = 2
EUSTYLE = 2.25 # Vitruvius mentions varying to 3 between middle columns, front and rear
DIASTYLE = 3
DEFAULT_TEXTURE = "column1_2"
NUM_STEPS = 3
def roofed_column_grid(x, y, origin, full_column_height, column_base_side):

    diam = shapes.get_oct_prism_width(column_base_side)
    entab_height = int((full_column_height / 7) * 2) # just some makey-up thing to start with... actually eyeballing photos of Archaic Doric suggests 4/15ths
    print("Diam" + str(diam))
    # I threw in a rounding hack to the shapes.get_oct_prism_width function so this error shouldn't happen
    if diam % 2 != 0:
        print("Deriving actual column diameter from the base side " + str(column_base_side) + " unfortunately led to a non-even quantity")
        return
    rad = diam / 2 # used to get position of *centre* of columns
    brushes = []
    for i in range(x):
        for j in range(y):
            # the plus one is for the column's width
            column = (shapes.create_doric_column([rad + (diam * (PARTHENON + 1) * i), rad + (diam * (PARTHENON + 1) * j), 0], full_column_height, column_base_side, DEFAULT_TEXTURE))
            for brush in column:
                brushes.append(brush)
    overall_width = (diam * (PARTHENON + 1) * (x - 1)) + diam # all spacings (including columns' width) + one column's width
    overall_breadth = (diam * (PARTHENON + 1) * (y - 1)) + diam # same idea
    fill_height = shapes.get_fillet_height(full_column_height)
    half_fill_height = math.floor(fill_height / 2)
    architrave = shapes.create_cuboid_brush((origin[0], origin[1], origin[2] + full_column_height), (origin[0] + overall_width, origin[1] + overall_breadth, origin[2] + full_column_height + (entab_height / 2 - half_fill_height)), "column1_4")
    fillet = shapes.create_cuboid_brush((origin[0] - fill_height, origin[1] - fill_height, origin[2] + full_column_height + (entab_height / 2 - math.floor(fill_height / 2))), (origin[0] + overall_width + fill_height, origin[1] + overall_breadth + fill_height, origin[2] + full_column_height + (entab_height / 2 + half_fill_height)), "column1_4")
    frieze = shapes.create_cuboid_brush((origin[0], origin[1], origin[2] + full_column_height + (entab_height / 2 + math.floor(fill_height / 2))), (origin[0] + overall_width, origin[1] + overall_breadth, origin[2] + full_column_height + entab_height), "column1_4")
    brushes.append(architrave)
    brushes.append(fillet)
    brushes.append(frieze)
    #roof/pediment
    corn_height = shapes.get_ab_height(column_base_side, full_column_height)
    corn_border = int(corn_height * 2)
    cornice = shapes.create_cuboid_brush((origin[0] - corn_border, origin[1] - corn_border, origin[2] + full_column_height + entab_height), (origin[0] + overall_width + corn_border, origin[1] + overall_breadth + corn_border, origin[2] + full_column_height + entab_height + corn_height), "column1_4")

    ped_height = shapes.get_pediment_height(overall_width + corn_border * 2, x)
    prism_height = ped_height - corn_height # subtract the height of the pitched cornice (same height as flat cornice, meaning lesser height if measured at angle!)   

    brushes.append(cornice)
    prism = shapes.create_roof_prism_brush((origin[0] - corn_border, origin[1] - corn_border, origin[2] + full_column_height + entab_height + corn_height), (origin[0] + overall_width + corn_border, origin[1] + overall_breadth + corn_border, origin[2] + full_column_height + entab_height + corn_height + prism_height))
    brushes.append(prism)
    # the entab only goes as far as the column diameters but the step below should be about equal to the extent of the capitals, so we figure out an extra border size
    border = (shapes.get_oct_prism_width(shapes.get_archaic_capital_side(column_base_side)) - diam) / 2
     # this replicates the BAD ASSUMPTION MADE IN shapes THAT HEIGHTS ARE NECESSARILY DIVISIBLE BY FIVE
    step_height = (full_column_height / 35) * 2 # replicating the logic that takes us from full height 350 to ab height 20
    for i in range(NUM_STEPS):
        v_shift = step_height * i
        h_shift = border * i
        step = shapes.create_cuboid_brush((origin[0] - h_shift, origin[1] - h_shift, origin[2] - v_shift), (origin[0] + overall_width + h_shift, origin[1] + overall_breadth + h_shift, origin[2] - v_shift - step_height), "column1_4")
        brushes.append(step)

    # return brushes and also the bounds as corners of a cuboid, for use in making a surrounding room later
    return {"brushes": brushes, "corner_a": (origin[0], origin[1], origin[2] - (step_height * NUM_STEPS)), "corner_b": (origin[0] + overall_width, origin[1] + overall_breadth, origin[2] + full_column_height + entab_height + corn_height)}
            
