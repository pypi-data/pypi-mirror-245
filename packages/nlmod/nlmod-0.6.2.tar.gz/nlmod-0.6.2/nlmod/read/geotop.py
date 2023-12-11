import datetime as dt
import logging
import os

import numpy as np
import pandas as pd
import xarray as xr

from .. import NLMOD_DATADIR, cache
from ..dims.resample import get_extent

logger = logging.getLogger(__name__)

GEOTOP_URL = r"http://www.dinodata.nl/opendap/GeoTOP/geotop.nc"


def get_lithok_props(rgb_colors=True):
    fname = os.path.join(NLMOD_DATADIR, "geotop", "litho_eenheden.csv")
    df = pd.read_csv(fname, index_col=0)
    if rgb_colors:
        df["color"] = pd.Series(get_lithok_colors())
    return df


def get_lithok_colors():
    colors = {
        0: (200, 200, 200),
        1: (157, 78, 64),
        2: (0, 146, 0),
        3: (194, 207, 92),
        5: (255, 255, 0),
        6: (243, 225, 6),
        7: (231, 195, 22),
        8: (216, 163, 32),
        9: (95, 95, 255),
    }
    colors = {key: tuple([x / 255 for x in colors[key]]) for key in colors}
    return colors


def get_strat_props():
    fname = os.path.join(NLMOD_DATADIR, "geotop", "geo_eenheden.csv")
    df = pd.read_csv(fname, index_col=0, keep_default_na=False)
    return df


def get_kh_kv_table(kind="Brabant"):
    if kind == "Brabant":
        fname = os.path.join(
            NLMOD_DATADIR,
            "geotop",
            "hydraulische_parameterisering_geotop_noord-brabant_en_noord-_en_midden-limburg.csv",
        )
        df = pd.read_csv(fname)
    else:
        raise (Exception(f"Unknown kind in get_kh_kv_table: {kind}"))
    return df


@cache.cache_netcdf
def geotop_to_layermodel(geotop_ds, strat_props=None):
    """Convert geotop dataset to layermodel dataset.

    Converts geotop data to dataset with layer elevations and hydraulic
    conductivities. Uses hydraulic conductivities provided by a

    Parameters
    ----------
    geotop_ds : xr.DataSet
        geotop dataset (download using `get_geotop(extent)`)
    strat_props : pd.DataFrame, optional
        The properties of the stratigraphic unit. Load with get_strat_props() when None.
        The default is None.

    Returns
    -------
    ds: xr.DataSet
        dataset with top, bot, kh and kv per geotop layer
    """

    if strat_props is None:
        strat_props = get_strat_props()

    ds = convert_geotop_to_ml_layers(geotop_ds, strat_props=strat_props)

    ds.attrs["extent"] = get_extent(ds)

    for datavar in ds:
        ds[datavar].attrs["source"] = "Geotop"
        ds[datavar].attrs["url"] = GEOTOP_URL
        ds[datavar].attrs["date"] = dt.datetime.now().strftime("%Y%m%d")
        if datavar in ["top", "bot"]:
            ds[datavar].attrs["units"] = "mNAP"
        elif datavar in ["kh", "kv"]:
            ds[datavar].attrs["units"] = "m/day"

    return ds


@cache.cache_netcdf
def get_geotop(extent, url=GEOTOP_URL, probabilities=False):
    """Get a slice of the geotop netcdf url within the extent, set the x and y
    coordinates to match the cell centers and keep only the strat and lithok
    data variables.

    Parameters
    ----------
    extent : list, tuple or np.array
        desired model extent (xmin, xmax, ymin, ymax)
    url : str, optional
        url of geotop netcdf file. The default is
        http://www.dinodata.nl/opendap/GeoTOP/geotop.nc
    probabilities : bool, optional
        if True, download probability data

    Returns
    -------
    gt : xarray Dataset
        slices geotop netcdf.
    """
    gt = xr.open_dataset(url, chunks="auto")

    # only download requisite data
    data_vars = ["strat", "lithok"]
    if probabilities:
        data_vars += [
            "kans_1",
            "kans_2",
            "kans_3",
            "kans_4",
            "kans_5",
            "kans_6",
            "kans_7",
            "kans_8",
            "kans_9",
            "onz_lk",
            "onz_ls",
        ]

    # set x and y dimensions to cell center
    for dim in ["x", "y"]:
        old_dim = gt[dim].values
        gt[dim] = old_dim + (old_dim[1] - old_dim[0]) / 2

    # get data vars and slice extent
    gt = gt[data_vars].sel(x=slice(extent[0], extent[1]), y=slice(extent[2], extent[3]))

    # change order of dimensions from x, y, z to z, y, x
    gt = gt.transpose("z", "y", "x")

    # flip z, and y coordinates
    gt = gt.isel(z=slice(None, None, -1), y=slice(None, None, -1))

    # add missing value
    # gt.strat.attrs["missing_value"] = -127

    return gt


