from zigpy import types
from zigpy.profiles import zha

from zigpy.zcl.foundation import DataTypeId, ZCLAttributeDef
from zigpy.zcl.clusters.general import (
    Basic,
    Identify,
    Groups,
    Scenes,
    OnOff,
    MultistateInput,
    Time,
    Ota,
)
from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement

from zigpy.quirks.v2 import QuirkBuilder

from zhaquirks.const import (
    COMMAND,
    COMMAND_SINGLE,
    COMMAND_DOUBLE,
    COMMAND_HOLD,
    COMMAND_RELEASE,
    BUTTON,
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
)
from zhaquirks.xiaomi import XiaomiAqaraE1Cluster


# ---------------------------------------------------------------------
# Manufacturer specific cluster (0xFCC0)
# ---------------------------------------------------------------------
class AqaraManuSpecificCluster(XiaomiAqaraE1Cluster):
    """Aqara manufacturer-specific cluster for H2 switch."""

    class AttributeDefs(XiaomiAqaraE1Cluster.AttributeDefs):
        lock_relay = ZCLAttributeDef(
            id=0x0285,
            type=types.uint8_t,
            zcl_type=DataTypeId.uint8,
            access="rw",
            is_manufacturer_specific=True,
        )

        multi_click = ZCLAttributeDef(
            id=0x0286,
            type=types.uint8_t,
            zcl_type=DataTypeId.uint8,
            access="rw",
            is_manufacturer_specific=True,
        )


# ---------------------------------------------------------------------
# Quirk definition
# ---------------------------------------------------------------------
(
    QuirkBuilder("Aqara", "lumi.switch.agl006")
    .applies_to("LUMI", "lumi.switch.agl006")

    # --- Endpoints (must match signature exactly) ---------------------
    .adds_endpoint(1, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Relay + Button 1
    .adds_endpoint(2, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Relay + Button 2
    .adds_endpoint(3, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Relay + Button 3
    .adds_endpoint(4, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Virtual Button 4
    .adds_endpoint(5, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Utility
    .adds_endpoint(21, device_type=zha.DeviceType.ON_OFF_SWITCH)  # Diagnostics

    # --- Cluster replacements ---------------------------------------
    .adds(Basic, endpoint_id=1)
    .adds(Identify, endpoint_id=1)
    .adds(Groups, endpoint_id=1)
    .adds(Scenes, endpoint_id=1)
    .adds(OnOff, endpoint_id=1)
    .adds(Metering, endpoint_id=1)
    .adds(ElectricalMeasurement, endpoint_id=1)
    .adds(Ota, endpoint_id=1)
    
    .adds(Time, endpoint_id=21)

    .replaces(MultistateInput, endpoint_id=1)
    .replaces(MultistateInput, endpoint_id=2)
    .replaces(MultistateInput, endpoint_id=3)
    .replaces(MultistateInput, endpoint_id=4)

    .replaces(AqaraManuSpecificCluster, endpoint_id=1)
    .replaces(AqaraManuSpecificCluster, endpoint_id=2)
    .replaces(AqaraManuSpecificCluster, endpoint_id=3)
    .replaces(AqaraManuSpecificCluster, endpoint_id=4)
    .replaces(AqaraManuSpecificCluster, endpoint_id=5)


    # --- Relay lock switches (disable physical relay) ----------------
    .switch(
        AqaraManuSpecificCluster.AttributeDefs.lock_relay.name,
        AqaraManuSpecificCluster.cluster_id,
        endpoint_id=1,
        translation_key="lock_relay_1",
        fallback_name="Disable relay 1",
        unique_id_suffix="relay_1",
        off_value=0,
        on_value=1,
    )
    .switch(
        AqaraManuSpecificCluster.AttributeDefs.lock_relay.name,
        AqaraManuSpecificCluster.cluster_id,
        endpoint_id=2,
        translation_key="lock_relay_2",
        fallback_name="Disable relay 2",
        unique_id_suffix="relay_2",
        off_value=0,
        on_value=1,
    )
    .switch(
        AqaraManuSpecificCluster.AttributeDefs.lock_relay.name,
        AqaraManuSpecificCluster.cluster_id,
        endpoint_id=3,
        translation_key="lock_relay_3",
        fallback_name="Disable relay 3",
        unique_id_suffix="relay_3",
        off_value=0,
        on_value=1,
    )

    # --- Button automation triggers ----------------------------------
    .device_automation_triggers(
        {
            (COMMAND_SINGLE, BUTTON_1): {COMMAND: "button_1_single"},
            (COMMAND_DOUBLE, BUTTON_1): {COMMAND: "button_1_double"},
            (COMMAND_HOLD, BUTTON_1): {COMMAND: "button_1_hold"},
            (COMMAND_RELEASE, BUTTON_1): {COMMAND: "button_1_release"},

            (COMMAND_SINGLE, BUTTON_2): {COMMAND: "button_2_single"},
            (COMMAND_DOUBLE, BUTTON_2): {COMMAND: "button_2_double"},
            (COMMAND_HOLD, BUTTON_2): {COMMAND: "button_2_hold"},
            (COMMAND_RELEASE, BUTTON_2): {COMMAND: "button_2_release"},

            (COMMAND_SINGLE, BUTTON_3): {COMMAND: "button_3_single"},
            (COMMAND_DOUBLE, BUTTON_3): {COMMAND: "button_3_double"},
            (COMMAND_HOLD, BUTTON_3): {COMMAND: "button_3_hold"},
            (COMMAND_RELEASE, BUTTON_3): {COMMAND: "button_3_release"},

            (COMMAND_SINGLE, BUTTON_4): {COMMAND: "button_4_single"},
            (COMMAND_DOUBLE, BUTTON_4): {COMMAND: "button_4_double"},
            (COMMAND_HOLD, BUTTON_4): {COMMAND: "button_4_hold"},
            (COMMAND_RELEASE, BUTTON_4): {COMMAND: "button_4_release"},
        }
    )

    .add_to_registry()
)
