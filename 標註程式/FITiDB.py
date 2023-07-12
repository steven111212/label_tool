
from sqlalchemy import Table, Column, ForeignKey, Integer, String,Float, create_engine,Boolean,DateTime, MetaData ,DECIMAL,Enum
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship
import datetime
import json

# 建立db位置
# 檢查db位置目錄是否存在 
basedir = os.path.abspath(os.path.dirname(__name__))
db_folderpath = os.path.join(basedir,'sys')
if os.path.isdir(db_folderpath):
    print("目錄存在。")
else:    
    print("db位置目錄不存在。")
    os.makedirs(db_folderpath)
print('db位置目錄:',basedir)
db_url="sqlite:///" + os.path.join(db_folderpath, "FITICV_test2.db")

#创建数据库连接
engine = create_engine(db_url,echo=False)      #echo ：为 True 时候会把sql语句打印出来

Session = sessionmaker(bind=engine)   # 绑定引擎   在ORM 中我们使用 Session 访问数据库。
session = scoped_session(Session)
metadata = MetaData(engine)
# metadata.drop_all(engine)  
Base = declarative_base(metadata=metadata)
    
#建立父纇class
class CommonRoutines(Base):
    __abstract__ = True    
    __table_args__ = {'extend_existing': True}		# 避免flask迁移数据库,二次创建表问题
    
    def __init__(self):
        pass
    
    def add(self):
        session.add(self)
        session.commit()
    def delete(self):
        session.delete(self)
        session.commit()     
        
    @classmethod
    def get_with_id(cls, gid):
        # result = session.query(gid)        
        return session.query(cls).filter_by(id=gid).first()   
    @classmethod
    def get_with_all(cls):
        return session.query(cls).all()
    
    
class Labelinfo(CommonRoutines):
    __tablename__ = 'labelinfo'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    image_path = Column(String(500), nullable=True)
    image_height = Column(Integer)
    image_width = Column(Integer)
    # label_list = Column(String(500), nullable=True)
    # point_list = Column(String(500), nullable=True)
    # shape_type = Column(String(500), nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
   
    def __repr__(self):
        return "<Labelinfo %r>" % self.id
    
    def __init__(self,image_path, image_height, image_width):
        self.image_path = image_path
        self.image_height = image_height
        self.image_width = image_width
        # self.label_list = label_list
        # self.point_list = point_list
        # self.shape_type = shape_type
        self.loading_time = datetime.datetime.now()


        
Base.metadata.create_all()  # 将模型映射到数据库中
def create_table():  # 创建表
    Base.metadata.create_all(engine)


def drop_table():  # 删除表
    Base.metadata.drop_all(engine)


def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

if __name__ == '__main__':
    # drop_table()        #刪除table
    # create_table()      #創建table
    # print("finish")
    
    image_path='.test/20230515img.png'
    image_height=2048
    image_width=2448
    # label_list={"ng1"}
    # point_list={[[10,10],[50,70],[90,150],[30,60]],[[10,10],[50,10],[50,50],[50,10]]}
    # shape_type=["polygon","rectangle"]
    
    Labelinfo(image_path, image_height, image_width).add()
    

        
    # for test_name in ['IDS','TSC','ACD','FEA']:
        
    #     user_instance = Projectinfo(
    #     name=test_name,
    #     label_name_to_value= json.dumps({"TEST1":1,"DEFECT":2}, indent=4)    
    #     )
    #     user_instance.add()
    # id=3
    # defect_id=Projectinfo.get_with_id(id)
    # print(defect_id.id)
    # defect_id.description='test one two three'
    # session.commit()
    # user_instance = Datasetinfo(defect_id=defect_id.id,train_num=30, valid_num=15, new_train_num=10, new_valid_num=7) 
    # user_instance.add()
    

    # session.add(user_instance)
    # # 提交
    # session.commit()
    # session.close()