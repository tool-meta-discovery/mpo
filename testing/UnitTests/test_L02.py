import unittest
import L02Parameter
import L03Discovery
import datetime

# Unit Tests for Parameter Classes
class tests_L02(unittest.TestCase):

    # Numeric Parameter Filter
    def test_Numeric_init_integer(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterNumeric(1.0, '2')
    def test_Numeric_init_list(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterNumeric('1', ['66666666666', 'qwe'])

    def test_Numeric_range_integer(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterNumeric('1', '2').set_lower_range(2)
    def test_Numeric_range_string(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterNumeric('1', '2').set_upper_range('qwe')
    def test_Numeric_range_datetime(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterNumeric('1', '2').set_upper_range(datetime.datetime(2022, 6, 1))

    def test_Numeric_dict_from_hand(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = 12.5
        up = 20.1
        val = 16.0
        para_num1 = L02Parameter.ParameterNumeric(name, desc)
        para_num1.set_current_value(val)
        para_num1.set_lower_range(low)
        para_num1.set_upper_range(up)
        dict = {"name": name,
            "description": desc,
            "type": "numeric",
            "lower_bound": str(low),
            "upper_bound": str(up),
            "start_value": str(val)}
        self.assertEqual(para_num1.get_info_dict(), dict)
    def test_Numeric_dict_from_dict(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = 12.5
        up = 20.1
        val = 16.0
        dict = {"name": name,
                "description": desc,
                "type": "numeric",
                "lower_bound": str(low),
                "upper_bound": str(up),
                "start_value": str(val)}
        # put in complete dictionary
        para_num2 = L02Parameter.ParameterNumeric(name, desc)
        para_num2.set_info_dict(dict)
        self.assertEqual(para_num2.get_info_dict(), dict)

    # Integral Parameter Filter
    def test_Integral_init_integer(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterIntegral(1, '2')
    def test_Integral_init_list(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterIntegral('1', [1, 2])

    def test_Integral_range_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterIntegral('1', '2').set_lower_range(2.0)
    def test_Integral_range_string(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterIntegral('1', '2').set_upper_range('qwe')
    def test_Integral_range_datetime(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterIntegral('1', '2').set_upper_range(datetime.datetime(2022, 6, 1))

    def test_Integral_dict_from_hand(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = 12
        up = 20
        val = 16
        para_num1 = L02Parameter.ParameterIntegral(name, desc)
        para_num1.set_current_value(val)
        para_num1.set_lower_range(low)
        para_num1.set_upper_range(up)
        dict = {"name": name,
            "description": desc,
            "type": "integral",
            "lower_bound": str(low),
            "upper_bound": str(up),
            "start_value": str(val)}
        self.assertEqual(para_num1.get_info_dict(), dict)
    def test_Integral_dict_from_dict(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = 12
        up = 20
        val = 16
        dict = {"name": name,
                "description": desc,
                "type": "integral",
                "lower_bound": str(low),
                "upper_bound": str(up),
                "start_value": str(val)}
        # put in complete dictionary
        para_num2 = L02Parameter.ParameterIntegral(name, desc)
        para_num2.set_info_dict(dict)
        self.assertEqual(para_num2.get_info_dict(), dict)

    # Time-based Parameter Filter
    def test_Time_init_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterTime(1.0, '2')
    def test_Time_init_list(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterTime('1', ['66666666666', 'qwe'])

    def test_Time_range_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterTime('1', '2').set_lower_range(1.0)
    def test_Time_range_string(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterTime('1', '2').set_upper_range('qwe')
    def test_Time_range_integer(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterTime('1', '2').set_upper_range(2)

    def test_Time_dict_from_hand(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        up = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        val = datetime.datetime.utcnow()
        para_num1 = L02Parameter.ParameterTime(name, desc)
        para_num1.set_current_value(val)
        para_num1.set_lower_range(low)
        para_num1.set_upper_range(up)
        dict = {"name": name,
            "description": desc,
            "type": "datetime",
            "lower_bound": str(low),
            "upper_bound": str(up),
            "start_value": str(val)}
        self.assertEqual(para_num1.get_info_dict(), dict)
    def test_Time_dict_from_dict(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        low = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        up = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        val = datetime.datetime.utcnow()
        dict = {"name": name,
            "description": desc,
            "type": "datetime",
            "lower_bound": str(low),
            "upper_bound": str(up),
            "start_value": str(val)}
        # put in complete dictionary
        para_num2 = L02Parameter.ParameterTime(name, desc)
        # ValueError: time data '2022-06-01 00:00:00' does not match format '%Y-%m-%d %H:%M:%S.%f'
        # sollte doch eigentlich gehen?
        para_num2.set_info_dict(dict)
        self.assertEqual(para_num2.get_info_dict(), dict)

    # Fixed-value Parameter Filter
    def test_FixedValue_init_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterFixedValue(1.0, '2', 123)
    def test_FixedValue_init_list(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterFixedValue('1', ['66666666666', 'qwe'], [123, 3254, 785])

    # Set-based Parameter Filter
    def test_Selection_init_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterSelection(1.0, '2')
    def test_Selection_init_list(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterSelection('1', ['66666666666', 'qwe'])

    def test_Selection_set_float(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterSelection('1', '2').set_selection_set(1.0)
    def test_Selection_set_string(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterSelection('1', '2').set_selection_set('qwe')
    def test_Selection_set_datetime(self):
        with self.assertRaises(TypeError):
            L02Parameter.ParameterSelection('1', '2').set_selection_set(datetime.date(2022, 6, 1))

    def test_Selection_dict_from_hand(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        sel_set = [123, 'string', 1.0]
        val = 1.0
        para_num1 = L02Parameter.ParameterSelection(name, desc)
        para_num1.set_selection_set(sel_set)
        para_num1.set_current_value(val)
        dict = {"name": name,
            "description": desc,
            "type": "selection",
            'selection_set':['123', 'string', '1.0'],
            "start_value": str(val)}
        self.assertEqual(para_num1.get_info_dict(), dict)
    def test_Selection_dict_from_dict(self):
        # build dictionary by hand
        name = 'Ein Name'
        desc = 'wichtige12%$3 unit test*()s123'
        sel_set = [123, 'string', 1.0]
        val = 1.0
        dict = {"name": name,
            "description": desc,
            "type": "selection",
            'selection_set':[],
            "start_value": 'None'}
        # put in complete dictionary
        para_num2 = L02Parameter.ParameterSelection(name, desc)
        para_num2.set_info_dict(dict)
        self.assertEqual(para_num2.get_info_dict(), dict)

# Run all Tests
if __name__ == '__main__':
    unittest.main()