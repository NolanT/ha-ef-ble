import time

from ..devicebase import AdvertisementData, BLEDevice, DeviceBase
from ..packet import Packet
from ..pb import dev_apl_comm_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)


def _round2(value: float):
    return round(value, 2)


class Device(DeviceBase, ProtobufProps):
    """Smart Panel 40 (EF-SHP-40)"""

    SN_PREFIX = (b"HR6H",)
    NAME_PREFIX = "EF-HR6H"

    @classmethod
    def check(cls, sn: bytes) -> bool:
        return sn[:4] == b"HR6H"

    # Grid
    grid_voltage = pb_field(pb.grid_connection_vol, _round2)
    grid_current = pb_field(pb.grid_connection_amp, _round2)
    grid_frequency = pb_field(pb.grid_connection_freq, _round2)
    grid_status = pb_field(pb.grid_connection_sta)
    grid_is_energized = pb_field(pb.grid_is_energized)
    grid_relay_state = pb_field(pb.grid_rly_state)
    grid_apparent_power = pb_field(pb.grid_connection_apparent_power, _round2)
    grid_power_l1 = pb_field(pb.grid_connection_power_l1, _round2)
    grid_power_l2 = pb_field(pb.grid_connection_power_l2, _round2)
    grid_voltage_l1 = pb_field(pb.grid_connection_vol_l1, _round2)
    grid_voltage_l2 = pb_field(pb.grid_connection_vol_l2, _round2)
    grid_current_l1 = pb_field(pb.grid_connection_amp_l1, _round2)
    grid_current_l2 = pb_field(pb.grid_connection_amp_l2, _round2)
    grid_frequency_l1 = pb_field(pb.grid_connection_freq_l1, _round2)
    grid_frequency_l2 = pb_field(pb.grid_connection_freq_l2, _round2)
    grid_type = pb_field(pb.grid_type)

    # Panel
    bus_voltage = pb_field(pb.panel_bus_vol, _round2)
    circuit_voltage = pb_field(pb.load_ch_vol, _round2)

    # CT sensors
    ct1_current = pb_field(pb.ct1_current, _round2)
    ct2_current = pb_field(pb.ct2_current, _round2)
    ct3_current = pb_field(pb.ct3_current, _round2)
    ct1_power = pb_field(pb.ct1_active_pwr, _round2)
    ct2_power = pb_field(pb.ct2_active_pwr, _round2)
    ct3_power = pb_field(pb.ct3_active_pwr, _round2)

    # Circuit status (ch_sta field of each LoadChSta message)
    circuit_1_status = pb_field(pb.load_ch1_sta.ch_sta)
    circuit_2_status = pb_field(pb.load_ch2_sta.ch_sta)
    circuit_3_status = pb_field(pb.load_ch3_sta.ch_sta)
    circuit_4_status = pb_field(pb.load_ch4_sta.ch_sta)
    circuit_5_status = pb_field(pb.load_ch5_sta.ch_sta)
    circuit_6_status = pb_field(pb.load_ch6_sta.ch_sta)
    circuit_7_status = pb_field(pb.load_ch7_sta.ch_sta)
    circuit_8_status = pb_field(pb.load_ch8_sta.ch_sta)
    circuit_9_status = pb_field(pb.load_ch9_sta.ch_sta)
    circuit_10_status = pb_field(pb.load_ch10_sta.ch_sta)
    circuit_11_status = pb_field(pb.load_ch11_sta.ch_sta)
    circuit_12_status = pb_field(pb.load_ch12_sta.ch_sta)
    circuit_13_status = pb_field(pb.load_ch13_sta.ch_sta)
    circuit_14_status = pb_field(pb.load_ch14_sta.ch_sta)
    circuit_15_status = pb_field(pb.load_ch15_sta.ch_sta)
    circuit_16_status = pb_field(pb.load_ch16_sta.ch_sta)
    circuit_17_status = pb_field(pb.load_ch17_sta.ch_sta)
    circuit_18_status = pb_field(pb.load_ch18_sta.ch_sta)
    circuit_19_status = pb_field(pb.load_ch19_sta.ch_sta)
    circuit_20_status = pb_field(pb.load_ch20_sta.ch_sta)
    circuit_21_status = pb_field(pb.load_ch21_sta.ch_sta)
    circuit_22_status = pb_field(pb.load_ch22_sta.ch_sta)
    circuit_23_status = pb_field(pb.load_ch23_sta.ch_sta)
    circuit_24_status = pb_field(pb.load_ch24_sta.ch_sta)
    circuit_25_status = pb_field(pb.load_ch25_sta.ch_sta)
    circuit_26_status = pb_field(pb.load_ch26_sta.ch_sta)
    circuit_27_status = pb_field(pb.load_ch27_sta.ch_sta)
    circuit_28_status = pb_field(pb.load_ch28_sta.ch_sta)
    circuit_29_status = pb_field(pb.load_ch29_sta.ch_sta)
    circuit_30_status = pb_field(pb.load_ch30_sta.ch_sta)
    circuit_31_status = pb_field(pb.load_ch31_sta.ch_sta)
    circuit_32_status = pb_field(pb.load_ch32_sta.ch_sta)
    circuit_33_status = pb_field(pb.load_ch33_sta.ch_sta)
    circuit_34_status = pb_field(pb.load_ch34_sta.ch_sta)
    circuit_35_status = pb_field(pb.load_ch35_sta.ch_sta)
    circuit_36_status = pb_field(pb.load_ch36_sta.ch_sta)
    circuit_37_status = pb_field(pb.load_ch37_sta.ch_sta)
    circuit_38_status = pb_field(pb.load_ch38_sta.ch_sta)
    circuit_39_status = pb_field(pb.load_ch39_sta.ch_sta)
    circuit_40_status = pb_field(pb.load_ch40_sta.ch_sta)

    # Circuit power (watts from LoadChSampleInfo)
    circuit_1_power = pb_field(pb.load_ch1_sample_info.load_ch_watts, _round2)
    circuit_2_power = pb_field(pb.load_ch2_sample_info.load_ch_watts, _round2)
    circuit_3_power = pb_field(pb.load_ch3_sample_info.load_ch_watts, _round2)
    circuit_4_power = pb_field(pb.load_ch4_sample_info.load_ch_watts, _round2)
    circuit_5_power = pb_field(pb.load_ch5_sample_info.load_ch_watts, _round2)
    circuit_6_power = pb_field(pb.load_ch6_sample_info.load_ch_watts, _round2)
    circuit_7_power = pb_field(pb.load_ch7_sample_info.load_ch_watts, _round2)
    circuit_8_power = pb_field(pb.load_ch8_sample_info.load_ch_watts, _round2)
    circuit_9_power = pb_field(pb.load_ch9_sample_info.load_ch_watts, _round2)
    circuit_10_power = pb_field(pb.load_ch10_sample_info.load_ch_watts, _round2)
    circuit_11_power = pb_field(pb.load_ch11_sample_info.load_ch_watts, _round2)
    circuit_12_power = pb_field(pb.load_ch12_sample_info.load_ch_watts, _round2)
    circuit_13_power = pb_field(pb.load_ch13_sample_info.load_ch_watts, _round2)
    circuit_14_power = pb_field(pb.load_ch14_sample_info.load_ch_watts, _round2)
    circuit_15_power = pb_field(pb.load_ch15_sample_info.load_ch_watts, _round2)
    circuit_16_power = pb_field(pb.load_ch16_sample_info.load_ch_watts, _round2)
    circuit_17_power = pb_field(pb.load_ch17_sample_info.load_ch_watts, _round2)
    circuit_18_power = pb_field(pb.load_ch18_sample_info.load_ch_watts, _round2)
    circuit_19_power = pb_field(pb.load_ch19_sample_info.load_ch_watts, _round2)
    circuit_20_power = pb_field(pb.load_ch20_sample_info.load_ch_watts, _round2)
    circuit_21_power = pb_field(pb.load_ch21_sample_info.load_ch_watts, _round2)
    circuit_22_power = pb_field(pb.load_ch22_sample_info.load_ch_watts, _round2)
    circuit_23_power = pb_field(pb.load_ch23_sample_info.load_ch_watts, _round2)
    circuit_24_power = pb_field(pb.load_ch24_sample_info.load_ch_watts, _round2)
    circuit_25_power = pb_field(pb.load_ch25_sample_info.load_ch_watts, _round2)
    circuit_26_power = pb_field(pb.load_ch26_sample_info.load_ch_watts, _round2)
    circuit_27_power = pb_field(pb.load_ch27_sample_info.load_ch_watts, _round2)
    circuit_28_power = pb_field(pb.load_ch28_sample_info.load_ch_watts, _round2)
    circuit_29_power = pb_field(pb.load_ch29_sample_info.load_ch_watts, _round2)
    circuit_30_power = pb_field(pb.load_ch30_sample_info.load_ch_watts, _round2)
    circuit_31_power = pb_field(pb.load_ch31_sample_info.load_ch_watts, _round2)
    circuit_32_power = pb_field(pb.load_ch32_sample_info.load_ch_watts, _round2)
    circuit_33_power = pb_field(pb.load_ch33_sample_info.load_ch_watts, _round2)
    circuit_34_power = pb_field(pb.load_ch34_sample_info.load_ch_watts, _round2)
    circuit_35_power = pb_field(pb.load_ch35_sample_info.load_ch_watts, _round2)
    circuit_36_power = pb_field(pb.load_ch36_sample_info.load_ch_watts, _round2)
    circuit_37_power = pb_field(pb.load_ch37_sample_info.load_ch_watts, _round2)
    circuit_38_power = pb_field(pb.load_ch38_sample_info.load_ch_watts, _round2)
    circuit_39_power = pb_field(pb.load_ch39_sample_info.load_ch_watts, _round2)
    circuit_40_power = pb_field(pb.load_ch40_sample_info.load_ch_watts, _round2)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        if packet.src == 0x02 and packet.cmdSet == 0xFE and packet.cmdId == 0x15:
            self.update_from_bytes(
                dev_apl_comm_pb2.DisplayPropertyUpload, packet.payload
            )
            processed = True

        for field_name in self.updated_fields:
            self.update_callback(field_name)
            self.update_state(field_name, getattr(self, field_name))

        return processed

    async def _send_config_packet(self, message: dev_apl_comm_pb2.ConfigWrite):
        message.cfg_utc_time = round(time.time())
        payload = message.SerializeToString()
        packet = Packet(0x20, 0x02, 0xFE, 0x11, payload, 0x01, 0x01, 0x13)
        await self._conn.sendPacket(packet)