def get_geotop_raw_within_extent(extent, url=GEOTOP_URL, drop_probabilities=True):
    DeprecationWarning(
        "This function is deprecated, use the equivalent `get_geotop()`!"
    )
    return get_geotop(extent=extent, url=url, drop_probabilities=drop_probabilities)


def convert_geotop_to_ml_layers(
    geotop_ds,
    strat_props=None,
    **kwargs,
):
    """Convert geotop voxel data to layers using the stratigraphy-data.

    It gets the top and botm of each stratigraphic unit in the geotop dataset.

    Parameters
    ----------
    geotop_ds_raw: xr.Dataset
        dataset with geotop voxel data
    strat_props: pandas.DataFrame
        The properties of the stratigraphic unit. Load with get_strat_props() when None.
        The default is None.

    Returns
    -------
    geotop_ds_mod: xarray.DataSet
        geotop dataset with top and botm per geo_eenheid

    Note
    ----
    strat-units >=6000 are 'stroombanen'. These are difficult to add because they can
    occur above and/or below any other unit. Therefore these units are not added to the
    dataset, and their thickness is added to the strat-unit below the stroombaan.
    """

    # stap 2 maak een laag per geo-eenheid
    if strat_props is None:
        strat_props = get_strat_props()

    # vindt alle geo-eenheden in model_extent
    geo_eenheden = np.unique(geotop_ds.strat.values)
    # geo_eenheden = geo_eenheden[~(geo_eenheden==geotop_ds.strat.missing_value)]
    geo_eenheden = geo_eenheden[np.isfinite(geo_eenheden)]
    stroombaan_eenheden = geo_eenheden[geo_eenheden >= 6000]
    geo_eenheden = geo_eenheden[geo_eenheden < 6000]

    # geo eenheid 2000 zit boven 1130
    if (2000.0 in geo_eenheden) and (1130.0 in geo_eenheden):
        geo_eenheden[(geo_eenheden == 2000.0) + (geo_eenheden == 1130.0)] = [
            2000.0,
            1130.0,
        ]

    strat_codes = []
    for geo_eenh in geo_eenheden:
        if int(geo_eenh) in strat_props.index:
            code = strat_props.at[int(geo_eenh), "code"]
        else:
            logger.warning(f"Unknown strat-value: {geo_eenh}")
            code = str(geo_eenh)
        strat_codes.append(code)

    # fill top and bot
    shape = (len(strat_codes), len(geotop_ds.y), len(geotop_ds.x))
    top = np.full(shape, np.nan)
    bot = np.full(shape, np.nan)
    lay = 0
    logger.info("creating top and bot per geo eenheid")
    for geo_eenheid in geo_eenheden:
        logger.debug(int(geo_eenheid))

        mask = geotop_ds.strat == geo_eenheid
        geo_z = xr.where(mask, geotop_ds.z, np.NaN)

        top[lay] = geo_z.max(dim="z") + 0.25
        bot[lay] = geo_z.min(dim="z") - 0.25

        lay += 1

    # add the thickness of stroombanen to the layer below the stroombaan
    for lay in range(top.shape[0]):
        if lay == 0:
            top[lay] = np.nanmax(top, 0)
        else:
            top[lay] = bot[lay - 1]
        bot[lay] = np.where(np.isnan(bot[lay]), top[lay], bot[lay])

    dims = ("layer", "y", "x")
    coords = {"layer": strat_codes, "y": geotop_ds.y, "x": geotop_ds.x}
    da_top = xr.DataArray(data=top, dims=dims, coords=coords)
    da_bot = xr.DataArray(data=bot, dims=dims, coords=coords)
    geotop_ds_mod = xr.Dataset()

    geotop_ds_mod["top"] = da_top
    geotop_ds_mod["botm"] = da_bot

    geotop_ds_mod.attrs["stroombanen"] = stroombaan_eenheden

    if "kh" in geotop_ds and "kv" in geotop_ds:
        aggregate_to_ds(geotop_ds, geotop_ds_mod, **kwargs)

    return geotop_ds_mod


