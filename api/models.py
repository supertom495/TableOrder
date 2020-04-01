# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, LargeBinary, NCHAR, SmallInteger, String, Table, Unicode, UnicodeText, text
from sqlalchemy.dialects.mssql import BIT, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence
from sqlalchemy.sql import func
from database import Base, db_session
import decimal


class Tables(Base):
    __tablename__ = 'Tables'

    # column_not_exist_in_db = Column(Integer) # just add for sake of this error, dont add in db
    table_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    table_code= Column(Unicode(15), nullable=False)
    table_status = Column(SmallInteger, nullable=False)
    seats = Column(SmallInteger, nullable=False)
    inactive = Column(BIT, nullable=False)
    staff_id = Column(Integer)
    logon_time = Column(DateTime)
    computer_user = Column(Unicode(100))
    start_time = Column(DateTime)
    ip = Column(Unicode(20))
    kb_id = Column(Integer)

    @classmethod
    def getTableAll(cls):
        return cls.query.all()

    @classmethod
    def getTableByTableCode(cls, tableCode):
        return cls.query.filter(cls.table_code == tableCode).first()

    @classmethod
    def activateTable(cls, tableCode, time):
        return cls.query.filter(cls.table_code == tableCode).update({"table_status": 2, "start_time": time})


class Site(Base):
    __tablename__ = 'Site'
    site_id = Column(Integer, nullable=False, primary_key=True)
    site_code = Column(Unicode(15), nullable=False)
    site_name = Column(Unicode(20), nullable=False)
    site_name2 = Column(Unicode(20), nullable=False)
    inactive = Column(BIT, nullable=False)
    printer = Column(Unicode(60))
    printer2 = Column(Unicode(60))

    @classmethod
    def getSiteAll(cls):
        return cls.query.all()



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
        return cls.query.filter(cls.kb_name2=='online').first()


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



class Staff(Base):
    __tablename__ = 'Staff'
    __table_args__ = (
        Index('Custom1', 'custom1', 'staff_id', unique=True),
        Index('Position', 'position', 'staff_id', unique=True),
        Index('Given Names', 'given_names', 'staff_id', unique=True),
        Index('Surname', 'surname', 'staff_id', unique=True),
        Index('Barcode', 'barcode', 'staff_id', unique=True),
        Index('Docket Name', 'docket_name', 'staff_id', unique=True),
        Index('State', 'state', 'staff_id', unique=True),
        Index('Custom2', 'custom2', 'staff_id', unique=True),
        Index('Suburb', 'suburb', 'staff_id', unique=True)
    )

    staff_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, unique=True)
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    surname = Column(Unicode(50), nullable=False)
    given_names = Column(Unicode(50), nullable=False)
    docket_name = Column(Unicode(50), nullable=False)
    position = Column(Unicode(50), nullable=False)
    dob = Column(DateTime, nullable=False)
    commission = Column(Float(53), nullable=False, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    mobile = Column(Unicode(20), nullable=False)
    email = Column(Unicode(50), nullable=False)
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    status = Column(BIT, nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))

    @classmethod
    def getStaffByBarcode(cls, barcode):
        return cls.query.filter(cls.barcode == barcode).first()


class Salesorder(Base):
    __tablename__ = 'SalesOrder'

    salesorder_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    expiry_date = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    transaction = Column(Unicode(2), nullable=False, index=True)
    original_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    custom = Column(Unicode(40))
    comments = Column(Unicode(255), nullable=False)
    subtotal = Column(MONEY, nullable=False, server_default=text("(0)"))
    discount = Column(MONEY, nullable=False, server_default=text("(0)"))
    rounding = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    guest_no = Column(SmallInteger)
    customer_name = Column(Unicode(40))
    origin = Column(Integer)

    customer = relationship('Customer')
    staff = relationship('Staff')

    @classmethod
    def insertSalesorder(cls, tableCode, guestNo, staffId, time):

        max =  cls.query.session.query(func.max(cls.salesorder_id).label("max_id")).one()
        salesorder_id = 1 if max.max_id is None else max.max_id + 1

        newSalesorder = Salesorder(salesorder_id = salesorder_id,
                                   salesorder_date = time,
                                   expiry_date = time,
                                   staff_id = staffId,
                                   custom = tableCode,
                                   customer_name = tableCode,
                                   guest_no = guestNo,
                                   transaction = 'DI',
                                   comments = '')
        cls.query.session.add(newSalesorder)
        return salesorder_id

    @classmethod
    def getSalesorderByTableCode(cls, tableCode):
        return cls.query.filter(cls.custom == tableCode).order_by(cls.salesorder_date.desc()).first()

    @classmethod
    def updatePrice(cls, salesorderId):
        salesorder = cls.query.filter(cls.salesorder_id == salesorderId).one()
        salesOrderLines = SalesorderLine.query.filter(SalesorderLine.salesorder_id == salesorderId).all()
        if len(salesOrderLines) == 0:
            return

        salesorder.total_ex  = decimal.Decimal(0)
        salesorder.total_inc =  decimal.Decimal(0)

        for line in salesOrderLines:
            salesorder.total_ex += line.print_ex
            salesorder.total_inc += line.print_inc

        salesorder.subtotal = salesorder.total_inc

        return



