import random

REGION_COEFFICIENT = {
    "Toshkent": 1.2,
    "Samarqand": 1.0,
    "Qashqadaryo": 0.9
}

MATERIAL_MULTIPLIER = {
    "Brick": 1.0,
    "Concrete": 1.3,
    "Frame": 0.8
}

def calculate_materials(area, floors, material, region):

    region_coef = REGION_COEFFICIENT[region]
    material_coef = MATERIAL_MULTIPLIER[material]

    total_area = area * floors

    concrete = total_area * 0.25 * material_coef
    bricks = total_area * 120 * material_coef
    rebar = total_area * 8 * material_coef
    roof = total_area * 1.1

    base_cost = total_area * 300
    total_cost = base_cost * region_coef * material_coef

    return {
        "Concrete (m3)": round(concrete, 2),
        "Bricks (pcs)": int(bricks),
        "Rebar (kg)": round(rebar, 2),
        "Roof material (m2)": round(roof, 2),
        "Estimated Cost ($)": round(total_cost, 2)
    }