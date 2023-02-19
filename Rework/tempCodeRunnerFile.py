result = []
        # for col in self.testDB["WebDB"].find({},{"_id":0,"key":1,"value":1}):
        #     col_dict = dict()
        #     col_dict["key"] = col["key"]
        #     col_dict["value"] = col["value"]
        #     result.append(col_dict)
        # self.assertEqual(result,[{"key":"key1","value":{"www.testcase01.com":2}},{"key":"key2","value":{"www.testcase01.com":2}}])