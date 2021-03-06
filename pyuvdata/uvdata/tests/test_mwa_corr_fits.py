# -*- mode: python; coding: utf-8 -*-
# Copyright (c) 2019 Radio Astronomy Software Group
# Licensed under the 2-clause BSD License

"""Tests for MWACorrFITS object."""

import pytest
import os
import numpy as np

from pyuvdata import UVData
from pyuvdata.data import DATA_PATH
import pyuvdata.tests as uvtest
from astropy.io import fits

# set up MWA correlator file list
testdir = os.path.join(DATA_PATH, "mwa_corr_fits_testfiles/")

testfiles = [
    "1131733552.metafits",
    "1131733552_20151116182537_mini_gpubox01_00.fits",
    "1131733552_20151116182637_mini_gpubox06_01.fits",
    "1131733552_mini_01.mwaf",
    "1131733552_mini_06.mwaf",
    "1131733552_mod.metafits",
    "1131733552_mini_cotter.uvfits",
    "1131733552_metafits_ppds.fits",
]
filelist = [testdir + i for i in testfiles]


@pytest.fixture(scope="module")
def flag_file_init(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("pyuvdata_corr_fits", numbered=True)
    spoof_file1 = str(tmp_path / "spoof_01_00.fits")
    spoof_file6 = str(tmp_path / "spoof_06_00.fits")
    # spoof box files of the appropriate size
    with fits.open(filelist[1]) as mini1:
        mini1[1].data = np.repeat(mini1[1].data, 8, axis=0)
        extra_dat = np.copy(mini1[1].data)
        for app_ind in range(2):
            mini1.append(fits.ImageHDU(extra_dat))
        mini1[2].header["MILLITIM"] = 500
        mini1[2].header["TIME"] = mini1[1].header["TIME"]
        mini1[3].header["MILLITIM"] = 0
        mini1[3].header["TIME"] = mini1[1].header["TIME"] + 1
        mini1.writeto(spoof_file1)

    with fits.open(filelist[2]) as mini6:
        mini6[1].data = np.repeat(mini6[1].data, 8, axis=0)
        extra_dat = np.copy(mini6[1].data)
        for app_ind in range(2):
            mini6.append(fits.ImageHDU(extra_dat))
        mini6[2].header["MILLITIM"] = 500
        mini6[2].header["TIME"] = mini6[1].header["TIME"]
        mini6[3].header["MILLITIM"] = 0
        mini6[3].header["TIME"] = mini6[1].header["TIME"] + 1
        mini6.writeto(spoof_file6)

    flag_testfiles = [spoof_file1, spoof_file6, filelist[0]]

    yield flag_testfiles


def test_read_mwa_write_uvfits(tmp_path):
    """
    MWA correlator fits to uvfits loopback test.

    Read in MWA correlator files, write out as uvfits, read back in and check
    for object equality.
    """
    mwa_uv = UVData()
    uvfits_uv = UVData()
    messages = [
        "telescope_location is not set",
        "some coarse channel files were not submitted",
    ]
    category = [UserWarning] * 2
    uvtest.checkWarnings(
        mwa_uv.read_mwa_corr_fits,
        func_args=[filelist[0:2]],
        func_kwargs={"correct_cable_len": True, "phase_to_pointing_center": True},
        nwarnings=len(messages),
        message=messages,
        category=category,
    )
    testfile = str(tmp_path / "outtest_MWAcorr.uvfits")
    mwa_uv.write_uvfits(testfile, spoof_nonessential=True)
    uvfits_uv.read_uvfits(testfile)
    assert mwa_uv == uvfits_uv

    messages = [
        "telescope_location is not set",
        "some coarse channel files were not submitted",
    ]
    category = [UserWarning] * 2
    uvtest.checkWarnings(
        mwa_uv.read_mwa_corr_fits,
        func_args=[filelist[0:2]],
        func_kwargs={"correct_cable_len": True, "phase_to_pointing_center": True},
        nwarnings=len(messages),
        message=messages,
        category=category,
    )
    testfile = str(tmp_path / "outtest_MWAcorr.uvfits")
    mwa_uv.write_uvfits(testfile, spoof_nonessential=True)
    uvfits_uv.read_uvfits(testfile)
    assert mwa_uv == uvfits_uv


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_select_on_read():
    mwa_uv = UVData()
    mwa_uv2 = UVData()
    mwa_uv.read_mwa_corr_fits(filelist[0:2], correct_cable_len=True)
    unique_times = np.unique(mwa_uv.time_array)
    select_times = unique_times[
        np.where(
            (unique_times >= np.min(mwa_uv.time_array))
            & (unique_times <= np.mean(mwa_uv.time_array))
        )
    ]
    mwa_uv.select(times=select_times)
    uvtest.checkWarnings(
        mwa_uv2.read,
        func_args=[filelist[0:2]],
        func_kwargs={
            "correct_cable_len": True,
            "time_range": [np.min(mwa_uv.time_array), np.mean(mwa_uv.time_array)],
        },
        message=[
            'Warning: select on read keyword set, but file_type is "mwa_corr_fits"',
            "telescope_location is not set. Using known values for MWA.",
            "some coarse channel files were not submitted",
        ],
        nwarnings=3,
    )
    assert mwa_uv == mwa_uv2


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_read_mwa_read_cotter():
    """
    Pyuvdata and cotter equality test.

    Read in MWA correlator files and the corresponding cotter file and check
    for data array equality.
    """
    mwa_uv = UVData()
    cotter_uv = UVData()
    # cotter data has cable correction and is unphased
    mwa_uv.read(filelist[0:2], correct_cable_len=True)
    cotter_uv.read(filelist[6])
    # cotter doesn't record the auto xy polarizations
    # due to a possible bug in cotter, the auto yx polarizations are conjugated
    # fix these before testing data_array
    autos = np.isclose(mwa_uv.ant_1_array - mwa_uv.ant_2_array, 0.0)
    cotter_uv.data_array[autos, :, :, 2] = cotter_uv.data_array[autos, :, :, 3]
    cotter_uv.data_array[autos, :, :, 3] = np.conj(cotter_uv.data_array[autos, :, :, 3])
    assert np.allclose(
        mwa_uv.data_array[:, :, :, :],
        cotter_uv.data_array[:, :, :, :],
        atol=1e-4,
        rtol=0,
    )


def test_read_mwa_write_uvfits_meta_mod(tmp_path):
    """
    MWA correlator fits to uvfits loopback test with a modified metafits file.

    Read in MWA correlator files, write out as uvfits, read back in and check
    for object equality.
    """
    # The metafits file has been modified to contain some coarse channels < 129,
    # and to have an uncorrected cable length.
    mwa_uv = UVData()
    uvfits_uv = UVData()
    messages = [
        "telescope_location is not set",
        "some coarse channel files were not submitted",
    ]
    files = [filelist[1], filelist[5]]
    uvtest.checkWarnings(
        mwa_uv.read,
        func_args=[files],
        func_kwargs={"correct_cable_len": True, "phase_to_pointing_center": True},
        nwarnings=2,
        message=messages,
    )
    testfile = str(tmp_path / "outtest_MWAcorr.uvfits")
    mwa_uv.write_uvfits(testfile, spoof_nonessential=True)
    uvfits_uv.read_uvfits(testfile)
    assert mwa_uv == uvfits_uv


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
@pytest.mark.filterwarnings("ignore:Combined frequencies are not contiguous")
def test_read_mwa_multi():
    """Test reading in two sets of files."""
    set1 = filelist[0:2]
    set2 = [filelist[0], filelist[2]]
    mwa_uv = UVData()

    mwa_uv.read([set1, set2])

    mwa_uv2 = UVData()
    messages = [
        "telescope_location is not set",
        "some coarse channel files were not submitted",
        "telescope_location is not set",
        "some coarse channel files were not submitted",
        "Combined frequencies are not contiguous",
    ]
    category = [UserWarning] * 5
    uvtest.checkWarnings(
        mwa_uv2.read,
        func_args=[[set1, set2]],
        func_kwargs={"file_type": "mwa_corr_fits"},
        nwarnings=5,
        message=messages,
        category=category,
    )

    assert mwa_uv == mwa_uv2


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_read_mwa_multi_concat(tmp_path):
    """Test reading in two sets of files with fast concatenation."""
    # modify file so that time arrays are matching
    mod_mini_6 = str(tmp_path / "mini_gpubox06_01.fits")
    with fits.open(filelist[2]) as mini6:
        mini6[1].header["time"] = 1447698337
        mini6.writeto(mod_mini_6)
    set1 = filelist[0:2]
    set2 = [filelist[0], mod_mini_6]
    mwa_uv = UVData()
    mwa_uv.read([set1, set2], axis="freq")

    mwa_uv2 = UVData()
    messages = [
        "telescope_location is not set",
        "some coarse channel files were not submitted",
        "telescope_location is not set",
        "some coarse channel files were not submitted",
    ]
    category = [UserWarning] * 4
    uvtest.checkWarnings(
        mwa_uv2.read,
        func_args=[[set1, set2]],
        func_kwargs={"axis": "freq", "file_type": "mwa_corr_fits"},
        nwarnings=4,
        message=messages,
        category=category,
    )
    assert mwa_uv == mwa_uv2
    os.remove(mod_mini_6)


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_read_mwa_flags():
    """Test handling of flag files."""
    mwa_uv = UVData()
    subfiles = [filelist[0], filelist[1], filelist[3], filelist[4]]
    messages = [
        "mwaf files submitted with use_cotter_flags=False",
        "telescope_location is not set",
        "some coarse channel files were not submitted",
    ]
    uvtest.checkWarnings(
        mwa_uv.read, func_args=[subfiles], nwarnings=3, message=messages
    )
    del mwa_uv
    mwa_uv = UVData()
    with pytest.raises(NotImplementedError) as cm:
        mwa_uv.read(subfiles, use_cotter_flags=True)
    assert str(cm.value).startswith("reading in cotter flag files")
    del mwa_uv
    mwa_uv = UVData()
    with pytest.raises(ValueError) as cm:
        mwa_uv.read(subfiles[0:2], use_cotter_flags=True)
    assert str(cm.value).startswith("no flag files submitted")
    del mwa_uv


def test_multiple_coarse():
    """
    Test two coarse channel files.

    Read in MWA correlator files with two different orderings of the files
    and check for object equality.
    """
    order1 = [filelist[0:3]]
    order2 = [filelist[0], filelist[2], filelist[1]]
    mwa_uv1 = UVData()
    mwa_uv2 = UVData()
    messages = [
        "telescope_location is not set",
        "coarse channels are not contiguous for this observation",
        "some coarse channel files were not submitted",
    ]
    uvtest.checkWarnings(
        mwa_uv1.read, func_args=[order1], nwarnings=3, message=messages
    )
    uvtest.checkWarnings(
        mwa_uv2.read, func_args=[order2], nwarnings=3, message=messages
    )
    assert mwa_uv1 == mwa_uv2


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_ppds(tmp_path):
    """Test handling of ppds files"""
    # turnaround test with just ppds file given
    mwa_uv = UVData()
    mwa_uv.read_mwa_corr_fits([filelist[1], filelist[7]], phase_to_pointing_center=True)
    testfile = str(tmp_path / "outtest_MWAcorr.uvfits")
    mwa_uv.write_uvfits(testfile, spoof_nonessential=True)
    uvfits_uv = UVData()
    uvfits_uv.read_uvfits(testfile)
    assert mwa_uv == uvfits_uv

    del mwa_uv
    del uvfits_uv

    # check that extra keywords are added when both ppds file and metafits file given
    mwa_uv = UVData()
    mwa_uv.read_mwa_corr_fits([filelist[0], filelist[1], filelist[7]])
    assert "MWAVER" in mwa_uv.extra_keywords and "MWADATE" in mwa_uv.extra_keywords


def test_fine_channels(tmp_path):
    """
    Break read_mwa_corr_fits by submitting files with different fine channels.

    Test that error is raised if files with different numbers of fine channels
    are submitted.
    """
    mwa_uv = UVData()
    bad_fine = str(tmp_path / "bad_gpubox06_01.fits")
    with fits.open(filelist[2]) as mini6:
        mini6[1].data = np.concatenate((mini6[1].data, mini6[1].data))
        mini6.writeto(bad_fine)
    with pytest.raises(ValueError) as cm:
        mwa_uv.read([bad_fine, filelist[1]])
    assert str(cm.value).startswith("files submitted have different fine")
    del mwa_uv


@pytest.mark.parametrize(
    "files,err_msg",
    [
        ([filelist[0]], "no data files submitted"),
        ([filelist[1]], "no metafits file submitted"),
        (
            [filelist[0], filelist[1], filelist[5]],
            "multiple metafits files in filelist",
        ),
    ],
)
def test_break_read_mwacorrfits(files, err_msg):
    """Break read_mwa_corr_fits by submitting files incorrectly."""
    mwa_uv = UVData()
    with pytest.raises(ValueError) as cm:
        mwa_uv.read(files)
    assert str(cm.value).startswith(err_msg)
    del mwa_uv


def test_file_extension(tmp_path):
    """
    Break read_mwa_corr_fits by submitting file with the wrong extension.

    Test that error is raised if a file with an extension that is not fits,
    metafits, or mwaf is submitted.
    """
    mwa_uv = UVData()
    bad_ext = str(tmp_path / "1131733552.meta")
    with fits.open(filelist[0]) as meta:
        meta.writeto(bad_ext)
    with pytest.raises(ValueError) as cm:
        mwa_uv.read(bad_ext, file_type="mwa_corr_fits")
    assert str(cm.value).startswith("only fits, metafits, and mwaf files supported")
    del mwa_uv


def test_diff_obs(tmp_path):
    """
    Break read_mwa_corr_fits by submitting files from different observations.

    Test that error is raised if files from different observations are
    submitted in the same file list.
    """
    mwa_uv = UVData()
    bad_obs = str(tmp_path / "bad2_gpubox06_01.fits")
    with fits.open(filelist[2]) as mini6:
        mini6[0].header["OBSID"] = "1131733555"
        mini6.writeto(bad_obs)
    with pytest.raises(ValueError) as cm:
        mwa_uv.read([bad_obs, filelist[0], filelist[1]])
    assert str(cm.value).startswith("files from different observations")
    del mwa_uv


def test_misaligned_times(tmp_path):
    """
    Break read_mwa_corr_fits by submitting files with misaligned times.

    Test that error is raised if file start times are different by an amount
    that is not an integer multiiple of the integration time.
    """
    mwa_uv = UVData()
    bad_obs = str(tmp_path / "bad3_gpubox06_01.fits")
    with fits.open(filelist[2]) as mini6:
        mini6[1].header["MILLITIM"] = 250
        mini6.writeto(bad_obs)
    with pytest.raises(ValueError) as cm:
        mwa_uv.read([bad_obs, filelist[0], filelist[1]])
    assert str(cm.value).startswith("coarse channel start times are misaligned")
    del mwa_uv


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings(
    "ignore:coarse channels are not contiguous for this observation"
)
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_flag_nsample_basic():
    """
    Test that the flag(without flag_int) and nsample arrays correctly reflect data.
    """
    uv = UVData()
    uv.read_mwa_corr_fits(filelist[0:3], flag_init=False)
    # check that only bad antennas are flagged for all times, freqs, pols
    bad_ants = [59, 114]
    good_ants = list(range(128))
    for j in bad_ants:
        good_ants.remove(j)
    bad = uv.select(antenna_nums=bad_ants, inplace=False)
    good = uv.select(antenna_nums=good_ants, inplace=False)
    assert np.all(bad.flag_array)
    good.flag_array = good.flag_array.reshape(
        (good.Ntimes, good.Nbls, good.Nspws, good.Nfreqs, good.Npols)
    )
    # good ants should be flagged except for the first time and second freq,
    # and for the second time and first freq
    assert np.all(good.flag_array[1:-1, :, :, :, :])
    assert np.all(good.flag_array[0, :, :, 1, :] == 0)
    assert np.all(good.flag_array[-1, :, :, 0, :] == 0)
    assert np.all(good.flag_array[0, :, :, 0, :])
    assert np.all(good.flag_array[-1, :, :, 1, :])
    # check that nsample array is filled properly
    uv.nsample_array = uv.nsample_array.reshape(
        (uv.Ntimes, uv.Nbls, uv.Nspws, uv.Nfreqs, uv.Npols)
    )
    assert np.all(uv.nsample_array[1:-1, :, :, :, :] == 0.0)
    assert np.all(uv.nsample_array[0, :, :, 1, :] == 1.0)
    assert np.all(uv.nsample_array[-1, :, :, 0, :] == 1.0)
    assert np.all(uv.nsample_array[0, :, :, 0, :] == 0.0)
    assert np.all(uv.nsample_array[-1, :, :, 1, :] == 0.0)


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings(
    "ignore:coarse channels are not contiguous for this observation"
)
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_flag_init(flag_file_init):
    """
    Test that routine MWA flagging works as intended.
    """
    uv = UVData()
    uv.read(flag_file_init, flag_init=True, start_flag=0, end_flag=0)

    freq_inds = [0, 1, 4, 6, 7, 8, 9, 12, 14, 15]
    freq_inds_complement = [ind for ind in range(16) if ind not in freq_inds]

    assert np.all(
        uv.flag_array[:, :, freq_inds, :]
    ), "Not all of edge and center channels are flagged!"
    assert not np.any(
        np.all(uv.flag_array[:, :, freq_inds_complement, :], axis=(0, 1, -1))
    ), "Some non-edge/center channels are entirely flagged!"


@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings(
    "ignore:coarse channels are not contiguous for this observation"
)
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_flag_start_flag(flag_file_init):
    uv = UVData()
    uv.read(
        flag_file_init,
        flag_init=True,
        start_flag=1.0,
        end_flag=1.0,
        edge_width=0,
        flag_dc_offset=False,
    )

    reshape = [uv.Ntimes, uv.Nbls, uv.Nspws, uv.Nfreqs, uv.Npols]
    time_inds = [0, 1, -1, -2]
    assert np.all(
        uv.flag_array.reshape(reshape)[time_inds, :, :, :, :]
    ), "Not all of start and end times are flagged."
    # Check that it didn't just flag everything
    # Should have unflagged data for time inds [2, -3]
    assert not np.any(
        np.all(uv.flag_array.reshape(reshape)[[2, -3], :, :, :, :], axis=(1, 2, 3, 4))
    ), "All the data is flagged for some intermediate times!"


@pytest.mark.parametrize(
    "err_type,read_kwargs,err_msg",
    [
        (
            ValueError,
            {"flag_init": True, "start_flag": 0, "end_flag": 0, "edge_width": 90e3},
            "The edge_width must be an integer multiple of the channel_width",
        ),
        (
            ValueError,
            {"flag_init": True, "start_flag": 1.2, "end_flag": 0},
            "The start_flag must be an integer multiple of the integration_time",
        ),
        (
            ValueError,
            {"flag_init": True, "start_flag": 0, "end_flag": 1.2},
            "The end_flag must be an integer multiple of the integration_time",
        ),
    ],
)
@pytest.mark.filterwarnings("ignore:telescope_location is not set. ")
@pytest.mark.filterwarnings(
    "ignore:coarse channels are not contiguous for this observation"
)
@pytest.mark.filterwarnings("ignore:some coarse channel files were not submitted")
def test_flag_init_errors(flag_file_init, err_type, read_kwargs, err_msg):
    uv = UVData()
    # give noninteger multiple inputs
    with pytest.raises(err_type) as cm:
        uv.read(flag_file_init, **read_kwargs)
    assert str(cm.value).startswith(err_msg)
