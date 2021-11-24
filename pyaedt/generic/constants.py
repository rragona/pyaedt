import math

RAD2DEG = 180.0 / math.pi
DEG2RAD = math.pi / 180
HOUR2SEC = 3600.0
MIN2SEC = 60.0
SEC2MIN = 1 / 60.0
SEC2HOUR = 1 / 3600.0
INV2PI = 0.5 / math.pi
V2PI = 2.0 * math.pi
METER2IN = 0.0254
METER2MILES = 1609.344051499


def db20(x, inverse=True):
    """Convert db20 to decimal and viceversa."""
    if inverse:
        return 20 * math.log10(x)
    else:
        return math.pow(10, x / 20.0)


def db10(x, inverse=True):
    """Convert db10 to decimal and viceversa."""
    if inverse:
        return 10 * math.log10(x)
    else:
        return math.pow(10, x / 10.0)


def fah2kel(val, inverse=True):
    """Convert a temperature from Fahrenheit to Kelvin.

    Parameters
    ----------
    val : float
        Temperature value in Fahrenheit.
    inverse : bool, optional
        The default is ``True``.

    Returns
    -------
    float
        Temperature value converted to Kelvin.

    """
    if inverse:
        return (val - 273.15) * 9 / 5 + 32
    else:
        return (val - 32) * 5 / 9 + 273.15


def cel2kel(val, inverse=True):
    """Convert a temperature from Celsius to Kelvin.

    Parameters
    ----------
    val : float
        Temperature value in Celsius.
    inverse : bool, optional
        The default is ``True``.

    Returns
    -------
    float
        Temperature value converted to Kelvin.

    """

    if inverse:
        return val - 273.15
    else:
        return val + 273.15


def unit_system(units):
    """Retrieve the name of the unit system associated with a unit string.

    Parameters
    ----------
    units : str
        Units for retrieving the associated unit system name.

    Returns
    -------
    str
        Key from the ``AEDT_units`` when successful. For example, ``"AngularSpeed"``.
    ``False`` when the units specified are not defined in AEDT units.

    """

    for unit_type, unit_dict in AEDT_UNITS.items():
        if units in unit_dict:
            return unit_type

    return False


def _resolve_unit_system(unit_system_1, unit_system_2, operation):
    """Retrieve the unit string of an arithmetic operation on ``Variable`` objects. If no resulting unit system
    is defined for a specific operation (in unit_system_operations), an empty string is returned

    Parameters
    ----------
    unit_system_1 : str
        Name of a unit system, which is a key of ``AEDT_units``.
    unit_system_2 : str
        Name of another unit system, which is a key of ``AEDT_units``.
    operation : str
        Name of an operator within the data set of ``["multiply" ,"divide"]``.

    Returns
    -------
    str
        Unit system when successful, ``""`` when failed.

    """
    try:
        key = "{}_{}_{}".format(unit_system_1, operation, unit_system_2)
        result_unit_system = UNIT_SYSTEM_OPERATIONS[key]
        return SI_UNITS[result_unit_system]
    except KeyError:
        return ""


