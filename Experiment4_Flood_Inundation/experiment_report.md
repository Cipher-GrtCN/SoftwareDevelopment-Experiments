# Experiment 4: Flood Inundation Analysis (DEM-based)

## Experiment Information
- **Course**: AI-Augmented Software Engineering
- **Module**: Smart Water Lab Series - Week 6 Session B
- **Duration**: 2 hours
- **Date**: 2026-07-07

---

## 1. Experiment Objectives

1. Process Digital Elevation Model (DEM) data
2. Implement spatial comparison algorithms for flood detection
3. Create visual flood extent maps using matplotlib
4. Calculate flooded area percentages
5. Validate that flooded area increases with water level

---

## 2. Physical Background

### Digital Elevation Models (DEM)
A DEM is a 2D grid where each cell contains an elevation value (in meters). Common sources include USGS SRTM (30m resolution) and ALOS PALSAR (12.5m resolution).

### Flood Inundation Logic
A location is **FLOODED** if:
```
Elevation < Flood_Water_Level
```

Inundation Depth:
```
Depth = Flood_Water_Level - Elevation (if flooded)
Depth = 0 (if not flooded)
```

Flooded Area Percentage:
```
% = (Number of flooded cells / Total cells) x 100
```

---

## 3. Methodology

### 3.1 DEM Data Preparation
- Generated synthetic 100x100 DEM with elevation range 30-80m
- Created terrain with hills, valleys, and surface roughness
- Saved DEM data as numpy file for reproducibility

### 3.2 Flood Simulation
- Implemented `simulate_flood(dem, water_level)` function
- Used boolean masking for flooded cell detection
- Calculated inundation depth and flooded percentage

### 3.3 Visualization
- Created original DEM visualization (terrain colormap)
- Generated flood extent overlay (blue tones, semi-transparent)
- Produced inundation depth heatmaps
- Made side-by-side comparisons at different water levels

### 3.4 Dynamic Simulation
- Simulated water level rising from 35m to 55m
- Recorded flooded percentage at each level
- Created water level vs flooded percentage curve

---

## 4. Results

### 4.1 DEM Characteristics
- Grid size: 100 x 100 cells
- Elevation range: 30.0 - 80.0 meters
- Terrain features: Hills, central valley, surface roughness

### 4.2 Flood Simulation Results

| Water Level (m) | Flooded (%) | Avg Depth (m) | Max Depth (m) |
|-----------------|-------------|---------------|---------------|
| 40 | 7.3% | 2.93 | 10.00 |
| 45 | 18.2% | 4.44 | 15.00 |
| 50 | 34.1% | 6.31 | 20.00 |
| 55 | 52.4% | 8.33 | 25.00 |

### 4.3 Dynamic Simulation
- Flooded area increases monotonically from 0% (at 30m) to 100% (at 80m)
- Rate of increase is highest when water level reaches the valley bottom
- Curve shows typical S-shape of cumulative distribution

### 4.4 Physical Validation
All validation checks passed:
- Flooded area increases monotonically with water level
- Maximum depth equals water_level - min_elevation
- Percentage values are in valid range [0, 100]
- Below min elevation: 0% flooded
- Above max elevation: ~100% flooded

---

## 5. Files Delivered

| File | Description |
|------|-------------|
| `flood_inundation.py` | Main implementation |
| `dem_data.npy` | Synthetic DEM data (100x100) |
| `flood_extent_40m.png` | Flood visualization at 40m |
| `flood_extent_50m.png` | Flood visualization at 50m |
| `flood_comparison.png` | Side-by-side comparison |
| `flood_curve.png` | Water level vs flooded percentage |
| `validation_report.txt` | Physical validation results |
| `prompt_log.md` | AI interaction documentation |

---

## 6. Discussion

### Key Findings
1. **Flood Progression**: At 40m water level, only 7.3% of area is flooded (valley only)
2. **Rapid Spread**: Between 45m and 55m, flooded area increases from 18% to 52%
3. **Complete Inundation**: At 80m (max elevation), 100% of area is flooded

### Physical Insights
- Terrain topography controls flood patterns
- Valleys flood first, highlands remain safe longer
- Inundation depth varies significantly across the landscape

### AI Collaboration
- AI successfully generated DEM creation and flood simulation code
- Custom colormap creation improved visualization quality
- Domain knowledge was used to validate monotonicity constraint

### Conclusion
Successfully implemented flood inundation analysis using DEM data. The system correctly identifies flooded areas, calculates inundation depths, and produces informative visualizations. All physical validation checks confirm the correctness of the implementation.
