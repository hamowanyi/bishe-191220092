import torch
import torch.nn as nn
import torch.utils.data as Data


'''
    def useData(self,path):
        if path not in self.dataPath:
            self.dataPath.append(path)
        vpath = r"".join([path])
        data = pd.read_json(vpath, orient='records', lines=True)
        self.data[path]=data
        df = data[["code", "docstring"]]
        for i in range(10):
            X = df.loc[i]
            X = X.values
            X.tolist()
            # print(X[0])
            pb_model = Prompt_base(X[0], X[1], tokenizer_str='Salesforce/codet5-large',
                                   model_str='Salesforce/codet5-large')
            self.scoreList.append(pb_model.output())

    def func(self):
        loader = Data.DataLoader(
            # 从数据库中每次抽出batch size个样本
            dataset=torch_dataset,  # torch TensorDataset format
            batch_size=BATCH_SIZE,  # mini batch size
            shuffle=True,  # 要不要打乱数据 (打乱比较好)
            num_workers=2,  # 多线程来读数据
        )

    def show_batch(self):
        for epoch in range(3):
            for step, (batch_x, batch_y) in enumerate(loader):
                # training
                print("steop:{}, batch_x:{}, batch_y:{}".format(step, batch_x, batch_y))


'''
'''
    def test(self):


        spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName(
            "readJSON").getOrCreate()

        readJSONDF = spark.read.json('Simple.json')
        readJSONDF.show(truncate=False)'''