AEDT_UNITS = {
    "AngularSpeed": {
        "deg_per_hr": HOUR2SEC * DEG2RAD,
        "rad_per_hr": HOUR2SEC,
        "deg_per_min": MIN2SEC * DEG2RAD,
        "rad_per_min": MIN2SEC,
        "deg_per_sec": DEG2RAD,
        "rad_per_sec": 1.0,
        "rev_per_sec": V2PI,
        "per_sec": V2PI,
        "rpm": SEC2MIN * V2PI,
    },
    "Angle": {"deg": DEG2RAD, "rad": 1.0, "degmin": DEG2RAD * SEC2MIN, "degsec": DEG2RAD * SEC2HOUR},
    "Current": {
        "fA": 1e-15,
        "pA": 1e-12,
        "nA": 1e-9,
        "uA": 1e-6,
        "mA": 1e-3,
        "A": 1.0,
        "kA": 1e3,
        "MegA": 1e6,
        "gA": 1e9,
        "dBA": (db20,),
    },
    "Flux": {"Wb": 1.0, "mx": 1e-8, "vh": 3600, "vs": 1.0},
    "Force": {
        "fNewton": 1e-15,
        "pNewton": 1e-12,
        "nNewton": 1e-9,
        "uNewton": 1e-6,
        "mNewton": 1e-3,
        "newton": 1.0,
        "kNewton": 1e3,
        "megNewton": 1e6,
        "gNewton": 1e9,
        "dyne": 1e-5,
        "kp": 9.80665,
        "PoundsForce": 4.44822,
    },
    "Freq": {"Hz": 1.0, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9, "THz": 1e12, "rps": 1.0, "per_sec": 1.0},
    "Inductance": {"fH": 1e-15, "pH": 1e-12, "nH": 1e-9, "uH": 1e-6, "mH": 1e-3, "H": 1.0},
    "Length": {
        "fm": 1e-15,
        "pm": 1e-12,
        "nm": 1e-9,
        "um": 1e-6,
        "mm": 1e-3,
        "cm": 1e-2,
        "dm": 1e-1,
        "meter": 1.0,
        "km": 1e3,
        "uin": METER2IN * 1e-6,
        "mil": METER2IN * 1e-3,
        "in": METER2IN,
        "ft": METER2IN * 12,
        "yd": METER2IN * 144,
    },
    "Mass": {"ug": 1e-9, "mg": 1e-6, "g": 1e-3, "kg": 1.0, "ton": 1000, "oz": 0.0283495, "lb": 0.453592},
    "None": {
        "f": 1e-15,
        "p": 1e-12,
        "n": 1e-9,
        "u": 1e-6,
        "m": 1e-3,
        "": 1.0,
        "k": 1e3,
        "meg": 1e6,
        "g": 1e9,
        "t": 1e12,
    },
    "Resistance": {"uOhm": 1e-6, "mOhm": 1e-3, "ohm": 1.0, "kOhm": 1e3, "megohm": 1e6, "GOhm": 1e9},
    "Speed": {
        "mm_per_sec": 1e-3,
        "cm_per_sec": 1e-2,
        "m_per_sec": 1.0,
        "km_per_sec": 1e3,
        "inches_per_sec": METER2IN,
        "feet_per_sec": METER2IN * 12,
        "feet_per_min": METER2IN * 12 * SEC2MIN,
        "km_per_min": 60e3,
        "m_per_h": 3600,
        "miles_per_hour": METER2MILES * SEC2HOUR,
        "miles_per_minute": METER2MILES * SEC2MIN,
        "miles_per_sec": METER2MILES,
    },
    "Time": {
        "fs": 1e-15,
        "ps": 1e-12,
        "ns": 1e-9,
        "us": 1e-6,
        "ms": 1e-3,
        "s": 1,
        "min": 60,
        "hour": 3600,
        "day": 3600 * 12,
    },
    "Torque": {
        "fNewtonMeter": 1e-15,
        "pNewtonMeter": 1e-12,
        "nNewtonMeter": 1e-9,
        "uNewtonMeter": 1e-6,
        "mNewtonMeter": 1e-3,
        "cNewtonMeter": 1e-2,
        "NewtonMeter": 1,
        "kNewtonMeter": 1e3,
        "megNewtonMeter": 1e6,
        "gNewtonMeter": 1e9,
    },
    "Voltage": {
        "fV": 1e-15,
        "pV": 1e-12,
        "nV": 1e-9,
        "uV": 1e-6,
        "mV": 1e-3,
        "V": 1.0,
        "kV": 1e3,
        "MegV": 1e6,
        "gV": 1e9,
        "dBV": (db20,),
    },
    "Temperature": {"kel": 1.0, "cel": (cel2kel,), "fah": (fah2kel,)},
    "Power": {
        "fW": 1e-15,
        "pW": 1e-12,
        "nW": 1e-9,
        "uW": 1e-6,
        "mW": 1e-3,
        "W": 1.0,
        "kW": 1e3,
        "megW": 1e6,
        "gW": 1e9,
    },
    "B-field": {
        "ftesla": 1e-15,
        "ptesla": 1e-12,
        "ntesla": 1e-9,
        "utesla": 1e-6,
        "mtesla": 1e-3,
        "tesla": 1.0,
        "ktesla": 1e3,
        "megtesla": 1e6,
        "gtesla": 1e9,
    },
    "H-field": {
        "fA_per_m": 1e-15,
        "pA_per_m": 1e-12,
        "nA_per_m": 1e-9,
        "uA_per_m": 1e-6,
        "mA_per_m": 1e-3,
        "A_per_m": 1.0,
        "kA_per_m": 1e3,
        "megA_per_m": 1e6,
        "gA_per_m": 1e9,
    },
}
SI_UNITS = {
    "AngularSpeed": "rad_per_sec",
    "Angle": "rad",
    "Current": "A",
    "Flux": "vs",
    "Force": "newton",
    "Freq": "Hz",
    "Inductance": "H",
    "Length": "meter",
    "Mass": "kg",
    "None": "",
    "Resistance": "ohm",
    "Time": "s",
    "Torque": "NewtonMeter",
    "Voltage": "V",
    "Temperature": "kel",
    "Power": "W",
    "B-field": "tesla",
    "H-field": "A_per_m",
}
UNIT_SYSTEM_OPERATIONS = {
    # Multiplication of physical domains
    "Voltage_multiply_Current": "Power",
    "Torque_multiply_AngularSpeed": "Power",
    "AngularSpeed_multiply_Time": "Angle",
    "Current_multiply_Resistance": "Voltage",
    "AngularSpeed_multiply_Inductance": "Resistance",
    "Speed_multiply_Time": "Length",
    # Division of Physical Domains
    "Power_divide_Voltage": "Current",
    "Power_divide_Current": "Voltage",
    "Power_divide_AngularSpeed": "Torque",
    "Power_divide_Torque": "AngularSpeed",
    "Angle_divide_AngularSpeed": "Time",
    "Angle_divide_Time": "AngularSpeed",
    "Voltage_divide_Current": "Resistance",
    "Voltage_divide_Resistance": "Current",
    "Resistance_divide_AngularSpeed": "Inductance",
    "Resistance_divide_Inductance": "AngularSpeed",
    "None_divide_Freq": "Time",
    "None_divide_Time": "Freq",
    "Length_divide_Time": "Speed",
    "Length_divide_Speed": "Time",
}


