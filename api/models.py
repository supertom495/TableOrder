# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, LargeBinary, NCHAR, SmallInteger, String, Table, Unicode, UnicodeText, text
from sqlalchemy.dialects.mssql import BIT, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Tables(Base):
    __tablename__ = 'Tables'

    # column_not_exist_in_db = Column(Integer) # just add for sake of this error, dont add in db
    table_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    table_code= Column(Unicode(15), nullable=False)
    table_status = Column('table_status', SmallInteger, nullable=False),
    seats = Column('seats', SmallInteger, nullable=False)
    inactive = Column('inactive', BIT, nullable=False)
    staff_id = Column(Integer)
    logon_time = Column(DateTime)
    table_shape = Column(SmallInteger)
    table_left = Column(SmallInteger)
    table_top = Column(SmallInteger)
    table_width = Column(SmallInteger)
    table_height = Column(SmallInteger)
    show_state = Column(SmallInteger)
    table_fore_color = Column(Integer)
    table_font_size = Column(SmallInteger)
    state_fore_color = Column(Integer)
    state_font_size = Column(SmallInteger)
    customer_name = Column(Unicode(60))
    table_left_rate = Column(Float(24))
    table_top_rate = Column(Float(24))
    table_width_rate = Column(Float(24))
    table_height_rate = Column(Float(24))
    computer_user = Column(Unicode(100))
    start_time = Column(DateTime)
    ip = Column(Unicode(20))
    kb_id = Column(Integer)


class Keyboard(Base):
    __tablename__ = 'Keyboard'
    kb_id = Column(Integer, nullable=False, primary_key=True)
    kb_name = Column(Unicode(64), nullable=False)
    btn_page = Column(Integer, nullable=False)
    btn_left = Column(Integer, nullable=False)
    btn_top = Column(Integer, nullable=False)
    btn_width = Column(Integer, nullable=False)
    btn_height = Column(Integer, nullable=False)
    btn_forecolor = Column(Integer, nullable=False)
    btn_backcolor = Column(Integer, nullable=False)
    btn_fontname = Column(Unicode(64), nullable=False)
    btn_fontsize = Column(Integer, nullable=False)
    btn_showpic = Column(BIT, nullable=False)
    cat_cols = Column(SmallInteger)
    cat_height = Column(SmallInteger)
    kb_name2 = Column(Unicode(20))
    cat_rows = Column(SmallInteger)
    menu_type_id = Column(Integer)
    menu_type_limit = Column(Integer)

    @classmethod
    def getActivateKeyboard(cls):
        return cls.query.filter(Keyboard.kb_name2=='online').first()


class KeyboardCat(Base):
    __tablename__ = 'KeyboardCat'
    cat_id = Column(Integer, nullable=False, primary_key=True)
    cat_name = Column(Unicode(64), nullable=False)
    kb_id = Column(Integer, nullable=False)
    btn_page = Column(Integer, nullable=False)
    btn_left = Column(Integer, nullable=False)
    btn_top = Column(Integer, nullable=False)
    btn_width = Column(Integer, nullable=False)
    btn_height = Column(Integer, nullable=False)
    btn_forecolor = Column(Integer, nullable=False)
    btn_backcolor = Column(Integer, nullable=False)
    btn_fontname = Column(Unicode(64), nullable=False)
    btn_fontsize = Column(Integer, nullable=False)
    btn_showpic = Column(BIT, nullable=False)
    btn_rows = Column(SmallInteger)
    btn_cols = Column(SmallInteger)
    pic_align = Column(SmallInteger)
    text_align = Column(SmallInteger)
    invisible = Column(BIT)
    cat_code = Column(Unicode(15))

    @classmethod
    def getActivateKeyboardCat(cls):
        res = cls.query.join(Keyboard, Keyboard.kb_id == cls.kb_id).filter(Keyboard.kb_name2 == 'online').all()
        return res

class KeyboardItem(Base):
    __tablename__ = 'KeyboardItem'
    item_id = Column(Integer, nullable=False, primary_key=True)
    item_barcode = Column(Unicode(24), nullable=False)
    item_name = Column(Unicode(64), nullable=False)
    cat_id = Column(Integer, nullable=False, primary_key=True)
    kb_id = Column(Integer, nullable=False, primary_key=True)
    # btn_page = Column(Integer, nullable=False)
    # btn_left = Column(Integer, nullable=False)
    # btn_top = Column(Integer, nullable=False)
    # btn_width = Column(Integer, nullable=False)
    # btn_height = Column(Integer, nullable=False)
    # btn_forecolor = Column(Integer, nullable=False)
    # btn_backcolor = Column(Integer, nullable=False)
    # btn_fontname = Column(Unicode(64), nullable=False)
    # btn_fontsize = Column(Integer, nullable=False)
    # btn_showpic = Column(BIT, nullable=False)
    # btn_showprice = Column(BIT)
    subcat_id = Column(Integer)
    stock_id = Column(Integer)
    subcat_link = Column(Unicode(999))

    @classmethod
    def getAvtiveKeyboardItem(cls, kbCatIds, kbId):
        res = cls.query.filter(cls.cat_id.in_(kbCatIds), cls.kb_id == kbId).all()
        return res