def add_top_and_botm(ds):
    """Add the top and bottom of the voxels to the GeoTOP Dataset.

    This makes sure the structure of the geotop dataset is more like regis, and we can
    use the cross-section class (DatasetCrossSection from nlmod.

    Parameters
    ----------
    ds : xr.Dataset
        The geotop-dataset.

    Returns
    -------
    ds : xr.Dataset
        The geotop-dataset, with added variables "top" and "botm".
    """
    bottom = np.expand_dims(ds.z.values - 0.25, axis=(1, 2))
    bottom = np.repeat(np.repeat(bottom, len(ds.y), 1), len(ds.x), 2)
    bottom[np.isnan(ds.strat.values)] = np.NaN
    ds["botm"] = ("z", "y", "x"), bottom

    top = np.expand_dims(ds.z.values + 0.25, axis=(1, 2))
    top = np.repeat(np.repeat(top, len(ds.y), 1), len(ds.x), 2)
    top[np.isnan(ds.strat.values)] = np.NaN
    ds["top"] = ("z", "y", "x"), top
    return ds


def add_kh_and_kv(
    gt,
    df,
    stochastic=None,
    kh_method="arithmetic_mean",
    kv_method="harmonic_mean",
    anisotropy=1.0,
    kh="kh",
    kv="kv",
    kh_df="kh",
    kv_df="kv",
):
    """Add kh and kv variables to the voxels of the GeoTOP Dataset.

    Parameters
    ----------
    gt : xr.Dataset
        The geotop dataset, at least with variable lithok.
    df : pd.DataFrame
        A DataFrame with information about the kh and optionally kv, for different
        lithoclasses or stratigraphic units. The DataFrame must contain the columns
        'lithok' and 'kh', and optionally 'strat' and 'kv'. As an example see
        nlmod.read.geotop.get_kh_kv_table().
    stochastic : bool, str or None, optional
        When stochastic is True or a string, use the stochastic data of GeoTOP. The only
        supported method right now is "linear", which means kh and kv are determined
        from a linear weighted mean of the voxels. For kh the method from kh_method is
        used to calculate the mean. For kv the method from kv_method is used. When
        stochastic is False or None, the stochastic data of GeoTOP is not used. The
        default is None.
    kh_method : str, optional
        The method to calculate the weighted mean of kh values when stochastic is True
        or "linear". Allowed values are "arithmetic_mean" and "harmonic_mean". The
        default is "arithmetic_mean".
    kv_method : str, optional
        The method to calculate the weighted mean of kv values when stochastic is True
        or "linear". Allowed values are "arithmetic_mean" and "harmonic_mean". The
        default is "arithmetic_mean".
    anisotropy : float, optional
        THe anisotropy value used when there are no kv values in df. The default is 1.0.
    kh : str, optional
        THe name of the new variable with kh values in gt. The default is "kh".
    kv : str, optional
        THe name of the new variable with kv values in gt. The default is "kv".
    kh_df : str, optional
        The name of the column with kh values in df. The default is "kh".
    kv_df : str, optional
        THe name of the column with kv values in df. The default is "kv".

    Raises
    ------

        DESCRIPTION.

    Returns
    -------
    gt : xr.Dataset
        Datset with voxel-data, with the added variables 'kh' and 'kv'.
    """
    if isinstance(stochastic, bool):
        if stochastic:
            stochastic = "linear"
        else:
            stochastic = None
    if kh_method not in ["arithmetic_mean", "harmonic_mean"]:
        raise (Exception("Unknown kh_method: {kh_method}"))
    if kv_method not in ["arithmetic_mean", "harmonic_mean"]:
        raise (Exception("Unknown kv_method: {kv_method}"))
    strat = gt["strat"].values
    msg = "Determining kh and kv of geotop-data based on lithoclass"
    if df.index.name in ["lithok", "strat"]:
        df = df.reset_index()
    if "strat" in df:
        msg = f"{msg} and stratigraphy"
    logger.info(msg)
    if kh_df not in df:
        raise (Exception(f"No {kh_df} defined in df"))
    if kv_df not in df:
        logger.info(f"Setting kv equal to kh / {anisotropy}")
    if stochastic is None:
        # calculate kh and kv from most likely lithoclass
        lithok = gt["lithok"].values
        kh_ar = np.full(lithok.shape, np.NaN)
        kv_ar = np.full(lithok.shape, np.NaN)
        if "strat" in df:
            combs = np.column_stack((strat.ravel(), lithok.ravel()))
            # drop nans
            combs = combs[~np.isnan(combs).any(1)].astype(int)
            # get unique combinations of strat and lithok
            combs_un = np.unique(combs, axis=0)
            for istrat, ilithok in combs_un:
                mask = (strat == istrat) & (lithok == ilithok)
                kh_ar[mask], kv_ar[mask] = _get_kh_kv_from_df(
                    df, ilithok, istrat, anisotropy=anisotropy, mask=mask
                )
        else:
            for ilithok in np.unique(lithok[~np.isnan(lithok)]):
                mask = lithok == ilithok
                kh_ar[mask], kv_ar[mask] = _get_kh_kv_from_df(
                    df,
                    ilithok,
                    anisotropy=anisotropy,
                    mask=mask,
                )
    elif stochastic == "linear":
        strat_un = np.unique(strat[~np.isnan(strat)])
        kh_ar = np.full(strat.shape, 0.0)
        kv_ar = np.full(strat.shape, 0.0)
        probality_total = np.full(strat.shape, 0.0)
        for ilithok in df["lithok"].unique():
            if ilithok == 0:
                # there are no probabilities defined for lithoclass 'antropogeen'
                continue
            probality = gt[f"kans_{ilithok}"].values
            if "strat" in df:
                khi, kvi = _handle_nans_in_stochastic_approach(
                    np.NaN, np.NaN, kh_method, kv_method
                )
                khi = np.full(strat.shape, khi)
                kvi = np.full(strat.shape, kvi)
                for istrat in strat_un:
                    mask = (strat == istrat) & (probality > 0)
                    if not mask.any():
                        continue
                    kh_sel, kv_sel = _get_kh_kv_from_df(
                        df, ilithok, istrat, anisotropy=anisotropy, mask=mask
                    )
                    if np.isnan(kh_sel):
                        probality[mask] = 0.0
                    kh_sel, kv_sel = _handle_nans_in_stochastic_approach(
                        kh_sel, kv_sel, kh_method, kv_method
                    )
                    khi[mask], kvi[mask] = kh_sel, kv_sel
            else:
                khi, kvi = _get_kh_kv_from_df(df, ilithok, anisotropy=anisotropy)
                if np.isnan(khi):
                    probality[:] = 0.0
                khi, kvi = _handle_nans_in_stochastic_approach(
                    khi, kvi, kh_method, kv_method
                )
            if kh_method == "arithmetic_mean":
                kh_ar = kh_ar + probality * khi
            else:
                kh_ar = kh_ar + (probality / khi)
            if kv_method == "arithmetic_mean":
                kv_ar = kv_ar + probality * kvi
            else:
                kv_ar = kv_ar + (probality / kvi)
            probality_total += probality
        if kh_method == "arithmetic_mean":
            kh_ar = kh_ar / probality_total
        else:
            kh_ar = probality_total / kh_ar
        if kv_method == "arithmetic_mean":
            kv_ar = kv_ar / probality_total
        else:
            kv_ar = probality_total / kv_ar
    else:
        raise (Exception(f"Unsupported value for stochastic: {stochastic}"))

    dims = gt["strat"].dims
    gt[kh] = dims, kh_ar
    gt[kv] = dims, kv_ar
    return gt


