# PS-5 Bharatiya Antariksh Hackathon 2026: AI-Powered Digital Twin

## Problem Statement
An "AI-powered Digital Twin of India's Climate using national datasets" refers to the creation of a high-fidelity, dynamic virtual replica of India's climate system that continuously evolves using real-time and historical observations. 
This digital twin integrates multi-source data from Indian satellites (INSAT, Oceansat), ground-based meteorological networks (IMD), reanalysis products, and hydrological datasets.

## Workflow Goals
1. **Problem Definition:** Select region & variable.
2. **Data Ingestion:** Rainfall & Temperature.
3. **Data Pre-processing:** Spatial masking, normalization, interpolation.
4. **Model Development:** ML/DL based model generates T+1 forecast.
5. **Visualization:** Interactive dashboard (Streamlit, CesiumJS, PyDeck).
6. **What-If Simulations:** Scenario testing.

## Datasets
- **IMD:** High-resolution gridded rainfall and temperature.
- **MOSDAC INSAT:** LST (Land Surface Temp), SST (Sea Surface Temp), IMC (Rainfall).