class FILLET(object):
    """FilletType Enumerator class."""

    (Round, Mitered) = range(0, 2)


class AXIS(object):
    """CoordinateSystemAxis Enumerator class."""

    (X, Y, Z) = range(0, 3)


class PLANE(object):
    """CoordinateSystemPlane Enumerator class."""

    (YZ, ZX, XY) = range(0, 3)


class GRAVITY(object):
    """GravityDirection Enumerator class."""

    (XNeg, YNeg, ZNeg, XPos, YPos, ZPos) = range(0, 6)


class VIEW(object):
    """View Enumerator class."""

    (XY, YZ, ZX, ISO) = ("XY", "YZ", "ZX", "iso")


class GLOBALCS(object):
    """GlobalCS Enumerator class."""

    (XY, YZ, ZX) = ("Global_XY", "Global_YZ", "Global:XZ")


class CSMODE(object):
    """COORDINATE SYSTEM MODE Enumerator class."""

    (View, Axis, ZXZ, ZYZ, AXISROTATION) = ("view", "axis", "zxz", "zyz", "axisrotation")


class SEGMENTTYPE(object):
    """CROSSSECTION Enumerator class."""

    (Line, Arc, Spline, AngularArc) = range(0, 4)


class CROSSSECTION(object):
    """CROSSSECTION Enumerator class."""

    (NONE, Line, Circle, Rectangle, Trapezoid) = range(0, 5)


class SWEEPDRAFT(object):
    """SweepDraftType Enumerator class."""

    (Extended, Round, Natural, Mixed) = range(0, 4)