def _get_kh_kv_from_df(df, ilithok, istrat=None, anisotropy=1.0, mask=None):
    mask_df = df["lithok"] == ilithok
    if istrat is not None:
        mask_df = mask_df & (df["strat"] == istrat)
    if not np.any(mask_df):
        msg = f"No conductivities found for stratigraphic unit {istrat}"
        if istrat is not None:
            msg = f"{msg} and lithoclass {ilithok}"
        if mask is None:
            msg = f"{msg}. Setting values of voxels to NaN."
        else:
            msg = f"{msg}. Setting values of {mask.sum()} voxels to NaN."
        logger.warning(msg)
        return np.NaN, np.NaN

    kh = df.loc[mask_df, "kh"].mean()
    if "kv" in df:
        kv = df.loc[mask_df, "kv"].mean()
        if np.isnan(kv):
            kv = kh / anisotropy
        if np.isnan(kh):
            kh = kv * anisotropy
    else:
        kv = kh / anisotropy

    return kh, kv


def _handle_nans_in_stochastic_approach(kh, kv, kh_method, kv_method):
    if np.isnan(kh):
        if kh_method == "arithmetic_mean":
            kh = 0.0
        else:
            kh = np.inf
    if np.isnan(kv):
        if kv_method == "arithmetic_mean":
            kv = 0.0
        else:
            kv = np.inf
    return kh, kv


