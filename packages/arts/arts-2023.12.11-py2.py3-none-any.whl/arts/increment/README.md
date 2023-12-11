# 项目描述

分布式主键生成器，支持多机器\|多进程\|多线程并发生成。

# 导入

```python
from arts.increment import Incrementer
```

# 创建生成器

```python
inc = Incrementer()
```

# 使用创建生成器时的时间

```python
inc.pk1()
# >>> 'lg85x42f_gsdo_258_1'

inc.pk1()
# >>> 'lg85x42f_gsdo_258_2'

# 'lg85x42f'是创建生成器时的时间
```

# 使用当前时间

```python
inc.pk2()
# >>> 'lg8657cj_gsdo_258_3'

# 'lg8657cj'是当前时间
```

# 只返回自增主键

```python
inc.pk3()
# >>> '4'

inc.pk3()
# >>> '5'
```