class Category(Base):
    __tablename__ = 'Category'
    cat_id = Column(Integer, nullable=False, primary_key=True)
    cat_code = Column(Unicode(15), nullable=False)
    cat_name = Column(Unicode(40))
    cat_name2 = Column(Unicode(40), nullable=False)
    time_id = Column(Integer, nullable=False)
    printer = Column(Unicode(80))
    printer2 = Column(Unicode(80))
    inactive = Column(BIT, nullable=False)
    modifier1 = Column(Unicode(20))
    modifier2 = Column(Unicode(20))
    modifier3 = Column(Unicode(20))
    modifier4 = Column(Unicode(20))
    cat_name3 = Column(Unicode(40))
    cat_name4 = Column(Unicode(40))

    @classmethod
    def getCategoryNameByCatCode(cls, catCode):
        res = cls.query.filter(cls.cat_code == catCode).one()
        return res


class Stock(Base):
    __tablename__ = 'Stock'
    __table_args__ = (
        Index('Sub', 'cat2', 'stock_id', unique=True),
        Index('Cat', 'cat1', 'stock_id', unique=True),
        Index('Bar code', 'barcode', 'stock_id', unique=True),
        Index('Supplier', 'supplier_id', 'stock_id', unique=True),
        Index('Custom1', 'custom1', 'stock_id', unique=True),
        Index('Categories', 'cat1', 'cat2', 'stock_id', unique=True),
        Index('Description', 'description', 'stock_id', unique=True),
        Index('Custom2', 'custom2', 'stock_id', unique=True)
    )

    stock_id = Column(Float(53), primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, index=True)
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    sales_prompt = Column(Unicode(100))
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    allow_renaming = Column(BIT, nullable=False, server_default=text("(0)"))
    allow_fractions = Column(BIT, nullable=False, server_default=text("(0)"))
    package = Column(BIT, nullable=False, server_default=text("(0)"))
    tax_components = Column(BIT, nullable=False, server_default=text("(0)"))
    print_components = Column(BIT, nullable=False, server_default=text("(0)"))
    description = Column(Unicode(60), nullable=False)
    longdesc = Column(Unicode(255), nullable=False)
    cat1 = Column(Unicode(20), nullable=False)
    cat2 = Column(Unicode(20), nullable=False)
    goods_tax = Column(Unicode(3), nullable=False)
    cost = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    layby_qty = Column(Float(53), nullable=False, server_default=text("(0)"))
    salesorder_qty = Column(Float(53), nullable=False, server_default=text("(0)"))
    date_created = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    track_serial = Column(BIT, nullable=False, server_default=text("(0)"))
    static_quantity = Column(BIT, nullable=False, server_default=text("(0)"))
    bonus = Column(MONEY, nullable=False, server_default=text("(0)"))
    order_threshold = Column(Float(53), nullable=False, server_default=text("(0)"))
    order_quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    freight = Column(BIT, nullable=False, server_default=text("(0)"))
    use_scale = Column(BIT, nullable=False, server_default=text("(0)"))
    item_code = Column(Unicode(16), nullable=False)
    custom3 = Column(Unicode(50), nullable=False)
    custom4 = Column(Unicode(50), nullable=False)
    description2 = Column(Unicode(60), nullable=False)
    sell2 = Column(MONEY)
    sell3 = Column(MONEY)
    sell4 = Column(MONEY)
    show_extra = Column(BIT)
    show_taste = Column(BIT)
    show_qty = Column(BIT)
    cost2 = Column(MONEY)
    cost3 = Column(MONEY)
    cost4 = Column(MONEY)
    kitchen_desc = Column(Unicode(60))
    kitchen_desc2 = Column(Unicode(60))
    description3 = Column(Unicode(60))
    description4 = Column(Unicode(60))
    longdesc2 = Column(Unicode(255))
    longdesc3 = Column(Unicode(255))
    longdesc4 = Column(Unicode(255))
    sell5 = Column(MONEY)
    sell6 = Column(MONEY)
    sell7 = Column(MONEY)
    sell8 = Column(MONEY)

    # supplier = relationship('Supplier')

    @classmethod
    def getStockById(cls, stockId):
        return cls.query.filter(cls.stock_id == stockId).one()


class TasteStock(Base):
    __tablename__ = 'TasteStock'
    stock_id = Column(Integer, nullable=False, primary_key=True)
    taste_id = Column(Integer, nullable=False, primary_key=True)

    @classmethod
    def getAll(cls):
        return cls.query.all()




class ExtraStock(Base):
    __tablename__ = 'ExtraStock'
    stock_id = Column(Integer, nullable=False, primary_key=True)
    extra_id = Column(Integer, nullable=False, primary_key=True)

    @classmethod
    def getAll(cls):
        return cls.query.all()
