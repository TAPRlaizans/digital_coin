# 配对交易
## 1.定义
是一种在特定金融市场出现**不均衡条件**时，投资者同时**买入低估资产**并**卖出高估资产**的**对冲**策略。

## 2.基本原理
找出两只**走势相关**的股票。这两只股票的价格差距从**长期**来看在一个**固定的水平内波动**，如果价差**暂时性的**超过或低于这个水平，就买多价格偏低的股票，卖空价格偏高的股票。等到价差恢复正常水平时，进行平仓操作，赚取这一过程中价差变化所产生的利润。

## 3.核心关键
必须找到一对价格走势高度相关的股票。而高度相关在这里意味着在长期来看有一个稳定的价差，这就要用到**协整关系的检验**。

## 4.操作步骤
- 相关性检验
- 买卖时机的判断
- 策略完整交易系统设计
- 策略回测部分

（1）相关性检验工具
单位根检验（ADF检验）
约束最小二乘法（Engle-Granger方法）
欧氏距离法
协整
相关性
随机差分残差（SDR）
遗传算法（GA）
非支配排序遗传算法 II (NSGA-II)

ADF检验就是判断序列是否存在单位根:如果序列平稳，就不存在单位根:否则，就会存在单位根。
代码实现：
使用python中的 statsmodels 模块
```
//使用到的模块
from statsmodels.tsa.stattools import adfuller

//接口定义
def adfuller(x, maxlag=None, regression="c", autolag='AIC',
             store=False, regresults=False):
    """
    Augmented Dickey-Fuller unit root test
    The Augmented Dickey-Fuller test can be used to test for a unit root in a
    univariate process in the presence of serial correlation.
    Parameters
    ----------
    x : array_like, 1d
        data series
    maxlag : int
        Maximum lag which is included in test, default 12*(nobs/100)^{1/4}
    regression : {'c','ct','ctt','nc'}
        Constant and trend order to include in regression
        * 'c' : constant only (default)
        * 'ct' : constant and trend
        * 'ctt' : constant, and linear and quadratic trend
        * 'nc' : no constant, no trend
    autolag : {'AIC', 'BIC', 't-stat', None}
        * if None, then maxlag lags are used
        * if 'AIC' (default) or 'BIC', then the number of lags is chosen
          to minimize the corresponding information criterion
        * 't-stat' based choice of maxlag.  Starts with maxlag and drops a
          lag until the t-statistic on the last lag length is significant
          using a 5%-sized test
    store : bool
        If True, then a result instance is returned additionally to
        the adf statistic. Default is False
    regresults : bool, optional
        If True, the full regression results are returned. Default is False
    Returns
    -------
    adf : float
        Test statistic
    pvalue : float
        MacKinnon's approximate p-value based on MacKinnon (1994, 2010)
    usedlag : int
        Number of lags used
    nobs : int
        Number of observations used for the ADF regression and calculation of
        the critical values
    critical values : dict
        Critical values for the test statistic at the 1 %, 5 %, and 10 %
        levels. Based on MacKinnon (2010)
    icbest : float
        The maximized information criterion if autolag is not None.
    resstore : ResultStore, optional
        A dummy class with results attached as attributes
    """
```


## 参考资料：
论文 https://www.mdpi.com/2673-4591/38/1/74
视频：布偶量化https://www.youtube.com/watch?v=wJTOcrAArRU 
