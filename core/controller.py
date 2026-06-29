import param
import asyncio
import pydeck as pdk
from data.pipeline import generate_mock_layer

class DigitalTwinController(param.Parameterized):
    """
    Central operational engine for the MugizhNokku application state.
    """
    # Interactive App States
    current_tab = param.String(default="TELEMETRY")
    prediction_data = param.List(default=[])
    
    # Live Tracked Analytical Parameters
    peak_intensity = param.String(default="0.0%")
    grid_average = param.String(default="0.0 mm")
    prediction_window = param.String(default="T+0 HOURS")
    
    # Simulation Control Parameters
    scenario_preset = param.Selector(default="Live Telemetry", objects=["Live Telemetry", "2018 Kerala Floods", "2023 Cyclone Biparjoy"])
    sst_shift = param.Number(default=0.0)
    moisture_mult = param.Number(default=1.0)
    
    # Pitch Sequence Interactive UI States
    is_calculating = param.Boolean(default=False)
    map_style = param.String(default=pdk.map_styles.CARTO_DARK)
    alert_message = param.String(default="")
    
    def __init__(self, **params):
        super().__init__(**params)
        self.update_layer_state() # Populate initial baseline metrics state

    def route_navigation(self, target_tab):
        """
        Updates the global layout viewport context state across tabs.
        """
        self.current_tab = target_tab
        print(f"[SYSTEM BACKEND] Context view switched to: {target_tab}")

    @param.depends('sst_shift', 'moisture_mult', watch=True)
    def trigger_generation(self):
        """Re-generates tensor when parameters shift"""
        self.update_layer_state()
        
    @param.depends('scenario_preset', watch=True)
    def apply_scenario(self):
        """Hard-snaps interactive parameters to trigger extreme historical scenario mathematical logic"""
        if self.scenario_preset == "2018 Kerala Floods":
            self.sst_shift = 3.2
            self.moisture_mult = 2.0
            self.alert_message = "CRITICAL ALERT: Orographic Ridge Inundation Threshold Exceeded - Regional Evacuation Protocol Inferred"
        elif self.scenario_preset == "2023 Cyclone Biparjoy":
            self.sst_shift = 3.8
            self.moisture_mult = 1.4
            self.alert_message = ""
        elif self.scenario_preset == "Live Telemetry":
            self.sst_shift = 0.0
            self.moisture_mult = 1.0
            self.alert_message = ""
            
    async def trigger_simulation_run(self):
        """Asynchronous trigger to build dramatic tension without blocking Tornado."""
        self.is_calculating = True
        await asyncio.sleep(1.5)
        self.update_layer_state()
        self.is_calculating = False
        
    def update_layer_state(self):
        """Calls the data pipeline to get new tensor payload."""
        payload, max_val, mean_val = generate_mock_layer(self.sst_shift, self.moisture_mult)
        self.prediction_data = payload
        self.peak_intensity = max_val
        self.grid_average = mean_val
        self.prediction_window = "T+24 HOURS" if self.current_tab == "PREDICT" else "LIVE TELEMETRY"