def aggregate_to_ds(
    gt, ds, kh="kh", kv="kv", kd="kD", c="c", kh_gt="kh", kv_gt="kv", add_kd_and_c=False
):
    """Aggregate voxels from GeoTOP to layers in a model DataSet with top and
    botm, to calculate kh and kv.

    Parameters
    ----------
    gt : xr.Dataset
        A Dataset containing the Geotop voxel data.
    ds : xr.Dataset
        A Dataset containing the top and botm of the layers.
    kh : str, optional
        The name of the new variable for the horizontal conductivity in ds. The default
        is "kh".
    kv : str, optional
        The name of the new variable for the vertical conductivity in ds. The default is
        "kv".
    kd : str, optional
        The name of the variable for the horizontal transmissivity. Only used when
        add_kd_and_c is True. The default is "kD".
    c : str, optional
        The name of the variable for the vertical reistance. Only used when add_kd_and_c
        is True The default is "c".
    kh_gt : str, optional
        The name of the variable for the horizontal conductivity in gt. The default is
        "kh".
    kv_gt : str, optional
        The name of the variable for the vertical conductivity in gt. The default is
        "kv".
    add_kd_and_c : bool, optional
        Add the variables kd and c to ds. The default is False.

    Returns
    -------
    ds : xr.Dataset
        The Dataset ds, with added variables kh and kv (and optionally kd and c).
    """
    assert (ds.x == gt.x).all() and (ds.y == gt.y).all()
    msg = "Please add {} to geotop-Dataset first, using add_kh_and_kv()"
    if kh_gt not in gt:
        raise (Exception(msg.format(kh_gt)))
    if kv_gt not in gt:
        raise (Exception(msg.format(kv_gt)))
    kD_ar = []
    c_ar = []
    kh_ar = []
    kv_ar = []
    if "layer" in ds["top"].dims:
        # make sure there is no layer dimension in top
        ds["top"] = ds["top"].max("layer")
    for ilay in range(len(ds.layer)):
        if ilay == 0:
            top = ds["top"]
        else:
            top = ds["botm"][ilay - 1].drop_vars("layer")
        bot = ds["botm"][ilay].drop_vars("layer")

        gt_top = (gt["z"] + 0.25).broadcast_like(gt[kh_gt])
        gt_bot = (gt["z"] - 0.25).broadcast_like(gt[kh_gt])
        gt_top = gt_top.where(gt_top < top, top)
        gt_top = gt_top.where(gt_top > bot, bot)
        gt_bot = gt_bot.where(gt_bot < top, top)
        gt_bot = gt_bot.where(gt_bot > bot, bot)
        gt_thk = gt_top - gt_bot
        # kD is the sum of thickness multiplied by conductivity
        kD_ar.append((gt_thk * gt[kh_gt]).sum("z"))
        # c is the sum of thickness devided by conductivity
        c_ar.append((gt_thk / gt[kv_gt]).sum("z"))
        # caluclate kh and hv
        d_gt = gt_top - gt_bot
        # use only the thickness with valid kh-values
        D = d_gt.where(~np.isnan(gt[kh_gt])).sum("z")
        kh_ar.append(kD_ar[-1] / D)
        # use only the thickness with valid kv-values
        D = d_gt.where(~np.isnan(gt[kv_gt])).sum("z")
        kv_ar.append(D / c_ar[-1])
    if add_kd_and_c:
        ds[kd] = xr.concat(kD_ar, ds.layer)
        ds[c] = xr.concat(c_ar, ds.layer)
    ds[kh] = xr.concat(kh_ar, ds.layer)
    ds[kv] = xr.concat(kv_ar, ds.layer)
    return ds
