import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate, optimize


plt.rcParams['font.family'] = 'Microsoft Yahei'


class SIR:
    def __init__(self, init_i, N):
        """
        :param init_i: 初始感染人数
        :param N: 总人数
        """
        self.__i = init_i
        self.__r = 0.  # 初始康复人数
        self.__N = N
        self.__s = self.__N - self.__i  # 初始易感染总人数
        self.popt = None

    def _sir_model_(self, y, x, beta, gamma):
        """
        SIR 模型的差分方程
        :param y:
        :param x:
        :param beta:
        :param gamma:
        :return:
        """
        S = -beta * y[0] * y[1] / self.__N
        R = gamma * y[1]
        I = -(S + R)
        return S, I, R

    def _fit_odeint_(self, x, beta, gamma):
        """
        用于拟合求解治愈曲线系数 beta、gamma
        :param x:
        :param beta:
        :param gamma:
        :return:
        """
        return integrate.odeint(self._sir_model_,
                                (self.__s, self.__i, self.__r),
                                x, args=(beta, gamma))[:, 2]

    def _ode_(self, x, beta, gamma):
        """
        通过给定初始数据以及拟合系数 beta、gamma 求解 sir 模型曲线
        :param x:
        :param beta:
        :param gamma:
        :return:
        """
        return integrate.odeint(self._sir_model_,
                                (self.__s, self.__i, self.__r),
                                x, args=(beta, gamma))

    def fit(self, X, y):
        # self.popt 即为拟合系数结果
        self.popt, pcov = optimize.curve_fit(self._fit_odeint_, X, y)
        return self

    def predict(self, X):
        if self.popt is not None:
            # 将拟合系数传递给 sir 模型
            return self._ode_(X, *self.popt)
        return None

    def fit_and_predict_plot(self, X, y, s, time):
        """
        绘制 S、I、R 随时间变化的曲线
        :param X:
        :param y:
        :param s:
        :param time:
        :return:
        """
        fig, ax = plt.subplots(1, 3)
        for _, title in enumerate(s):
            ax[_].plot(X, y[title])
            ax[_].plot(X, self.predict(X)[:, _])
            ax[_].set_ylabel('%s人数' % title)
            ax[_].set_title('SIR 模型 - %s' % title)
            ax[_].legend(('%s人数-时间' % title, '预测%s人数-时间' % title))
            ax[_].set_xlabel('时间')
            ax[_].set_xticks([_ * 28 for _ in range(len(time))])
            ax[_].set_xticklabels(time)
        plt.show()


data = pd.read_csv('CoVID_19_China.csv')
N = data['确诊'].values[-1] + data['死亡'].values[-1]
data['易感染'] = data['确诊'].values[::-1] + data['死亡'].values[::-1]
I0 = data['确诊'].values[0]
sir = SIR(I0, N)
X = list(range(len(data)))
sir.fit(X, data['治愈'])
sir.fit_and_predict_plot(X, data, ['易感染', '确诊', '治愈'], ['1月', '2月', '3月', '4月', '5月', '6月', '7月'])
