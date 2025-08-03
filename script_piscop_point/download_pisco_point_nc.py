#!/usr/bin/env python3
"""
download_pisco_point_nc.py

Descarga series diarias de:
  - Precipitación
  - Temperatura mínima
  - Temperatura máxima

para un punto geográfico dado (lat, lon) desde PISCOp,
y guarda cada serie en un archivo NetCDF.
"""

import xarray as xr

def download_point_nc(lat, lon, out_prefix="pisco_point_nc", start_date=None, end_date=None):
    # Definición de variables, URLs y nombres en el dataset
    var_dict = {
        "precip": ("Prec",
            "http://iridl.ldeo.columbia.edu/"
            "SOURCES/.SENAMHI/.HSR/.PISCO/.Prec/.v2p1/.stable/.daily/dods"),
        "tmin": ("tmin",
            "http://iridl.ldeo.columbia.edu/"
            "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmin/.stable/.daily/dods"),
        "tmax": ("tmax",
            "http://iridl.ldeo.columbia.edu/"
            "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmax/.stable/.daily/dods"),
    }

    for var_key, (var_name, url) in var_dict.items():
        # 1) Abrir el dataset remoto
        ds = xr.open_dataset(url)

        # 2) Extraer y seleccionar el punto (nearest neighbor)
        da = ds[var_name].sel(X=lon, Y=lat, method="nearest")

        # 3) Filtrar por fechas si se indicaron
        if start_date or end_date:
            da = da.sel(T=slice(start_date, end_date))

        # 4) Convertir DataArray a Dataset para netCDF
        ds_out = da.to_dataset(name=var_name)

        # 5) Guardar en NetCDF
        filename = f"{out_prefix}_{var_key}_{lat}_{lon}.nc"
        ds_out.to_netcdf(filename)
        print(f"Guardado: {filename}")

if __name__ == "__main__":
    # coordenadas
    lat_pt = -7.158
    lon_pt = -78.53

    # Rango  de fechas (o None para todo el período disponible)
    start = "1981-01-01"
    end   = "2020-12-31"

    download_point_nc(lat_pt, lon_pt,
                      out_prefix="pisco_ronquillo",
                      start_date=start,
                      end_date=end)
