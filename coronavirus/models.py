# 数据库表，表中有哪些字段

from sqlalchemy import Column, String, Integer, BigInteger, \
    Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    # Data 是关联的类名，back_pupulates 来指定反向访问的属性名称
    data = relationship('Data', back_populates='city')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), comment='更新时间')

    # 对获取到的属性进行排序
    # 默认是正序，倒序加上.desc()方法
    __mapper_args__ = {"order_by": country_code}

    def __repr__(self):
        return f'{self.country}_{self.province}'

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # ForeignKey里的字符串格式不是类名.属性名，而是表名.字段名
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    # 'City'是关联的类名；back_populates来指定反向访问的属性名称
    city = relationship('City', back_populates='data')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 按日期降序
    __mapper_args__ = {"order_by": date.desc()}

    def __repr__(self):
        return f'{repr(self.date)}:确诊{self.confirmed}例'
