import random
from datetime import datetime, timedelta, date
import streamlit as st

st.set_page_config(
    page_title="The Pellet Smokehouse",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 82% 0%, rgba(137,70,31,.35) 0%, transparent 26%),
            linear-gradient(140deg, #100d0b 0%, #1d1713 48%, #0d0c0b 100%);
        color: #f6eee6;
    }
    .block-container {max-width:1320px;padding-top:1.6rem;padding-bottom:4rem;}
    .hero {
        padding:34px;border-radius:26px;
        background:linear-gradient(120deg,rgba(94,49,25,.92),rgba(29,23,20,.96));
        border:1px solid rgba(255,180,100,.25);
        margin-bottom:22px;box-shadow:0 14px 40px rgba(0,0,0,.26);
    }
    .hero h1 {font-size:clamp(2.3rem,5vw,4.3rem);margin:0 0 10px;color:#ffb45c;}
    .hero p {font-size:1.05rem;color:#d8c7b5;max-width:780px;margin:0;}
    .eyebrow {text-transform:uppercase;letter-spacing:2px;font-size:.76rem;color:#d89a61;font-weight:700;}
    .section-title {font-size:1.45rem;font-weight:800;color:#ffc078;margin-top:25px;margin-bottom:10px;}
    .subtle {color:#bfae9e;font-size:.94rem;margin-top:-3px;margin-bottom:12px;}
    .animal-card,.recipe-card,.metric,.veg-card {
        background:rgba(31,25,22,.94);
        border:1px solid rgba(255,180,100,.18);
        border-radius:18px;
    }
    .animal-card {padding:10px;}
    .recipe-card {padding:20px;margin:10px 0;}
    .selected-chip {
        display:inline-block;padding:8px 13px;border-radius:999px;
        border:1px solid rgba(255,180,100,.32);
        background:rgba(242,140,40,.13);color:#ffc078;font-weight:750;margin:4px 0 10px;
    }
    .recipe-hero {
        background:linear-gradient(135deg,rgba(111,55,26,.92),rgba(31,25,22,.96));
        border:1px solid rgba(255,180,100,.27);
        padding:25px;border-radius:20px;margin-top:14px;
    }
    .recipe-hero h2 {margin:0;color:#ffbd78;font-size:2rem;}
    .recipe-hero p {color:#d8c7b5;margin-bottom:0;}
    .metric {padding:18px;min-height:118px;}
    .metric-label {color:#b7a593;font-size:.73rem;text-transform:uppercase;letter-spacing:1.45px;font-weight:750;}
    .metric-value {font-size:1.35rem;line-height:1.1;font-weight:850;margin-top:10px;color:#f9eee4;}
    .metric-value.orange {color:#ff9f43;font-size:2rem;}
    .timeline {padding-left:28px;margin:8px 0 16px 8px;border-left:2px solid rgba(255,165,79,.28);}
    .timeline-item {
        position:relative;margin:0 0 17px;padding:14px 16px;
        background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.065);border-radius:14px;
    }
    .timeline-time {color:#ffb66d;font-weight:850;}
    .timeline-title {color:#f7eee7;font-weight:800;}
    .timeline-note {color:#baa99b;font-size:.9rem;margin-top:3px;}
    .veg-card {text-align:center;padding:15px 10px;min-height:128px;background:rgba(255,255,255,.045);}
    .veg-icon {font-size:3.2rem;}
    .rub-box {
        padding:18px;border-radius:16px;
        background:linear-gradient(120deg,rgba(119,60,27,.55),rgba(48,36,29,.82));
        border:1px solid rgba(255,180,100,.18);
    }
    .step-row {display:flex;gap:13px;align-items:flex-start;padding:15px 0;border-bottom:1px solid rgba(255,255,255,.07);}
    .step-num {
        flex:0 0 34px;height:34px;border-radius:50%;display:grid;place-items:center;
        background:#a95023;color:white;font-weight:850;
    }
    .step-copy {color:#e8ddd3;line-height:1.55;}
    .footer-note {color:#9c8b7d;font-size:.83rem;padding-top:10px;}
    div.stButton > button {
        background:linear-gradient(90deg,#9d421b,#d46929);color:white;
        border:1px solid rgba(255,180,100,.17);border-radius:14px;font-weight:800;min-height:47px;
    }
    div.stButton > button:hover {
        background:linear-gradient(90deg,#b9501f,#ef8237);color:white;border-color:rgba(255,190,120,.34);
    }
    .stDownloadButton > button {width:100%;min-height:45px;border-radius:13px;font-weight:750;}
    </style>
    """,
    unsafe_allow_html=True,
)

ANIMALS = {
    "Beef": {
        "icon": "🐂",
        "image": "https://images.unsplash.com/photo-1588347818036-558601350947?auto=format&fit=crop&w=900&q=82",
        "cuts": ["Brisket","Tri-Tip","Chuck Roast","Beef Ribs","Ribeye","Tenderloin"],
    },
    "Pork": {
        "icon": "🐖",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=82",
        "cuts": ["Pork Butt","Baby Back Ribs","Spare Ribs","Pork Tenderloin","Pork Chops","Pork Belly"],
    },
    "Chicken": {
        "icon": "🐓",
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=900&q=82",
        "cuts": ["Whole Chicken","Chicken Wings","Chicken Thighs","Chicken Breast","Drumsticks"],
    },
    "Turkey": {
        "icon": "🦃",
        "image": "https://images.unsplash.com/photo-1574672280600-4accfa5b6f98?auto=format&fit=crop&w=900&q=82",
        "cuts": ["Whole Turkey","Turkey Breast","Turkey Legs"],
    },
    "Fish / Seafood": {
        "icon": "🐟",
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=82",
        "cuts": ["Salmon","Trout","Shrimp","Scallops"],
    },
}

VEGETABLES = {
    "Corn": {"icon":"🌽","mins":55,"note":"Butter, salt, pepper; rotate once."},
    "Potatoes": {"icon":"🥔","mins":110,"note":"Oil + kosher salt; cook until probe tender."},
    "Sweet Potatoes": {"icon":"🍠","mins":95,"note":"Oil lightly; finish with butter."},
    "Asparagus": {"icon":"🌿","mins":28,"note":"Olive oil, SPG; keep a little bite."},
    "Bell Peppers": {"icon":"🫑","mins":38,"note":"Quarter, oil lightly, smoke until softened."},
    "Jalapeños": {"icon":"🌶️","mins":38,"note":"Whole or stuffed; great late-cook side."},
    "Mushrooms": {"icon":"🍄","mins":38,"note":"Butter, garlic, Worcestershire."},
    "Onions": {"icon":"🧅","mins":60,"note":"Thick slices or quarters; butter helps."},
    "Zucchini": {"icon":"🥒","mins":30,"note":"Lengthwise, light oil; don't overcook."},
    "Brussels Sprouts": {"icon":"🥬","mins":48,"note":"Halve, oil, salt, pepper; finish hot."},
}

FLAVOR_DATA = {
    "Classic BBQ": {
        "rub":"Kosher salt • coarse black pepper • paprika • garlic powder • onion powder • brown sugar",
        "finish":"Your favorite BBQ sauce, applied only near the end so the sugar doesn't burn.",
    },
    "Texas Salt & Pepper": {
        "rub":"2 parts coarse black pepper • 1 part kosher salt • light garlic powder",
        "finish":"Usually no sauce. Let the bark and smoke do the talking.",
    },
    "Sweet & Smoky": {
        "rub":"Brown sugar • smoked paprika • kosher salt • black pepper • garlic • chili powder",
        "finish":"Light honey-BBQ glaze during the final 20–30 minutes.",
    },
    "Spicy Cajun": {
        "rub":"Kosher salt • black pepper • cayenne • paprika • garlic • oregano • thyme",
        "finish":"Hot honey or a thin Cajun butter at the end.",
    },
    "Garlic Herb": {
        "rub":"Kosher salt • cracked pepper • garlic • rosemary • thyme • olive oil",
        "finish":"Brush with garlic-herb butter during the rest.",
    },
    "Bourbon Brown Sugar": {
        "rub":"Brown sugar • kosher salt • pepper • smoked paprika • garlic",
        "finish":"Bourbon-brown-sugar glaze near the end of the cook.",
    },
    "Carolina": {
        "rub":"Kosher salt • pepper • paprika • mustard powder • brown sugar",
        "finish":"Tangy vinegar-pepper sauce after slicing or pulling.",
    },
    "Southwest": {
        "rub":"Kosher salt • cumin • ancho chili • smoked paprika • garlic • oregano",
        "finish":"Lime, cilantro, and a thin chipotle finishing sauce.",
    },
}

COOK_STYLES = ["Classic Smoke","Low & Slow","Hot & Fast","Reverse Sear"]
DISH_TYPES = ["Smokehouse Plate","Sandwiches","Tacos","Game Day","Family Dinner"]

COOK_DATA = {
    "Brisket": dict(pit=225,finish="200–205°F + probe tender",pellet="Post Oak",hours_per_lb=1.05,fixed_hours=None,rest_hours=1.5,rest_text="1–2 hours",wrap="Optional around 165–175°F once bark is set",note="Probe tenderness matters more than the final number."),
    "Tri-Tip": dict(pit=225,finish="130–135°F for medium-rare",pellet="Oak / Hickory",hours_per_lb=None,fixed_hours=2.0,rest_hours=.25,rest_text="15 minutes",wrap="Do not wrap",note="Best with a reverse sear at the end."),
    "Chuck Roast": dict(pit=250,finish="200–205°F + probe tender",pellet="Hickory",hours_per_lb=1.15,fixed_hours=None,rest_hours=.75,rest_text="45–60 minutes",wrap="Wrap or pan around 165–175°F",note="Treat it like a small brisket."),
    "Beef Ribs": dict(pit=250,finish="200–205°F + probe tender",pellet="Oak",hours_per_lb=None,fixed_hours=7.0,rest_hours=.5,rest_text="30 minutes",wrap="Usually no wrap unless color gets too dark",note="Probe between the bones for tenderness."),
    "Ribeye": dict(pit=225,finish="125–135°F depending on preference",pellet="Oak",hours_per_lb=None,fixed_hours=1.15,rest_hours=.17,rest_text="10 minutes",wrap="Do not wrap",note="Reverse sear gives the best crust."),
    "Tenderloin": dict(pit=225,finish="130–135°F for medium-rare",pellet="Cherry / Oak",hours_per_lb=None,fixed_hours=1.5,rest_hours=.25,rest_text="15 minutes",wrap="Do not wrap",note="Pull early and avoid overcooking this lean cut."),
    "Pork Butt": dict(pit=250,finish="200–205°F + probe tender",pellet="Hickory / Apple",hours_per_lb=1.15,fixed_hours=None,rest_hours=1.0,rest_text="1–2 hours",wrap="Wrap or pan around 165–175°F after bark sets",note="Bone should wiggle freely when it's ready to pull."),
    "Baby Back Ribs": dict(pit=250,finish="Tender; typically around 195–203°F",pellet="Apple / Cherry",hours_per_lb=None,fixed_hours=5.0,rest_hours=.2,rest_text="10–15 minutes",wrap="Optional 1–2 hour wrap after color develops",note="Use bend and toothpick tenderness, not only temperature."),
    "Spare Ribs": dict(pit=250,finish="Tender; typically around 195–203°F",pellet="Hickory / Cherry",hours_per_lb=None,fixed_hours=5.75,rest_hours=.2,rest_text="10–15 minutes",wrap="Optional once bark and color are right",note="Cook until the rack bends easily."),
    "Pork Tenderloin": dict(pit=250,finish="145°F",pellet="Apple",hours_per_lb=None,fixed_hours=1.25,rest_hours=.17,rest_text="10 minutes",wrap="Do not wrap",note="Lean cut—watch internal temperature closely."),
    "Pork Chops": dict(pit=250,finish="145°F",pellet="Apple / Maple",hours_per_lb=None,fixed_hours=1.1,rest_hours=.13,rest_text="8 minutes",wrap="Do not wrap",note="Thick-cut chops work best."),
    "Pork Belly": dict(pit=250,finish="195–205°F depending on texture",pellet="Cherry / Hickory",hours_per_lb=None,fixed_hours=5.0,rest_hours=.33,rest_text="20 minutes",wrap="Optional pan/cover during tenderizing",note="Excellent for burnt ends."),
    "Whole Chicken": dict(pit=325,finish="Breast 165°F / thigh 175°F",pellet="Apple / Pecan",hours_per_lb=None,fixed_hours=2.0,rest_hours=.25,rest_text="15 minutes",wrap="Do not wrap",note="Higher pit heat helps the skin render."),
    "Chicken Wings": dict(pit=375,finish="175–185°F for tender wings",pellet="Cherry",hours_per_lb=None,fixed_hours=1.0,rest_hours=.08,rest_text="5 minutes",wrap="Do not wrap",note="Finish hotter for crispier skin."),
    "Chicken Thighs": dict(pit=325,finish="175–185°F",pellet="Pecan / Apple",hours_per_lb=None,fixed_hours=1.25,rest_hours=.13,rest_text="8 minutes",wrap="Do not wrap",note="Dark meat benefits from higher finishing temperature."),
    "Chicken Breast": dict(pit=275,finish="165°F",pellet="Apple",hours_per_lb=None,fixed_hours=1.15,rest_hours=.17,rest_text="10 minutes",wrap="Do not wrap",note="Pull promptly at safe temperature."),
    "Drumsticks": dict(pit=350,finish="175–185°F",pellet="Cherry / Pecan",hours_per_lb=None,fixed_hours=1.0,rest_hours=.08,rest_text="5 minutes",wrap="Do not wrap",note="Sauce late, then let it tack up."),
    "Whole Turkey": dict(pit=325,finish="Breast 165°F / thigh 175°F",pellet="Apple / Pecan",hours_per_lb=.22,fixed_hours=None,rest_hours=.5,rest_text="30–45 minutes",wrap="Do not wrap whole bird",note="Verify both breast and thigh."),
    "Turkey Breast": dict(pit=275,finish="165°F",pellet="Apple",hours_per_lb=None,fixed_hours=3.0,rest_hours=.33,rest_text="20 minutes",wrap="Optional late foil if color is sufficient",note="A light brine is a strong play."),
    "Turkey Legs": dict(pit=300,finish="175–185°F",pellet="Hickory / Apple",hours_per_lb=None,fixed_hours=2.5,rest_hours=.25,rest_text="15 minutes",wrap="Optional late wrap",note="Cook until tender, not merely safe."),
    "Salmon": dict(pit=225,finish="135–145°F",pellet="Alder / Apple",hours_per_lb=None,fixed_hours=1.0,rest_hours=.08,rest_text="5 minutes",wrap="Do not wrap",note="Pull at the lower end for a softer center."),
    "Trout": dict(pit=225,finish="145°F",pellet="Alder",hours_per_lb=None,fixed_hours=.9,rest_hours=.08,rest_text="5 minutes",wrap="Do not wrap",note="Delicate smoke is the goal."),
    "Shrimp": dict(pit=300,finish="Opaque and firm",pellet="Apple / Alder",hours_per_lb=None,fixed_hours=.45,rest_hours=0.0,rest_text="Serve immediately",wrap="Do not wrap",note="These move fast—don't walk away."),
    "Scallops": dict(pit=275,finish="125–130°F",pellet="Alder / Apple",hours_per_lb=None,fixed_hours=.55,rest_hours=.05,rest_text="3 minutes",wrap="Do not wrap",note="Dry the surface well before seasoning."),
}

def fmt_time(dt_obj):
    return dt_obj.strftime("%a %b %d • %I:%M %p").replace(" 0"," ")

def estimate_cook_hours(cook, weight_lb, style):
    hours = cook["hours_per_lb"] * weight_lb if cook["hours_per_lb"] is not None else cook["fixed_hours"]
    if style == "Hot & Fast":
        hours *= .82
    elif style == "Low & Slow":
        hours *= 1.12
    elif style == "Reverse Sear":
        hours *= 1.05
    return max(hours, .35)

def adjusted_pit_temp(base_temp, style, cut):
    if style == "Hot & Fast":
        return min(base_temp + 50, 400)
    if style == "Low & Slow":
        return min(base_temp, 250)
    if style == "Reverse Sear" and cut in {"Ribeye","Tri-Tip","Tenderloin"}:
        return 225
    return base_temp

def rub_quantity(weight_lb):
    tbsp = max(2.0, weight_lb * .55)
    if tbsp < 4:
        return f"about {tbsp:.1f} tbsp total rub"
    cups = tbsp / 16
    return f"about {cups:.1f} cup total rub" if cups >= .5 else f"about {tbsp:.0f} tbsp total rub"

def build_recipe_text(recipe):
    lines = [
        f"# {recipe['title']}",
        "",
        f"Protein: {recipe['animal']} — {recipe['cut']} ({recipe['weight']:.1f} lb)",
        f"Style: {recipe['style']}",
        f"Dish: {recipe['dish']}",
        f"Flavor: {recipe['flavor']}",
        f"Pellets: {recipe['pellets']}",
        f"Pit temperature: {recipe['pit_temp']}°F",
        f"Target: {recipe['finish']}",
        f"Estimated cook: {recipe['cook_hours']:.1f} hr",
        f"Rest: {recipe['rest_text']}",
        "",
        "## Rub",
        recipe["rub"],
        f"Planning quantity: {recipe['rub_qty']}",
        "",
        "## Finish",
        recipe["finish_sauce"],
        "",
        "## Timeline",
    ]
    for item in recipe["timeline"]:
        lines.append(f"- {fmt_time(item['time'])}: {item['title']} — {item['note']}")
    lines.extend(["","## Cook Steps"])
    for i, step in enumerate(recipe["steps"],1):
        lines.append(f"{i}. {step}")
    if recipe["veggies"]:
        lines.extend(["","## Sides"])
        for veg in recipe["veggies"]:
            lines.append(f"- {VEGETABLES[veg]['icon']} {veg}: {VEGETABLES[veg]['note']} Add around {fmt_time(recipe['veg_times'][veg])}.")
    lines.extend(["","## Pitmaster Note",recipe["tip"],"","Use a reliable thermometer and follow safe food handling practices."])
    return "\n".join(lines)

if "animal" not in st.session_state:
    st.session_state["animal"] = "Beef"
if "last_recipe" not in st.session_state:
    st.session_state["last_recipe"] = None

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">PELLET GRILL COMMAND CENTER</div>
        <h1>The Pellet Smokehouse</h1>
        <p>
            Pick the protein, set the weight and dinner time, choose the flavor,
            and get a backwards-planned cook schedule — including meat-on time,
            bark check, side timing, resting window, and dinner.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""<div class="section-title">1. Pick your protein</div>""", unsafe_allow_html=True)
st.markdown("""<div class="subtle">Start with the animal, then narrow the cook.</div>""", unsafe_allow_html=True)

animal_cols = st.columns(len(ANIMALS))
for col, (animal_name, info) in zip(animal_cols, ANIMALS.items()):
    with col:
        try:
            st.image(info["image"], use_container_width=True)
        except Exception:
            st.markdown(f"<div style='font-size:64px;text-align:center'>{info['icon']}</div>", unsafe_allow_html=True)
        if st.button(f"{info['icon']} {animal_name}", key=f"animal_{animal_name}", use_container_width=True):
            st.session_state["animal"] = animal_name

animal = st.session_state["animal"]
st.markdown(f"""<div class="selected-chip">{ANIMALS[animal]["icon"]} Selected: {animal}</div>""", unsafe_allow_html=True)

st.markdown("""<div class="section-title">2. Build the main dish</div>""", unsafe_allow_html=True)
c1,c2,c3 = st.columns([1.2,1,1.2])
with c1:
    cut = st.selectbox("Cut", ANIMALS[animal]["cuts"])
with c2:
    default_weight = 9.0 if cut in {"Brisket","Pork Butt"} else 3.0
    weight_lb = st.number_input("Weight (lb)", min_value=.25, max_value=40.0, value=float(default_weight), step=.25)
with c3:
    dish_type = st.selectbox("What are we making?", DISH_TYPES)

st.markdown("""<div class="section-title">3. Set the smoke profile</div>""", unsafe_allow_html=True)
p1,p2,p3 = st.columns(3)
with p1:
    cook_style = st.selectbox("Cook style", COOK_STYLES)
with p2:
    flavor = st.selectbox("Flavor profile", list(FLAVOR_DATA.keys()))
with p3:
    preferred_wood = st.selectbox("Pellet strategy", ["Use recommended wood","Oak-forward","Hickory-forward","Fruitwood-forward"])

st.markdown("""<div class="section-title">4. What's riding shotgun?</div>""", unsafe_allow_html=True)
st.markdown("""<div class="subtle">Choose vegetables and I'll time them to the main dish.</div>""", unsafe_allow_html=True)

selected_veggies = st.multiselect(
    "Vegetables",
    list(VEGETABLES.keys()),
    default=["Corn","Potatoes"],
    format_func=lambda name: f"{VEGETABLES[name]['icon']} {name}",
    label_visibility="collapsed",
)

if selected_veggies:
    veg_cols = st.columns(min(len(selected_veggies),5))
    for i, veg in enumerate(selected_veggies):
        with veg_cols[i % len(veg_cols)]:
            st.markdown(
                f"""
                <div class="veg-card">
                    <div class="veg-icon">{VEGETABLES[veg]["icon"]}</div>
                    <strong>{veg}</strong><br>
                    <span style="color:#ab9a8c;font-size:.82rem;">~{VEGETABLES[veg]["mins"]} min</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("""<div class="section-title">5. Tell me when we're eating</div>""", unsafe_allow_html=True)
today = date.today()
d1,d2,d3,d4 = st.columns(4)
with d1:
    dinner_date = st.date_input("Dinner date", value=today)
with d2:
    dinner_time = st.time_input("Dinner time", value=datetime.strptime("18:00","%H:%M").time())
with d3:
    bark_level = st.slider("Bark / char",0,5,4)
with d4:
    heat_level = st.slider("Heat 🌶️",0,5,2)

st.divider()

if st.button("🔥 BUILD MY COOK PLAN", use_container_width=True):
    cook = COOK_DATA[cut]
    pit_temp = adjusted_pit_temp(cook["pit"], cook_style, cut)
    cook_hours = estimate_cook_hours(cook, weight_lb, cook_style)

    pellets = {
        "Use recommended wood": cook["pellet"],
        "Oak-forward": "Oak blend",
        "Hickory-forward": "Hickory blend",
        "Fruitwood-forward": "Apple / Cherry fruitwood blend",
    }[preferred_wood]

    dinner_dt = datetime.combine(dinner_date, dinner_time)
    buffer_hours = 1.25 if cook_hours >= 8 else .75 if cook_hours >= 4 else .35
    meat_on = dinner_dt - timedelta(hours=cook_hours + cook["rest_hours"] + buffer_hours)
    preheat = meat_on - timedelta(minutes=25)
    bark_check = meat_on + timedelta(hours=cook_hours * (.42 if cook_hours >= 5 else .50))
    start_probe = meat_on + timedelta(hours=cook_hours * .82)
    target_pull = dinner_dt - timedelta(hours=cook["rest_hours"])
    slice_time = dinner_dt - timedelta(minutes=5)

    veg_times = {veg: dinner_dt - timedelta(minutes=VEGETABLES[veg]["mins"]) for veg in selected_veggies}

    timeline = [
        {"time":preheat,"title":"Preheat smoker","note":f"Set to {pit_temp}°F and load {pellets} pellets."},
        {"time":meat_on,"title":f"{cut} goes on","note":"Insert a probe in the thickest appropriate section."},
        {"time":bark_check,"title":"First real check","note":f"Assess color and bark. {cook['wrap']}."},
        {"time":start_probe,"title":"Start watching tenderness","note":f"Target: {cook['finish']}. {cook['note']}"},
        {"time":target_pull,"title":"Target pull window","note":f"Rest guidance: {cook['rest_text']}. Build in flexibility."},
        {"time":slice_time,"title":"Slice / pull / sauce","note":f"Finish for a {dish_type.lower()} and get it to the table."},
        {"time":dinner_dt,"title":"EAT","note":"The whole plan has been backed into this time."},
    ]
    for veg in selected_veggies:
        timeline.append({"time":veg_times[veg],"title":f"Add {veg}","note":VEGETABLES[veg]["note"]})
    timeline = sorted(timeline, key=lambda item: item["time"])

    flavor_info = FLAVOR_DATA[flavor]
    qty = rub_quantity(weight_lb)
    extra_heat = " Add cayenne, jalapeño powder, or extra cracked pepper to taste." if heat_level >= 4 else " Keep the heat components very light." if heat_level == 0 else ""
    bark_note = "Prioritize surface drying and leave it unwrapped longer for darker bark." if bark_level >= 4 else "Wrap once color is right if you want a softer exterior."

    steps = [
        f"Trim and prep the {cut}. Remove loose pieces and excessive hard fat where appropriate.",
        f"Season evenly with the {flavor} profile. Plan on {qty}.{extra_heat}",
        f"Preheat the pellet grill to {pit_temp}°F using {pellets}.",
        f"Put the {cut} on the smoker and place your probe correctly. Keep the lid closed as much as possible.",
        f"At the first bark/color check: {cook['wrap']}. {bark_note}",
        f"Cook toward {cook['finish']}. Finish temperature is a guide; texture and tenderness still win.",
        f"Pull when ready and rest for {cook['rest_text']}.",
        f"Finish with: {flavor_info['finish']}",
        f"Serve as a {dish_type.lower()} at {dinner_dt.strftime('%I:%M %p').lstrip('0')}.",
    ]

    title = {
        "Classic BBQ":f"Backyard Pitmaster {cut}",
        "Texas Salt & Pepper":f"Texas-Style {cut}",
        "Sweet & Smoky":f"Sweet Smoke {cut}",
        "Spicy Cajun":f"Cajun Fire {cut}",
        "Garlic Herb":f"Garlic-Herb Smoked {cut}",
        "Bourbon Brown Sugar":f"Bourbon Brown Sugar {cut}",
        "Carolina":f"Carolina Smokehouse {cut}",
        "Southwest":f"Southwest Smoked {cut}",
    }[flavor]

    tips = [
        "If you're looking, you ain't cooking. Open the lid with a purpose.",
        "Cook to tenderness and internal temperature; the clock is a planning tool, not the boss.",
        "Clean, steady smoke beats heavy smoke every time.",
        "On big cuts, a long rest is part of the cook—not dead time.",
        "Get the smoke on early, then manage color and tenderness.",
        "Don't chase every little pit-temperature swing. Pellet grills breathe.",
    ]

    st.session_state["last_recipe"] = {
        "title":title,"animal":animal,"cut":cut,"weight":weight_lb,"dish":dish_type,"style":cook_style,
        "flavor":flavor,"pellets":pellets,"pit_temp":pit_temp,"finish":cook["finish"],"cook_hours":cook_hours,
        "rest_text":cook["rest_text"],"rub":flavor_info["rub"],"rub_qty":qty,"finish_sauce":flavor_info["finish"],
        "timeline":timeline,"steps":steps,"veggies":selected_veggies,"veg_times":veg_times,"tip":random.choice(tips),
        "dinner_dt":dinner_dt,"meat_on":meat_on,
    }

recipe = st.session_state.get("last_recipe")

if recipe:
    st.markdown(
        f"""
        <div class="recipe-hero">
            <div class="eyebrow">YOUR COOK PLAN</div>
            <h2>🔥 {recipe["title"]}</h2>
            <p>
                {ANIMALS[recipe["animal"]]["icon"]} {recipe["animal"]} •
                {recipe["cut"]} • {recipe["weight"]:.1f} lb •
                {recipe["style"]} • {recipe["flavor"]}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1,m2,m3,m4,m5 = st.columns(5)
    metric_data = [
        ("PIT TEMP",f'{recipe["pit_temp"]}°F',"orange"),
        ("TARGET",recipe["finish"],""),
        ("EST. COOK",f'{recipe["cook_hours"]:.1f} hr',""),
        ("MEAT ON",recipe["meat_on"].strftime("%I:%M %p").lstrip("0"),""),
        ("PELLETS",recipe["pellets"],""),
    ]
    for col,(label,value,extra) in zip([m1,m2,m3,m4,m5],metric_data):
        with col:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value {extra}">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    left,right = st.columns([1.2,1])
    with left:
        st.markdown("## ⏱️ Cook Timeline")
        st.markdown('<div class="timeline">', unsafe_allow_html=True)
        for item in recipe["timeline"]:
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">{fmt_time(item["time"])}</div>
                    <div class="timeline-title">{item["title"]}</div>
                    <div class="timeline-note">{item["note"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("## 🧂 Rub & Finish")
        st.markdown(
            f"""
            <div class="rub-box">
                <strong>{recipe["flavor"]}</strong><br><br>
                {recipe["rub"]}<br><br>
                <span style="color:#ffbd78;font-weight:800;">Amount:</span>
                {recipe["rub_qty"]}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="recipe-card">
                <div class="metric-label">FINISH / SAUCE</div>
                <div style="margin-top:8px;color:#e9ded4;">{recipe["finish_sauce"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### 🪵 Pitmaster Note")
        st.info(recipe["tip"])

    st.markdown("## 🔥 Step-by-Step")
    for idx, step in enumerate(recipe["steps"],1):
        st.markdown(
            f"""
            <div class="step-row">
                <div class="step-num">{idx}</div>
                <div class="step-copy">{step}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if recipe["veggies"]:
        st.markdown("## 🥕 Side Timing")
        side_cols = st.columns(min(len(recipe["veggies"]),3))
        for i, veg in enumerate(recipe["veggies"]):
            with side_cols[i % len(side_cols)]:
                st.markdown(
                    f"""
                    <div class="recipe-card">
                        <div style="font-size:3rem;">{VEGETABLES[veg]["icon"]}</div>
                        <h3 style="margin-bottom:5px;">{veg}</h3>
                        <div style="color:#ffb66d;font-weight:800;">
                            ON: {recipe["veg_times"][veg].strftime("%I:%M %p").lstrip("0")}
                        </div>
                        <div style="color:#baa99b;font-size:.9rem;margin-top:8px;">
                            {VEGETABLES[veg]["note"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("## 📄 Take the Plan With You")
    recipe_text = build_recipe_text(recipe)
    dl1,dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "⬇️ Download Cook Plan (.md)",
            data=recipe_text,
            file_name="pellet_smokehouse_cook_plan.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with dl2:
        if st.button("🔄 Clear Cook Plan", use_container_width=True):
            st.session_state["last_recipe"] = None
            st.rerun()

    st.markdown(
        """
        <div class="footer-note">
            Planning times are estimates. Meat thickness, starting temperature, weather,
            grill behavior, and the stall can move the schedule. Use a reliable thermometer.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.caption("Make your selections, choose your dinner time, then hit BUILD MY COOK PLAN.")
