import numpy as np
import pandas as pd
from font import get_font_data
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def main():
    # 处理缺失值
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(pd.DataFrame(get_font_data())))

    # 取出特征值\目标值
    x = data.drop([0], axis=1)
    y = data[0]

    # 分割数据集
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    x_train = x.head(10)
    y_train = y.head(10)
    print(x_train)
    print(y_train)
    x_test = x.tail(70)
    y_test = y.tail(70)

    # 标准化
    # std = StandardScaler()
    # x_train = std.fit_transform(x_train)
    # x_test = std.transform(x_test)

    # 进行算法流程
    knn = KNeighborsClassifier(n_neighbors=1)
    # 开始训练
    knn.fit(x_train, y_train)
    # 预测结果
    y_predict = knn.predict(x_test)
    print(y)
    # 得出准确率
    print(knn.score(x_test, y_test))

if __name__ == '__main__':
    main()
