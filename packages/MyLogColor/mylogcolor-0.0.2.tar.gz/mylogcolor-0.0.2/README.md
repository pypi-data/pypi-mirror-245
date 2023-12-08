##### 这是一个简单的带颜色输出的包，主要用于支持代码调试的时候打印出来的内容变成不同的彩色

##### 以下是使用例子：

```python
from MyLogColor import log,LogLevel


log('Hello,错误', LogLevel.ERROR)
log('Hello,通过', LogLevel.PASS)
log('Hello,信息', LogLevel.INFO)
log('Hello,至关重要的', LogLevel.CRITICAL)
log('Hello,警告', LogLevel.WARN)
log('Hello,愚蠢的', LogLevel.SILLY)
log('Hello,成功', LogLevel.SUCCESS)
```
