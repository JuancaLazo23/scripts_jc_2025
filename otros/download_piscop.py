#!/usr/bin/env python3
"""
download_piscop.py

Descarga diaria de:
 - Precipitación (PISCOp V2.1)
 - Temperatura mínima y máxima (PISCOp v1p1)

y guarda NetCDF locales.
"""

import xarray as xr

def main():
    # Endpoints OPeNDAP
    precip_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Prec/.v2p1/.stable/.daily/.Prec/dods"
    )  # DODS endpoint de precipitación :contentReference[oaicite:0]{index=0}

    tmin_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmin/.stable/.daily/.tmin/dods"
    )
    tmax_url = (
        "http://iridl.ldeo.columbia.edu/"
        "SOURCES/.SENAMHI/.HSR/.PISCO/.Temp/.v1p1/.tmax/.stable/.daily/.tmax/dods"
    )
    # Según catálogo: PISCOp incluye variables Prec y Temp (tmin, tmax) :contentReference[oaicite:1]{index=1}

    # 1) Abre los datasets remotos
    ds_prec = xr.open_dataset(precip_url)
    ds_tmin = xr.open_dataset(tmin_url)
    ds_tmax = xr.open_dataset(tmax_url)

    # 2) Selecciona las variables
    precip = ds_prec["Prec"]        # mm/día
    tmin   = ds_tmin["tmin"]        # °C
    tmax   = ds_tmax["tmax"]        # °C

    # 3) (Opcional) Submuestreo espacial y temporal
    precip = precip.sel(X=slice(-81.5, -67.0), Y=slice(-18.75, 1.35))
    precip = precip.sel(T=slice("1999-01-01", "2001-12-31"))

    # 4) Calcula temperatura media diaria
    temp_mean = (tmin + tmax) / 2
    temp_mean.name = "temp_mean"

    # 5) Guarda a NetCDF local
    precip.to_netcdf("piscop_precip_daily_1981-2016.nc")
    temp_mean.to_netcdf("piscop_temp_mean_daily_1981-2016.nc")

    print("Descargas completadas:")
    print(" - pescop_precip_daily_1981-2016.nc (precipitación)")
    print(" - piscop_temp_mean_daily_1981-2016.nc (temperatura media)")

if __name__ == "__main__":
    main()
