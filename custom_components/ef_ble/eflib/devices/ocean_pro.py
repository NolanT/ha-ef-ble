import time

from ..devicebase import AdvertisementData, BLEDevice, DeviceBase
from ..packet import Packet
from ..pb import dev_apl_comm_pb2
from ..props import ProtobufProps, pb_field, proto_attr_mapper

pb = proto_attr_mapper(dev_apl_comm_pb2.DisplayPropertyUpload)
pb_rt = proto_attr_mapper(dev_apl_comm_pb2.RuntimePropertyUpload)


def _round2(value: float):
    return round(value, 2)


class Device(DeviceBase, ProtobufProps):
    """Ocean Pro Hybrid Inverter"""

    SN_PREFIX = (b"HR5N",)
    NAME_PREFIX = "EF-HR5N"

    @classmethod
    def check(cls, sn: bytes) -> bool:
        return sn[:4] == b"HR5N"

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

    # Battery / system
    battery_level = pb_field(pb.panel_generate_energy_soc_cms, _round2)
    battery_status = pb_field(pb.panel_generate_energy_battery_sta_cms)
    battery_power = pb_field(pb.panel_generate_energy_battery_power_cms, _round2)
    system_run_state = pb_field(pb.panel_generate_energy_run_sta)

    # PV / solar
    pv_power = pb_field(pb.pow_home_energy_pv_in_cms, _round2)
    pv_external_power = pb_field(pb.pow_exter_pv_inv_in_w, _round2)

    # Inverter
    inv_target_voltage = pb_field(pb.inv_target_vol)
    bus_voltage = pb_field(pb.panel_bus_vol, _round2)
    rated_power = pb_field(pb.dev_rate_power, _round2)

    # Feed-in
    feed_grid_mode = pb_field(pb.feed_grid_mode)
    feed_grid_power_limit = pb_field(pb.feed_grid_mode_pow_limit, _round2)
    feed_grid_power_max = pb_field(pb.feed_grid_mode_pow_max, _round2)

    # Generator
    standby_generator_power = pb_field(pb.pow_get_standy_generator, _round2)
    portable_generator_power = pb_field(pb.pow_get_portable_generator, _round2)

    # CT sensors
    ct1_current = pb_field(pb.ct1_current, _round2)
    ct2_current = pb_field(pb.ct2_current, _round2)
    ct3_current = pb_field(pb.ct3_current, _round2)
    ct1_power = pb_field(pb.ct1_active_pwr, _round2)
    ct2_power = pb_field(pb.ct2_active_pwr, _round2)
    ct3_power = pb_field(pb.ct3_active_pwr, _round2)

    # Runtime: PCS inverter details
    pcs_grid_voltage_l1 = pb_field(pb_rt.dt_pcs_grid_vol_l1_rms, _round2)
    pcs_grid_voltage_l2 = pb_field(pb_rt.dt_pcs_grid_vol_l2_rms, _round2)
    pcs_grid_current_l1 = pb_field(pb_rt.dt_pcs_grid_curr_l1_rms, _round2)
    pcs_grid_current_l2 = pb_field(pb_rt.dt_pcs_grid_curr_l2_rms, _round2)
    pcs_grid_frequency_l1 = pb_field(pb_rt.dt_pcs_grid_fre_l1, _round2)
    pcs_grid_frequency_l2 = pb_field(pb_rt.dt_pcs_grid_fre_l2, _round2)
    pcs_inv_voltage_l1 = pb_field(pb_rt.dt_pcs_inv_vol_l1_rms, _round2)
    pcs_inv_voltage_l2 = pb_field(pb_rt.dt_pcs_inv_vol_l2_rms, _round2)
    pcs_active_power_l1 = pb_field(pb_rt.dt_pcs_active_power_l1, _round2)
    pcs_active_power_l2 = pb_field(pb_rt.dt_pcs_active_power_l2, _round2)
    pcs_reactive_power_l1 = pb_field(pb_rt.dt_pcs_reactive_power_l1, _round2)
    pcs_reactive_power_l2 = pb_field(pb_rt.dt_pcs_reactive_power_l2, _round2)
    pcs_current_l1 = pb_field(pb_rt.dt_pcs_curr_real_l1, _round2)
    pcs_current_l2 = pb_field(pb_rt.dt_pcs_curr_real_l2, _round2)
    pcs_battery_power = pb_field(pb_rt.dt_pcs_bp_cur_pwr, _round2)
    pcs_warning_code = pb_field(pb_rt.dt_pcs_waring_code)

    def __init__(
        self, ble_dev: BLEDevice, adv_data: AdvertisementData, sn: str
    ) -> None:
        super().__init__(ble_dev, adv_data, sn)

    async def packet_parse(self, data: bytes):
        return Packet.fromBytes(data, xor_payload=True)

    async def data_parse(self, packet: Packet) -> bool:
        processed = False
        self.reset_updated()

        if packet.src == 0x02 and packet.cmdSet == 0xFE:
            if packet.cmdId == 0x15:
                self.update_from_bytes(
                    dev_apl_comm_pb2.DisplayPropertyUpload, packet.payload
                )
                processed = True
            elif packet.cmdId == 0x16:
                self.update_from_bytes(
                    dev_apl_comm_pb2.RuntimePropertyUpload, packet.payload
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
