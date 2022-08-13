from django.db import connections


class Filter:
    def __init__(self, tot='Все', db='demo_db'):
        self.cursor = connections[db].cursor()
        self.total = tot

    def prepare_data(self, fetched_data):
        data = [item[0] for item in fetched_data]
        data.append(self.total)
        return data

    def get_clients(self):
        res = self.cursor.execute('SELECT clients.name FROM clients').fetchall()
        return self.prepare_data(res)

    def get_equips(self):
        res = self.cursor.execute('SELECT equipment.name FROM equipment').fetchall()
        return self.prepare_data(res)

    def get_modes(self):
        res = self.cursor.execute('SELECT modes.name FROM modes').fetchall()
        return self.prepare_data(res)

    def client_filter(self, client):
        if client != self.total:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM clients as cl LEFT JOIN durations as dr on cl.id = dr.client_id '
                                      'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                      'LEFT JOIN modes as md on md.id = dr.mode_id '
                                      'WHERE cl.name = %s', [client]).fetchall()
        else:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM clients as cl LEFT JOIN durations as dr on cl.id = dr.client_id '
                                      'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                      'LEFT JOIN modes as md on md.id = dr.mode_id ').fetchall()
        return res

    def equipment_filter(self, equipment):
        if equipment != self.total:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM equipment as eq LEFT JOIN durations as dr on eq.id = dr.equipment_id '
                                      'LEFT JOIN clients as cl on cl.id = dr.client_id '
                                      'LEFT JOIN modes as md on md.id = dr.mode_id '
                                      'WHERE eq.name = %s', [equipment]).fetchall()
        else:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM equipment as eq LEFT JOIN durations as dr on eq.id = dr.equipment_id '
                                      'LEFT JOIN clients as cl on cl.id = dr.client_id '
                                      'LEFT JOIN modes as md on md.id = dr.mode_id ').fetchall()
        return res

    def mode_filter(self, mode):
        if mode != self.total:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM modes as md LEFT JOIN durations as dr on md.id = dr.mode_id '
                                      'LEFT JOIN clients as cl on cl.id = dr.client_id '
                                      'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                      'WHERE md.name = %s', [mode]).fetchall()
        else:
            res = self.cursor.execute('SELECT cl.name, eq.name,'
                                      'dr.start, dr.stop, dr.minutes, md.name '
                                      'FROM modes as md LEFT JOIN durations as dr on md.id = dr.mode_id '
                                      'LEFT JOIN clients as cl on cl.id = dr.client_id '
                                      'LEFT JOIN equipment as eq on eq.id = dr.equipment_id ').fetchall()
        return res

    def minute_filter(self, minute):
        res = self.cursor.execute('SELECT cl.name, eq.name,'
                                  'dr.start, dr.stop, dr.minutes, md.name '
                                  'FROM durations as dr LEFT JOIN clients as cl on cl.id = dr.client_id '
                                  'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                  'LEFT JOIN modes as md on md.id = dr.mode_id '
                                  'WHERE dr.minutes <= %s', [minute]).fetchall()
        return res

    def start_date_filter(self, _date):
        res = self.cursor.execute('SELECT cl.name, eq.name,'
                                  'dr.start, dr.stop, dr.minutes, md.name '
                                  'FROM durations as dr LEFT JOIN clients as cl on cl.id = dr.client_id '
                                  'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                  'LEFT JOIN modes as md on md.id = dr.mode_id '
                                  'WHERE strftime( \'%%Y-%%m-%%d\', dr.start) = %s', [_date]).fetchall()
        return res

    def start_time_filter(self, _time):
        res = self.cursor.execute('SELECT cl.name, eq.name,'
                                  'dr.start, dr.stop, dr.minutes, md.name '
                                  'FROM durations as dr LEFT JOIN clients as cl on cl.id = dr.client_id '
                                  'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                  'LEFT JOIN modes as md on md.id = dr.mode_id '
                                  'WHERE strftime( \'%%H:%%M\', dr.start) = %s', [_time]).fetchall()
        return res

    def end_date_filter(self, _date):
        res = self.cursor.execute('SELECT cl.name, eq.name,'
                                  'dr.start, dr.stop, dr.minutes, md.name '
                                  'FROM durations as dr LEFT JOIN clients as cl on cl.id = dr.client_id '
                                  'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                  'LEFT JOIN modes as md on md.id = dr.mode_id '
                                  'WHERE strftime( \'%%Y-%%m-%%d\', dr.stop) = %s', [_date]).fetchall()
        return res

    def end_time_filter(self, _time):
        res = self.cursor.execute('SELECT cl.name, eq.name,'
                                  'dr.start, dr.stop, dr.minutes, md.name '
                                  'FROM durations as dr LEFT JOIN clients as cl on cl.id = dr.client_id '
                                  'LEFT JOIN equipment as eq on eq.id = dr.equipment_id '
                                  'LEFT JOIN modes as md on md.id = dr.mode_id '
                                  'WHERE strftime( \'%%H:%%M\', dr.stop) = %s', [_time]).fetchall()
        return res