class SOLUTIONS(object):
    """Provides the names of default solution types."""

    class Hfss(object):
        """Provides HFSS solution types."""

        (DrivenModal, DrivenTerminal, EigenMode, Transient, SBR) = (
            "DrivenModal",
            "DrivenTerminal",
            "EigenMode",
            "Transient Network",
            "SBR+",
        )

    class Maxwell3d(object):
        """Provides Maxwell 3D solution types."""

        (Transient, Magnetostatic, EddyCurrent, ElectroStatic, ElectroDCConduction, ElectroDCTransient) = (
            "Transient",
            "Magnetostatic",
            "EddyCurrent",
            "Electrostatic",
            "ElectroDCConduction",
            "ElectricTransient",
        )

    class Maxwell2d(object):
        """Provides Maxwell 2D solution types."""

        (
            TransientXY,
            TransientZ,
            MagnetostaticXY,
            MagnetostaticZ,
            EddyCurrentXY,
            EddyCurrentZ,
            ElectroStaticXY,
            ElectroStaticZ,
            ElectroDCConductionX,
            ElectroDCConductionZ,
            ElectroDCTransientXY,
            ElectroDCTransientZ,
        ) = (
            "TransientXY",
            "TransientZ",
            "MagnetostaticXY",
            "MagnetostaticZ",
            "EddyCurrentXY",
            "EddyCurrentZ",
            "ElectrostaticXY",
            "ElectrostaticZ",
            "ElectroDCConductionXY",
            "ElectroDCConductionZ",
            "ElectricTransientXY",
            "ElectricTransientZ",
        )

    class Icepak(object):
        """Provides Icepak solution types."""

        (
            SteadyTemperatureAndFlow,
            SteadyTemperatureOnly,
            SteadyFlowOnly,
            TransientTemperatureAndFlow,
            TransientTemperatureOnly,
            TransientFlowOnly,
        ) = (
            "SteadyTemperatureAndFlow",
            "SteadyTemperatureOnly",
            "SteadyFlowOnly",
            "TransientTemperatureAndFlow",
            "TransientTemperatureOnly",
            "TransientFlowOnly",
        )

    class Circuit(object):
        """Provides Circuit solution types."""

        (
            NexximLNA,
            NexximDC,
            NexximTransient,
            NexximQuickEye,
            NexximVerifEye,
            NexximAMI,
            NexximOscillatorRSF,
            NexximOscillator1T,
            NexximOscillatorNT,
            NexximHarmonicBalance1T,
            NexximHarmonicBalanceNT,
            NexximSystem,
            NexximTVNoise,
            HSPICE,
            TR,
        ) = (
            "NexximLNA",
            "NexximDC",
            "NexximTransient",
            "NexximQuickEye",
            "NexximVerifEye",
            "NexximAMI",
            "NexximOscillatorRSF",
            "NexximOscillator1T",
            "NexximOscillatorNT",
            "NexximHarmonicBalance1T",
            "NexximHarmonicBalanceNT",
            "NexximSystem",
            "NexximTVNoise",
            "HSPICE",
            "TR",
        )

    class Mechanical(object):
        """Provides Mechanical solution types."""

        (Thermal, Structural, Modal) = ("Thermal", "Structural", "Modal")


class SETUPS(object):
    """Provides constants for the default setup types."""

    (
        HFSSDrivenAuto,
        HFSSDrivenDefault,
        HFSSEigen,
        HFSSTransient,
        HFSSSBR,
        MaxwellTransient,
        Magnetostatic,
        EddyCurrent,
        Electrostatic,
        ElectrostaticDC,
        ElectricTransient,
        SteadyTemperatureAndFlow,
        SteadyTemperatureOnly,
        SteadyFlowOnly,
        Matrix,
        NexximLNA,
        NexximDC,
        NexximTransient,
        NexximQuickEye,
        NexximVerifEye,
        NexximAMI,
        NexximOscillatorRSF,
        NexximOscillator1T,
        NexximOscillatorNT,
        NexximHarmonicBalance1T,
        NexximHarmonicBalanceNT,
        NexximSystem,
        NexximTVNoise,
        HSPICE,
        HFSS3DLayout,
        Open,
        Close,
        MechTerm,
        MechModal,
        GRM,
        TR,
        TransientTemperatureAndFlow,
        TransientTemperatureOnly,
        TransientFlowOnly,
    ) = range(0, 39)


class CoordinateSystemAxis(object):
    """CoordinateSystemAxis class.

    .. deprecated:: 0.4.8
        Use :func:`AXIS` instead."""

    (XAxis, YAxis, ZAxis) = range(0, 3)


class CoordinateSystemPlane(object):
    """CoordinateSystemPlane class.

    .. deprecated:: 0.4.8
        Use :func:`PLANE` instead."""

    (YZPlane, ZXPlane, XYPlane) = range(0, 3)


class Plane(object):
    """Plane class.

    .. deprecated:: 0.4.8
        Use :func:`VIEW` instead."""

    (XYPlane, YZPlane, ZXPlane, ISO) = ("XY", "YZ", "ZX", "iso")


class GravityDirection(object):
    """GravityDirection class.

    .. deprecated:: 0.4.8
        Use :func:`GRAVITY` instead."""

    (XNeg, YNeg, ZNeg, XPos, YPos, ZPos) = range(0, 6)