class SalesorderLine(Base):
    __tablename__ = 'SalesOrderLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_id = Column(ForeignKey('SalesOrder.salesorder_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    parentline_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    package = Column(BIT, nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    orderline_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    size_level = Column(SmallInteger)
    staff_id = Column(Integer)
    time_ordered = Column(DateTime)
    out_order = Column(SmallInteger)
    hand_writting = Column(BIT)
    seq_id = Column(Integer)
    original_line_id = Column(Integer)

    salesorder = relationship('Salesorder')
    stock = relationship('Stock')

    @classmethod
    def insertSalesorderLine(cls, salesorderId, stockId, sizeLevel, price, quantity, staffId, time, parentlineId, orderlineId=None):
        max =  cls.query.session.query(func.max(cls.line_id).label("max_id")).one()
        salesorderLineId = 1 if max.max_id is None else max.max_id + 1
        if orderlineId is None:
            orderlineId = salesorderLineId

        newSalesorderLine = SalesorderLine(line_id = salesorderLineId,
                                   salesorder_id = salesorderId,
                                   stock_id = stockId,
                                   sales_tax = 'GST',
                                   sell_ex = price,
                                   sell_inc = round(price * decimal.Decimal(1.1), 2),
                                   rrp = round(price * decimal.Decimal(1.1), 2),
                                   print_ex = round(price * decimal.Decimal(1.1), 2),
                                   print_inc = round(price * decimal.Decimal(1.1), 2),
                                   quantity = quantity,
                                   parentline_id = parentlineId,
                                   status = 1,
                                   orderline_id = orderlineId,
                                   size_level = sizeLevel,
                                   staff_id = staffId,
                                   time_ordered = time)
        cls.query.session.add(newSalesorderLine)
        cls.query.session.commit()
        return salesorderLineId


    @classmethod
    def getSalesorderLine(cls, salesorderId):
        return cls.query.filter(cls.salesorder_id == salesorderId).all()


class Kitchen(Base):
    __tablename__ = 'Kitchen'
    line_id = Column(Integer, nullable=False, primary_key=True)
    orderline_id = Column(Integer, nullable=False)
    table_code = Column(Unicode(40))
    staff_name = Column(Unicode(40), nullable=False)
    cat1 = Column(Unicode(40))
    description = Column(Unicode(60))
    description2 = Column(Unicode(60))
    unit = Column(Unicode(30))
    quantity = Column(Float(24), nullable=False)
    printer = Column(Unicode(100))
    printer2 = Column(Unicode(100))
    order_time = Column(DateTime, nullable=False)
    handwritting = Column(BIT, nullable=False)
    comments = Column(Unicode(200))
    stock_type = Column(SmallInteger)
    out_order = Column(SmallInteger)
    customer_name = Column(Unicode(40))
    cat2 = Column(Unicode(40))
    salesorder_id = Column(Integer)
    status = Column(SmallInteger)
    original_line_id = Column(Integer)




class Customer(Base):
    __tablename__ = 'Customer'
    __table_args__ = (
        Index('Country', 'country', 'customer_id', unique=True),
        Index('Surname', 'surname', 'customer_id', unique=True),
        Index('Customer Name', 'surname', 'given_names', 'customer_id', unique=True),
        Index('Given Names', 'given_names', 'customer_id', unique=True),
        Index('Suburb', 'suburb', 'customer_id', unique=True),
        Index('Custom1', 'custom1', 'customer_id', unique=True),
        Index('Salutation', 'salutation', 'customer_id', unique=True),
        Index('Company', 'company', 'customer_id', unique=True),
        Index('Position', 'position', 'customer_id', unique=True),
        Index('Custom2', 'custom2', 'customer_id', unique=True),
        Index('State', 'state', 'customer_id', unique=True),
        Index('Barcode', 'barcode', 'customer_id', unique=True),
        Index('AC Owner', 'owner_id', 'customer_id', unique=True)
    )

    customer_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, unique=True)
    grade = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    notes = Column(Unicode(255), nullable=False)
    comments = Column(Unicode(255), nullable=False)
    status = Column(BIT, nullable=False, server_default=text("(0)"))
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    surname = Column(Unicode(50), nullable=False)
    given_names = Column(Unicode(50), nullable=False)
    position = Column(Unicode(50), nullable=False)
    company = Column(Unicode(50), nullable=False)
    salutation = Column(Unicode(5), nullable=False)
    account = Column(BIT, nullable=False, server_default=text("(0)"))
    opened_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    owner_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    limit = Column(MONEY, nullable=False, server_default=text("(0)"))
    days = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    fromEOM = Column(BIT, nullable=False, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    country = Column(Unicode(20), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    fax = Column(Unicode(20), nullable=False)
    mobile = Column(Unicode(20), nullable=False)
    email = Column(Unicode(50), nullable=False)
    abn = Column(Unicode(11), nullable=False)
    overseas = Column(BIT, nullable=False, server_default=text("(0)"))
    total_points = Column(Integer)
    unclaimed_points = Column(Integer)
    dob = Column(DateTime)
    sex = Column(Unicode(1))
    receive_info = Column(BIT)
    prepaid_amt = Column(MONEY)

    opened = relationship('Staff', primaryjoin='Customer.opened_id == Staff.staff_id')
    owner = relationship('Staff', primaryjoin='Customer.owner_id == Staff.staff_id')