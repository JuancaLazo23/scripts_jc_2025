#!/usr/bin/env python3
"""
download_pisco_point.py

Descarga series diarias de:
  - Precipitación
  - Temperatura mínima
  - Temperatura máxima

para un punto geográfico dado (lat, lon) desde PISCOp,
y exporta cada serie a CSV.
"""

import xarray as xr
import pandas as pd

def download_point(lat, lon, out_prefix="pisco_point", start_date=None, end_date=None):
    # URLs DODS
    urls = {
        "precip": "http://iridl.ldeo.columbia.edu/SOURCES/.SENAMHI/.HSR/.PISCO/.Prec/.v2p1/.stable/.daily/dods",
        "tmin":   "http://iridl.ldeo.columbia.edu/SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmin/.stable/.daily/dods",
        "tmax":   "http://iridl.ldeo.columbia.edu/SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmax/.stable/.daily/dods",
    }

    for var, url in urls.items():
        ds = xr.open_dataset(url)
        da = ds[list(ds.data_vars)[0]]  # asume la variable relevante es la primera

        # Selección por punto (nearest grid cell)
        da_pt = da.sel(X=lon, Y=lat, method="nearest")

        # Filtrado temporal opcional
        if start_date or end_date:
            da_pt = da_pt.sel(T=slice(start_date, end_date))

        # Convertir a pandas.Series y guardar CSV
        ser = da_pt.to_series()
        csv_path = f"{out_prefix}_{var}_{lat}_{lon}.csv"
        ser.to_csv(csv_path, header=[var])
        print(f"Guardado: {csv_path}")

if __name__ == "__main__":
    # Coordenadas 
    lat_pt = -7.158
    lon_pt = -78.53

    # rango de fechas
    start = "1981-01-01"
    end   = "2020-12-31"

    download_point(lat_pt, lon_pt,
                   out_prefix="pisco_ronquillo",
                   start_date=start,
                   end_date=end)
