#!/usr/bin/env python3
"""
download_piscop_separate_temps.py

Descarga diaria de:
  - Precipitación (PISCOp V2.1)
  - Temperatura mínima (PISCOp v1p1)
  - Temperatura máxima (PISCOp v1p1)

y guarda cada variable en un NetCDF local.
"""

import xarray as xr

def main():
    # URLs DODS para cada variable
    precip_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Prec/.v2p1/"
        ".stable/.daily/dods"
    )  # Precipitación PISCOp V2.1 :contentReference[oaicite:0]{index=0}

    tmin_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/"
        ".tmin/.stable/.daily/dods"
    )  # Temperatura mínima PISCOp v1p1 :contentReference[oaicite:1]{index=1}

    tmax_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/"
        ".tmax/.stable/.daily/dods"
    )  # Temperatura máxima PISCOp v1p1 :contentReference[oaicite:2]{index=2}

    # 1) Abrir los datasets remotos
    ds_prec = xr.open_dataset(precip_url)
    ds_tmin = xr.open_dataset(tmin_url)
    ds_tmax = xr.open_dataset(tmax_url)

    # 2) Extraer las variables
    precip = ds_prec["Prec"]   # mm/día
    tmin   = ds_tmin["tmin"]   # °C
    tmax   = ds_tmax["tmax"]   # °C

    # 3) (Opcional) Recorte espacial/temporal
    precip = precip.sel(X=slice(-81.5, -67.0), Y=slice(-18.75, 1.35))
    precip = precip.sel(T=slice("1999-01-01", "2000-12-31"))

    # 4) Guardar cada variable a su propio NetCDF
    precip.to_netcdf("piscop_precip_daily_1999-2000.nc")
    tmin.to_netcdf("piscop_tmin_daily_1999-2000.nc")
    tmax.to_netcdf("piscop_tmax_daily_1999-2000.nc")

    print("Descargas completadas:")
    print(" - piscop_precip_daily_1999-2000.nc (precipitación)")
    print(" - piscop_tmin_daily_1999-2000.nc (temperatura mínima)")
    print(" - piscop_tmax_daily_1999-2000.nc (temperatura máxima)")

if __name__ == "__main__":
    main()
