
import pandas as pd
import logging

from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
logging.basicConfig(level=logging.DEBUG)

FilePath = r"D:\CONTROLYTICS\SIVA_M_WORK\THINGSBOARD\thd.xlsx"
print(FilePath)
xls = pd.ExcelFile(FilePath)
# print(xls.sheet_names)


def main():
    for sheet_name in xls.sheet_names:
        print(sheet_name)
        df = pd.read_excel(FilePath, sheet_name=sheet_name, index_col=None)
        res = df.Topic.count()
        # print(res)
        if sheet_name == 'Sheet1':
            for i in range(0, res):
                client = TBDeviceMqttClient(df.Broker[i], 1883,df.Token[i])
                client.connect()
                data = {"ts": int(df.timestamp[i]), "values": {str(df.Key1[i]): str(df.Value1[i]),
                                                               str(df.Key2[i]): str(df.Value2[i]),
                                                               str(df.Key3[i]): str(df.Value3[i]),
                                                               }}
                topic = df.Topic[i]
                print(i, data)
                result = client.publish_data(data, topic, 1)
                print("Attribute update sent: " +
                      str(result.rc() == TBPublishInfo.TB_ERR_SUCCESS))
                result.get()
                print(result)
                print("Telemetry update sent: " +
                      str(result.rc() == TBPublishInfo.TB_ERR_SUCCESS))
                client.stop()


if __name__ == '__main__':
    main()
