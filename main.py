import panel as pn
from core.controller import DigitalTwinController
from visualization.map_engine import build_map
import pydeck as pdk

pn.extension('deckgl')

# 1. Initialize the Core State Engine
controller = DigitalTwinController()

# 2. Build out Visualization Layer
def update_deckgl(event):
    data = event.new if event else controller.prediction_data
    deck_obj = build_map(data, controller.map_style)
    deckgl_pane.object = deck_obj

# Initial rendering wrapper
initial_deck = build_map(controller.prediction_data, controller.map_style)
deckgl_pane = pn.pane.DeckGL(initial_deck, sizing_mode='stretch_both', min_height=400)

# Bind state controller to visual map refresh
controller.param.watch(update_deckgl, 'prediction_data')
controller.param.watch(update_deckgl, 'map_style')

# 3. Load Frontend UI Template
with open("frontend/templates/dashboard.html", "r", encoding="utf-8") as f:
    hud_template = f.read()

# 4. Bind UI Components (Buttons and Sliders)
preset_selector = pn.widgets.Select.from_param(controller.param.scenario_preset, name='PRESET SCENARIO')
preset_selector.stylesheets = ["""
    :host { font-family: 'Inter', sans-serif; color: #e5e2e1; }
    .bk-input { background-color: #202020; color: #e5e2e1; border-color: #434652; border-width: 2px; }
"""]
slider_sst = pn.widgets.FloatSlider.from_param(controller.param.sst_shift, name='SST (°C)', start=-2.0, end=4.0, step=0.1, bar_color='#b1c5ff')
slider_moisture = pn.widgets.FloatSlider.from_param(controller.param.moisture_mult, name='Moisture', start=0.5, end=2.0, step=0.1, bar_color='#b1c5ff')
control_block = pn.Column(preset_selector, slider_sst, slider_moisture, width=220)

peak_intensity_pane = pn.pane.HTML(controller.param.peak_intensity, margin=0, sizing_mode='stretch_width')
grid_average_pane = pn.pane.HTML(controller.param.grid_average, margin=0, sizing_mode='stretch_width')
prediction_window_pane = pn.pane.HTML(controller.param.prediction_window, margin=0, sizing_mode='stretch_width')

# Alerts and Loading Overlays
def render_alert(msg):
    if not msg: return ""
    return f'''
    <div class="bg-surface-container-highest border-2 border-error p-container-padding flex items-start space-x-4 w-96 shadow-lg pointer-events-auto">
        <span class="material-symbols-outlined text-error text-3xl" data-icon="warning">warning</span>
        <div>
            <h4 class="font-headline-sm text-headline-sm text-error uppercase mb-1">System Alert</h4>
            <p class="font-body-md text-on-surface">{msg}</p>
        </div>
    </div>
    '''

def render_loading(is_calc):
    if not is_calc: return ""
    return '''
    <div class="absolute inset-0 z-[200] bg-surface/80 backdrop-blur-sm flex flex-col items-center justify-center pointer-events-auto">
        <div class="bg-surface-container-high border-2 border-outline-variant p-8 flex flex-col items-center">
            <span class="material-symbols-outlined text-primary text-5xl mb-4 animate-spin" data-icon="sync">sync</span>
            <div class="font-data-sm text-data-sm text-primary uppercase tracking-widest">
                Processing Telemetry...
            </div>
        </div>
    </div>
    '''
    
alert_pane = pn.pane.HTML(pn.bind(render_alert, controller.param.alert_message), sizing_mode='stretch_width')
loading_pane = pn.pane.HTML(pn.bind(render_loading, controller.param.is_calculating), sizing_mode='fixed', width=0, height=0, margin=0, css_classes=['pointer-events-none'])

# Routing and Event Triggers
nav_satellite_btn = pn.widgets.Button(name='satellite', css_classes=['hidden-satellite-btn'])
nav_radar_btn = pn.widgets.Button(name='radar', css_classes=['hidden-radar-btn'])
run_sim_btn = pn.widgets.Button(name='run', css_classes=['hidden-run-btn'])

def set_satellite(*args): controller.map_style = 'satellite'
def set_radar(*args): controller.map_style = pdk.map_styles.CARTO_DARK

nav_satellite_btn.on_click(set_satellite)
nav_radar_btn.on_click(set_radar)
run_sim_btn.on_click(lambda e: pn.state.execute(controller.trigger_simulation_run))

nav_archive_btn = pn.widgets.Button(name='archive', css_classes=['hidden-archive-btn'])
nav_telemetry_btn = pn.widgets.Button(name='telemetry', css_classes=['hidden-telemetry-btn'])
nav_predict_btn = pn.widgets.Button(name='predict', css_classes=['hidden-predict-btn'])
nav_scenarios_btn = pn.widgets.Button(name='scenarios', css_classes=['hidden-scenarios-btn'])
nav_layers_btn = pn.widgets.Button(name='layers', css_classes=['hidden-layers-btn'])

def route_and_sync(tab_name):
    controller.route_navigation(tab_name)
    controller.update_layer_state()

nav_archive_btn.on_click(lambda e: route_and_sync('ARCHIVE'))
nav_telemetry_btn.on_click(lambda e: route_and_sync('TELEMETRY'))
nav_predict_btn.on_click(lambda e: route_and_sync('PREDICT'))
nav_scenarios_btn.on_click(lambda e: route_and_sync('SCENARIOS'))
nav_layers_btn.on_click(lambda e: route_and_sync('V-LAYERS'))

# 5. Compile into Unified Core Template Object
app_view = pn.Template(hud_template)
app_view.add_panel('map_canvas', deckgl_pane)
app_view.add_panel('alert_modal', alert_pane)
app_view.add_panel('loading_overlay', loading_pane)
app_view.add_panel('nav_satellite_btn', nav_satellite_btn)
app_view.add_panel('nav_radar_btn', nav_radar_btn)
app_view.add_panel('run_sim_btn', run_sim_btn)

app_view.add_panel('control_sliders', control_block)

app_view.add_panel('peak_intensity', peak_intensity_pane)
app_view.add_panel('grid_average', grid_average_pane)
app_view.add_panel('prediction_window', prediction_window_pane)

app_view.add_panel('nav_archive_btn', nav_archive_btn)
app_view.add_panel('nav_telemetry_btn', nav_telemetry_btn)
app_view.add_panel('nav_predict_btn', nav_predict_btn)
app_view.add_panel('nav_scenarios_btn', nav_scenarios_btn)
app_view.add_panel('nav_layers_btn', nav_layers_btn)

app_view.servable()
